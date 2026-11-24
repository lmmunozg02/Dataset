"""Valida que los archivos agregados del sitio coincidan con los resultados."""

from __future__ import annotations

import json
import math
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
RUTA_DATOS_WEB = RAIZ_REPOSITORIO / "docs" / "data"
RAIZ_SITIO = RAIZ_REPOSITORIO / "docs"


class InspectorHtml(HTMLParser):
    """Recopila encabezados y recursos locales del documento principal."""

    def __init__(self) -> None:
        super().__init__()
        self.encabezados_h1 = 0
        self.referencias: list[str] = []

    def handle_starttag(self, etiqueta: str, atributos: list[tuple[str, str | None]]) -> None:
        valores = dict(atributos)
        if etiqueta == "h1":
            self.encabezados_h1 += 1
        if etiqueta in {"a", "link"} and valores.get("href"):
            self.referencias.append(str(valores["href"]))
        if etiqueta in {"script", "iframe", "img"} and valores.get("src"):
            self.referencias.append(str(valores["src"]))


def leer_json(nombre: str) -> dict[str, object]:
    ruta = RUTA_DATOS_WEB / nombre
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el resultado web: {ruta}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def leer_especificacion_grafico(nombre: str) -> tuple[dict[str, object], str]:
    ruta = RAIZ_SITIO / "graficos" / nombre
    contenido = ruta.read_text(encoding="utf-8")
    inicio_marcador = "var spec = "
    fin_marcador = ";\n      var embedOpt"
    inicio = contenido.find(inicio_marcador)
    if inicio < 0:
        raise ValueError(f"No se encontró la especificación Vega en {nombre}.")
    inicio += len(inicio_marcador)
    fin = contenido.find(fin_marcador, inicio)
    if fin < 0:
        raise ValueError(f"No se pudo delimitar la especificación Vega de {nombre}.")
    return json.loads(contenido[inicio:fin]), contenido


def validar() -> list[str]:
    indicadores = leer_json("indicadores.json")
    ranking = leer_json("ranking.json")
    distribucion = leer_json("distribucion.json")
    estadisticas = indicadores["indicadores"]
    territorios = ranking["territorios"]
    intervalos = distribucion["intervalos"]

    total = int(estadisticas["total_capturas"])
    muestra = int(estadisticas["tamano_muestra_territorios"])
    if len(territorios) != muestra or len(set(
        fila["departamento"] for fila in territorios
    )) != muestra:
        raise ValueError("El ranking no contiene un registro único por territorio.")
    if sum(int(fila["capturas"]) for fila in territorios) != total:
        raise ValueError("El total del ranking no coincide con los indicadores.")
    if not math.isclose(
        sum(float(fila["participacion_porcentual"]) for fila in territorios),
        100.0,
        abs_tol=0.01,
    ):
        raise ValueError("Las participaciones del ranking no suman 100 %.")
    if [int(fila["posicion"]) for fila in territorios] != list(
        range(1, muestra + 1)
    ):
        raise ValueError("Las posiciones del ranking no son consecutivas.")
    if sum(int(fila["territorios"]) for fila in intervalos) != muestra:
        raise ValueError("Las frecuencias no suman el tamaño de muestra.")
    if int(ranking["total_capturas"]) != total:
        raise ValueError("El total del ranking web no coincide con los indicadores.")
    if int(distribucion["tamano_muestra_territorios"]) != muestra:
        raise ValueError("El tamaño de muestra de la distribución no coincide.")

    archivos_graficos = (
        "distribucion.html",
        "ranking.html",
        "espacial.html",
    )
    titulos = {
        "distribucion.html": "¿Cómo se distribuye el número de capturas entre los territorios de Colombia?",
        "ranking.html": "¿Qué territorios presentan los mayores y menores registros de capturas?",
        "espacial.html": "¿Cómo se distribuyen geográficamente las capturas registradas en Colombia?",
    }
    for nombre in archivos_graficos:
        ruta = RAIZ_REPOSITORIO / "docs" / "graficos" / nombre
        if not ruta.is_file() or ruta.stat().st_size == 0:
            raise ValueError(f"El gráfico no existe o está vacío: {ruta}")
        especificacion, contenido = leer_especificacion_grafico(nombre)
        grafico = especificacion["vconcat"][0]
        titulo = grafico["title"]
        if titulo["text"] != titulos[nombre]:
            raise ValueError(f"El título del gráfico no coincide: {nombre}")
        if f"n = {muestra} territorios" not in titulo.get("subtitle", ""):
            raise ValueError(f"El gráfico no informa el tamaño de muestra: {nombre}")
        if "Fuente:" not in json.dumps(especificacion, ensure_ascii=False):
            raise ValueError(f"El gráfico no incluye la fuente: {nombre}")
        if grafico.get("width") != "container":
            raise ValueError(f"El gráfico no es adaptable: {nombre}")
        capas = grafico.get("layer", [])
        if not capas:
            raise ValueError(f"No se encontró la capa de barras: {nombre}")
        dominio = capas[0]["encoding"]["x"]["scale"]["domain"]
        if not dominio or dominio[0] != 0:
            raise ValueError(f"El eje de barras no comienza en cero: {nombre}")
        if not all(
            dependencia in contenido
            for dependencia in ("vega@6", "vega-lite@", "vega-embed@")
        ):
            raise ValueError(f"Falta una dependencia Vega en {nombre}.")

    ruta_html = RAIZ_SITIO / "index.html"
    inspector = InspectorHtml()
    inspector.feed(ruta_html.read_text(encoding="utf-8"))
    if inspector.encabezados_h1 != 1:
        raise ValueError("La página debe tener exactamente un encabezado H1.")
    for referencia in inspector.referencias:
        partes = urlsplit(referencia)
        if partes.scheme or partes.netloc or not partes.path:
            continue
        if partes.path.startswith("/"):
            raise ValueError(f"Se encontró una ruta local absoluta: {referencia}")
        destino = (RAIZ_SITIO / partes.path).resolve()
        try:
            destino.relative_to(RAIZ_SITIO.resolve())
        except ValueError as error:
            raise ValueError(f"Una ruta intenta salir de docs/: {referencia}") from error
        if not destino.is_file():
            raise FileNotFoundError(f"No se encontró el recurso local: {referencia}")
    if not (RAIZ_SITIO / ".nojekyll").is_file():
        raise FileNotFoundError("Falta docs/.nojekyll.")
    for nombre in ("indicadores.json", "ranking.json", "distribucion.json"):
        if not (RUTA_DATOS_WEB / nombre).is_file():
            raise FileNotFoundError(f"Falta el JSON web {nombre}.")
    for nombre in archivos_graficos:
        contenido = (RAIZ_SITIO / "graficos" / nombre).read_text(encoding="utf-8")
        if '"container"' not in contenido:
            raise ValueError(f"El gráfico no usa anchura adaptable: {nombre}")

    total_formateado = f"{total:,}".replace(",", ".")
    return [
        f"Indicadores contrastados: {total_formateado} capturas en {muestra} territorios.",
        "Ranking: posiciones, territorios, conteos y participaciones validados.",
        "Distribución: frecuencias y tamaño de muestra validados.",
        "Tres gráficos HTML presentes y no vacíos.",
        "Gráficos: título, fuente, muestra, eje desde cero y Vega validados.",
        "HTML: un H1, rutas relativas existentes y recursos del sitio presentes.",
        "Gráficos: anchura adaptable configurada para los contenedores.",
    ]


def main() -> None:
    for resultado in validar():
        print(f"Correcto: {resultado}")


if __name__ == "__main__":
    main()
