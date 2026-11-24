const numeroEntero = new Intl.NumberFormat("es-CO", {
  maximumFractionDigits: 0,
});
const numeroDecimal = new Intl.NumberFormat("es-CO", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
const numeroPorcentaje = new Intl.NumberFormat("es-CO", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

async function leerJson(ruta) {
  const respuesta = await fetch(new URL(ruta, import.meta.url));
  if (!respuesta.ok) {
    throw new Error(`No fue posible cargar ${ruta}: HTTP ${respuesta.status}.`);
  }
  return respuesta.json();
}

export async function cargarResultados() {
  const [paqueteIndicadores, ranking, distribucion] = await Promise.all([
    leerJson("../data/indicadores.json"),
    leerJson("../data/ranking.json"),
    leerJson("../data/distribucion.json"),
  ]);
  if (
    !paqueteIndicadores.indicadores ||
    !paqueteIndicadores.metadatos ||
    !Array.isArray(ranking.territorios) ||
    !Array.isArray(distribucion.intervalos)
  ) {
    throw new Error("Los archivos JSON no tienen la estructura esperada.");
  }
  return { indicadores: paqueteIndicadores.indicadores, metadatos: paqueteIndicadores.metadatos, ranking, distribucion };
}

function mostrarNumero(elemento, valor, decimales = 0) {
  const formato = decimales ? numeroDecimal : numeroEntero;
  const duracion = window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 850;
  if (!duracion) {
    elemento.textContent = formato.format(valor);
    return;
  }
  const inicio = performance.now();
  const animar = (ahora) => {
    const avance = Math.min((ahora - inicio) / duracion, 1);
    const suavizado = 1 - (1 - avance) ** 3;
    elemento.textContent = formato.format(valor * suavizado);
    if (avance < 1) window.requestAnimationFrame(animar);
  };
  window.requestAnimationFrame(animar);
}

function asignarNumero(clave, valor, decimales = 0) {
  document.querySelectorAll(`[data-indicador="${clave}"]`).forEach((elemento) => {
    mostrarNumero(elemento, valor, decimales);
  });
}

function asignarTexto(clave, texto) {
  document.querySelectorAll(`[data-meta="${clave}"]`).forEach((elemento) => {
    elemento.textContent = texto;
  });
}

function mostrarMetadatos(metadatos, indicadores) {
  const pendientes = "Pendiente de confirmación";
  asignarTexto("autor", metadatos.autor || pendientes);
  asignarTexto("institucion", metadatos.institucion || pendientes);
  asignarTexto("periodo_referencia", metadatos.periodo_referencia || pendientes);
  asignarTexto("fuente_original", metadatos.fuente_original || "Pendiente de confirmación documental");
  asignarTexto("fuente_resumen", indicadores.fuente);
  asignarTexto("registros_originales", numeroEntero.format(metadatos.registros_originales));
  asignarTexto("registros_finales", numeroEntero.format(metadatos.registros_finales));
  asignarTexto("unidad_observacion", metadatos.unidad_observacion);
  const fecha = document.querySelectorAll('[data-meta="fecha_generacion"]');
  fecha.forEach((elemento) => {
    const valor = metadatos.fecha_generacion;
    elemento.textContent = valor
      ? new Intl.DateTimeFormat("es-CO", { dateStyle: "long", timeZone: "UTC" }).format(new Date(`${valor}T00:00:00Z`))
      : "No disponible";
    if (elemento instanceof HTMLTimeElement && valor) elemento.dateTime = valor;
  });
  asignarTexto("herramientas", metadatos.herramientas.join(", "));
}

function mostrarIndicadores(indicadores, ranking) {
  asignarNumero("total_capturas", indicadores.total_capturas);
  asignarNumero("numero_territorios", indicadores.numero_territorios);
  asignarNumero("tamano_muestra_territorios", indicadores.tamano_muestra_territorios);
  asignarNumero("promedio_capturas_por_territorio", indicadores.promedio_capturas_por_territorio, 2);
  asignarNumero("mediana_capturas_por_territorio", indicadores.mediana_capturas_por_territorio);
  asignarNumero("minimo_capturas", indicadores.minimo_capturas);
  asignarNumero("maximo_capturas", indicadores.maximo_capturas);
  const atipicos = indicadores.posibles_valores_atipicos
    .map((fila) => `${fila.departamento} (${numeroEntero.format(fila.capturas)})`)
    .join("; ");
  document.querySelectorAll('[data-indicador="posibles_atipicos"]').forEach((elemento) => {
    elemento.textContent = atipicos || "No se identificaron según el criterio aplicado";
  });
  const territorioMayor = indicadores.territorios_maximo.join(", ");
  document.querySelectorAll('[data-indicador="territorio_maximo"]').forEach((elemento) => {
    elemento.textContent = territorioMayor;
  });
  const concentracionCinco = indicadores.concentracion_top["5"];
  document.querySelectorAll('[data-indicador="top5_porcentaje"]').forEach((elemento) => {
    mostrarNumero(elemento, concentracionCinco.participacion_porcentual, 2);
  });
  document.querySelectorAll('[data-detalle="top5_capturas"]').forEach((elemento) => {
    elemento.textContent = numeroEntero.format(concentracionCinco.capturas);
  });
  if (ranking.territorios.length !== indicadores.tamano_muestra_territorios) {
    throw new Error("El número de territorios del ranking no coincide con los indicadores.");
  }
}

function mostrarConcentraciones(indicadores) {
  for (const cantidad of ["3", "5", "10"]) {
    const dato = indicadores.concentracion_top[cantidad];
    const porcentaje = dato.participacion_porcentual;
    document.querySelectorAll(`[data-concentracion="${cantidad}"]`).forEach((barra) => {
      barra.value = porcentaje;
      barra.setAttribute(
        "aria-valuetext",
        `${numeroPorcentaje.format(porcentaje)} por ciento, ${numeroEntero.format(dato.capturas)} capturas`,
      );
    });
    document.querySelectorAll(`[data-concentracion-texto="${cantidad}"]`).forEach((texto) => {
      texto.textContent = `${numeroPorcentaje.format(porcentaje)} % · ${numeroEntero.format(dato.capturas)} capturas`;
    });
  }
}

function mostrarFrecuencias(distribucion) {
  const cuerpo = document.querySelector("#frecuencias-body");
  cuerpo.replaceChildren();
  for (const intervalo of distribucion.intervalos) {
    const fila = document.createElement("tr");
    const nombre = document.createElement("th");
    nombre.scope = "row";
    nombre.textContent = intervalo.etiqueta;
    const frecuencia = document.createElement("td");
    frecuencia.textContent = numeroEntero.format(intervalo.territorios);
    fila.append(nombre, frecuencia);
    cuerpo.append(fila);
  }
}

export function mostrarResultados(resultados) {
  mostrarMetadatos(resultados.metadatos, resultados.indicadores);
  mostrarIndicadores(resultados.indicadores, resultados.ranking);
  mostrarConcentraciones(resultados.indicadores);
  mostrarFrecuencias(resultados.distribucion);
}

const nombresColumnas = {
  posicion: "posicion",
  departamento: "departamento",
  capturas: "capturas",
  participacion_porcentual: "participacion_porcentual",
};

function formatearParticipacion(fila) {
  return `${numeroPorcentaje.format(fila.participacion_porcentual)} % · ${numeroEntero.format(fila.capturas)} capturas`;
}

export function iniciarTablaRanking(ranking) {
  const controles = {
    filtro: document.querySelector("#filtro-rango"),
    orden: document.querySelector("#orden-ranking"),
    busqueda: document.querySelector("#buscar-territorio"),
    cuerpo: document.querySelector("#ranking-body"),
    estado: document.querySelector("#estado-tabla"),
    tabla: document.querySelector("#tabla-ranking"),
  };
  let columnaOrden = "posicion";
  let direccionOrden = "asc";

  function actualizar() {
    const longitud = ranking.territorios.length;
    let filas = [...ranking.territorios];
    if (controles.filtro.value === "primeros5") filas = filas.filter((fila) => fila.posicion <= 5);
    if (controles.filtro.value === "primeros10") filas = filas.filter((fila) => fila.posicion <= 10);
    if (controles.filtro.value === "ultimos5") filas = filas.filter((fila) => fila.posicion > longitud - 5);
    const termino = controles.busqueda.value.trim().toLocaleLowerCase("es-CO");
    if (termino) {
      filas = filas.filter((fila) => fila.departamento.toLocaleLowerCase("es-CO").includes(termino));
    }

    if (columnaOrden === "capturas" || columnaOrden === "participacion_porcentual") {
      filas.sort((a, b) => (a[columnaOrden] - b[columnaOrden]) * (direccionOrden === "asc" ? 1 : -1));
    } else if (columnaOrden === "departamento") {
      filas.sort((a, b) => a.departamento.localeCompare(b.departamento, "es-CO") * (direccionOrden === "asc" ? 1 : -1));
    } else {
      filas.sort((a, b) => (a.posicion - b.posicion) * (direccionOrden === "asc" ? 1 : -1));
    }

    controles.cuerpo.replaceChildren();
    for (const fila of filas) {
      const tr = document.createElement("tr");
      const valores = [
        numeroEntero.format(fila.posicion),
        fila.departamento,
        numeroEntero.format(fila.capturas),
        formatearParticipacion(fila),
      ];
      valores.forEach((valor, indice) => {
        const celda = document.createElement("td");
        celda.textContent = valor;
        if (indice === 0) celda.setAttribute("data-label", "Posición");
        if (indice === 1) celda.setAttribute("data-label", "Territorio");
        if (indice === 2) celda.setAttribute("data-label", "Capturas");
        if (indice === 3) celda.setAttribute("data-label", "Participación");
        tr.append(celda);
      });
      controles.cuerpo.append(tr);
    }
    controles.estado.textContent = `Mostrando ${numeroEntero.format(filas.length)} de ${numeroEntero.format(longitud)} territorios.`;
    if (!filas.length) {
      const filaVacia = document.createElement("tr");
      const celdaVacia = document.createElement("td");
      celdaVacia.colSpan = 4;
      celdaVacia.textContent = "No se encontraron territorios con esos criterios.";
      filaVacia.append(celdaVacia);
      controles.cuerpo.append(filaVacia);
    }
    controles.tabla.querySelectorAll("thead th").forEach((cabecera) => {
      const boton = cabecera.querySelector("[data-ordenar]");
      if (!boton) return;
      const activo = boton.dataset.ordenar === columnaOrden;
      cabecera.setAttribute("aria-sort", activo ? (direccionOrden === "asc" ? "ascending" : "descending") : "none");
    });
  }

  controles.filtro.addEventListener("change", actualizar);
  controles.orden.addEventListener("change", () => {
    columnaOrden = "capturas";
    direccionOrden = controles.orden.value;
    actualizar();
  });
  controles.busqueda.addEventListener("input", actualizar);
  controles.tabla.querySelectorAll("[data-ordenar]").forEach((boton) => {
    boton.addEventListener("click", () => {
      if (columnaOrden === boton.dataset.ordenar) {
        direccionOrden = direccionOrden === "asc" ? "desc" : "asc";
      } else {
        columnaOrden = nombresColumnas[boton.dataset.ordenar];
        direccionOrden = boton.dataset.ordenar === "posicion" ? "asc" : "desc";
      }
      if (columnaOrden === "capturas") controles.orden.value = direccionOrden;
      actualizar();
    });
  });
  actualizar();
}
