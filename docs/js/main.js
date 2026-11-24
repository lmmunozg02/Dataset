import { cargarResultados, iniciarTablaRanking, mostrarResultados } from "./visualizaciones.js";
import {
  iniciarMenu,
  iniciarNavegacionActiva,
  iniciarProgreso,
  iniciarRevelado,
} from "./interacciones.js";

document.documentElement.classList.add("js");
iniciarMenu();
iniciarProgreso();
iniciarNavegacionActiva();
iniciarRevelado();

const estadoDatos = document.querySelector("#estado-datos");

try {
  const resultados = await cargarResultados();
  mostrarResultados(resultados);
  iniciarTablaRanking(resultados.ranking);
} catch (error) {
  console.error("Error al cargar los resultados agregados:", error);
  estadoDatos.hidden = false;
  estadoDatos.textContent = `No se pudieron cargar los resultados agregados. ${error.message}`;
}
