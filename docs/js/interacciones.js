export function iniciarMenu() {
  const boton = document.querySelector(".boton-menu");
  const navegacion = document.querySelector("#navegacion-principal");
  if (!boton || !navegacion) return;

  const cerrar = () => {
    boton.setAttribute("aria-expanded", "false");
    navegacion.classList.remove("abierto");
    boton.querySelector(".sr-only").textContent = "Abrir menú de navegación";
  };
  boton.addEventListener("click", () => {
    const abierto = boton.getAttribute("aria-expanded") === "true";
    boton.setAttribute("aria-expanded", String(!abierto));
    navegacion.classList.toggle("abierto", !abierto);
    boton.querySelector(".sr-only").textContent = abierto
      ? "Abrir menú de navegación"
      : "Cerrar menú de navegación";
  });
  navegacion.querySelectorAll("a").forEach((enlace) => enlace.addEventListener("click", cerrar));
  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && boton.getAttribute("aria-expanded") === "true") {
      cerrar();
      boton.focus();
    }
  });
}

export function iniciarProgreso() {
  const barra = document.querySelector("#progreso-lectura");
  if (!barra) return;
  let pendiente = false;
  const actualizar = () => {
    const recorrido = document.documentElement.scrollHeight - window.innerHeight;
    const proporcion = recorrido > 0 ? Math.min(window.scrollY / recorrido, 1) : 0;
    barra.style.width = `${proporcion * 100}%`;
    pendiente = false;
  };
  window.addEventListener("scroll", () => {
    if (!pendiente) {
      window.requestAnimationFrame(actualizar);
      pendiente = true;
    }
  }, { passive: true });
  actualizar();
}

export function iniciarNavegacionActiva() {
  const enlaces = [...document.querySelectorAll('.navegacion a[href^="#"]')];
  const secciones = enlaces
    .map((enlace) => document.querySelector(enlace.getAttribute("href")))
    .filter(Boolean);
  if (!("IntersectionObserver" in window)) return;
  const observador = new IntersectionObserver((entradas) => {
    for (const entrada of entradas) {
      if (!entrada.isIntersecting) continue;
      const destino = `#${entrada.target.id}`;
      enlaces.forEach((enlace) => {
        if (enlace.getAttribute("href") === destino) enlace.setAttribute("aria-current", "location");
        else enlace.removeAttribute("aria-current");
      });
    }
  }, { rootMargin: "-22% 0px -68% 0px", threshold: 0 });
  secciones.forEach((seccion) => observador.observe(seccion));
}

export function iniciarRevelado() {
  const elementos = document.querySelectorAll(".revelar");
  if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    elementos.forEach((elemento) => elemento.classList.add("visible"));
    return;
  }
  const observador = new IntersectionObserver((entradas, instancia) => {
    entradas.forEach((entrada) => {
      if (entrada.isIntersecting) {
        entrada.target.classList.add("visible");
        instancia.unobserve(entrada.target);
      }
    });
  }, { threshold: 0.08 });
  elementos.forEach((elemento) => observador.observe(elemento));
}
