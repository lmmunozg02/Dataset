"""Documenta el límite cartográfico y genera la alternativa territorial aprobada."""

from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ_REPOSITORIO / "datos" / "limpio" / "capturas_colombia_limpio.csv"
RUTA_TABLA = RAIZ_REPOSITORIO / "docs" / "tablas" / "alternativa_espacial.csv"
RUTA_GRAFICO = RAIZ_REPOSITORIO / "docs" / "graficos" / "espacial.html"
RUTA_DOCUMENTACION = RAIZ_REPOSITORIO / "docs" / "espacial.md"
FECHA_CONSULTA = "2026-11-24"
FUENTE = "DANE, Marco Geoestadístico Nacional MGN integrado, versión 2025 — capa Departamento."
URL_FICHA = "https://www.datos.gov.co/d/i443-az6j"
URL_GEOJSON = (
    "https://cdge.dane.gov.co/api/download/v1/items/"
    "798ecd3194794ed69653ea3f948a9f4b/geojson?layers=319"
)
URL_SERVICIO = (
    "https://portalgis.dane.gov.co/mparcgis/rest/services/"
    "MGN2025/Serv_CapasMGN_2025/MapServer/319"
)
FUENTE_CONTEOS = (
    "Fuente: archivo agregado suministrado por el estudiante; "
    "fuente original pendiente de confirmación."
)


def crear_grafico(datos: pd.DataFrame) -> alt.TopLevelMixin:
    seleccion = alt.selection_point(
        fields=["departamento"],
        on="click",
        clear="dblclick",
        empty=True,
    )
    barras = (
        alt.Chart(datos)
        .mark_bar()
        .encode(
            y=alt.Y(
                "departamento:N",
                title="Territorio (orden alfabético)",
                sort=alt.SortField(field="departamento", order="ascending"),
                axis=alt.Axis(labelLimit=420),
            ),
            x=alt.X(
                "capturas:Q",
                title="Capturas registradas (conteos absolutos)",
                scale=alt.Scale(
                    domain=[0, float(datos["capturas"].max()) * 1.32],
                    nice=False,
                ),
            ),
            color=alt.condition(
                seleccion,
                alt.value("#1f5a85"),
                alt.value("#b7c8d6"),
            ),
            tooltip=[
                alt.Tooltip("departamento:N", title="Territorio"),
                alt.Tooltip("capturas:Q", title="Capturas", format="d"),
                alt.Tooltip(
                    "participacion_porcentual:Q",
                    title="Participación (%)",
                    format=".2f",
                ),
                alt.Tooltip(
                    "nota:N",
                    title="Alcance",
                ),
            ],
        )
        .add_params(seleccion)
        .properties(width=760, height=820)
    )
    etiquetas = (
        alt.Chart(datos)
        .mark_text(align="left", baseline="middle", dx=4, fontSize=10, color="#263746")
        .encode(
            y=alt.Y(
                "departamento:N",
                sort=alt.SortField(field="departamento", order="ascending"),
            ),
            x=alt.X(
                "capturas:Q",
                scale=alt.Scale(
                    domain=[0, float(datos["capturas"].max()) * 1.32],
                    nice=False,
                ),
            ),
            text="etiqueta:N",
        )
    )
    grafico = (barras + etiquetas).properties(
        title=alt.TitleParams(
            text="¿Cómo se distribuyen geográficamente las capturas registradas en Colombia?",
            subtitle=(
                "Alternativa en barras, no es un mapa ni representa tasas poblacionales o riesgo · "
                f"n = {len(datos)} territorios"
            ),
            anchor="start",
        )
    )
    pie = (
        alt.Chart(
            pd.DataFrame(
                {
                    "fuente": [
                        f"{FUENTE_CONTEOS}  Límites geográficos DANE no disponibles localmente."
                    ]
                }
            )
        )
        .mark_text(align="left", fontSize=11, color="#4b5563")
        .encode(text="fuente:N")
        .properties(width=760, height=28)
    )
    return (
        alt.vconcat(grafico, pie, spacing=8)
        .configure_axis(labelFont="Arial", titleFont="Arial", gridColor="#e5e7eb")
        .configure_view(stroke=None)
    )


def generar_documentacion(territorios: list[str]) -> str:
    lista_territorios = "\n".join(f"- {nombre}" for nombre in territorios)
    return "\n".join(
        [
            "# Análisis espacial: limitación de la capa geográfica",
            "",
            "## Fuente cartográfica consultada",
            "",
            f"- **Fuente:** [{FUENTE}]({URL_FICHA}), atribución DANE.",
            f"- **URL GeoJSON anunciada en el catálogo:** {URL_GEOJSON}",
            f"- **Servicio de mapas:** {URL_SERVICIO}",
            f"- **Fecha de consulta:** {FECHA_CONSULTA}.",
            "- **Cobertura:** capa departamental del MGN 2025 con cobertura nacional; "
            "la ficha publica una extensión aproximada de "
            "`-81.7356,-4.2294,-66.8472,13.3947`.",
            "- **Licencia:** no declarada en los metadatos consultados.",
            "",
            "## Resultado de la verificación",
            "",
            "La URL de descarga oficial respondió que las descargas no están soportadas para "
            "este elemento (`400: Downloads are not supported for this item`). El endpoint del "
            "servicio geográfico no pudo consultarse desde este entorno por errores de conexión "
            "TLS/timeout. Por ello, no se descargó ni guardó un GeoJSON, no se inventaron límites "
            "y no se asignaron valores a geometrías sin correspondencia.",
            "",
            "No fue posible comprobar correspondencias entre geometrías y los 33 nombres "
            "normalizados. Por tanto, todos quedan **sin correspondencia geográfica verificable** "
            "en esta etapa (no significa que no exista una geometría correspondiente):",
            "",
            lista_territorios,
            "",
            "## Alternativa aprobada",
            "",
            "Se presenta un gráfico interactivo de barras por territorio, ordenado "
            "alfabéticamente, con conteos y participación porcentual. Es una alternativa "
            "descriptiva y no un mapa; repite la variable territorial del ranking. Los conteos "
            "son absolutos: no son tasas poblacionales ni niveles de riesgo.",
            "",
            f"El gráfico y la tabla se generaron desde el dataset limpio. Fuente de los conteos: "
            f"{FUENTE_CONTEOS} Tamaño de muestra: {len(territorios)} territorios.",
            "",
        ]
    )


def main() -> None:
    if not RUTA_DATOS.is_file():
        raise FileNotFoundError(f"No se encontró el dataset limpio: {RUTA_DATOS}")

    datos = pd.read_csv(RUTA_DATOS, sep=";", encoding="utf-8-sig")
    if not {"departamento", "capturas"}.issubset(datos.columns):
        raise ValueError("El dataset limpio no tiene las columnas esperadas.")
    if bool((datos["capturas"] < 0).any()):
        raise ValueError("Se encontraron conteos negativos; no se generará la alternativa.")

    total = int(datos["capturas"].sum())
    if total <= 0:
        raise ValueError("El total de capturas debe ser mayor que cero.")

    alternativa = datos[["departamento", "capturas"]].sort_values(
        "departamento",
        ascending=True,
    ).reset_index(drop=True)
    alternativa["participacion_porcentual"] = alternativa["capturas"] / total * 100
    alternativa["etiqueta"] = alternativa.apply(
        lambda fila: f"{int(fila['capturas'])} · {fila['participacion_porcentual']:.1f} %",
        axis=1,
    )
    alternativa["nota"] = "Alternativa en barras; no es un mapa ni una tasa."

    RUTA_TABLA.parent.mkdir(parents=True, exist_ok=True)
    RUTA_GRAFICO.parent.mkdir(parents=True, exist_ok=True)
    RUTA_TABLA.write_text(
        alternativa.drop(columns=["etiqueta", "nota"]).to_csv(index=False),
        encoding="utf-8",
    )
    crear_grafico(alternativa).save(RUTA_GRAFICO)
    RUTA_DOCUMENTACION.write_text(
        generar_documentacion(alternativa["departamento"].tolist()),
        encoding="utf-8",
    )

    print(f"Alternativa territorial creada para {len(alternativa)} territorios.")
    print("No se creó mapa porque no se pudo descargar/verificar la capa de geometrías.")
    print(f"Gráfico: {RUTA_GRAFICO.relative_to(RAIZ_REPOSITORIO)}")
    print(f"Tabla: {RUTA_TABLA.relative_to(RAIZ_REPOSITORIO)}")
    print(f"Documentación: {RUTA_DOCUMENTACION.relative_to(RAIZ_REPOSITORIO)}")


if __name__ == "__main__":
    main()
