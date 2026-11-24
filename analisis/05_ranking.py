"""Construye el ranking territorial interactivo de capturas registradas."""

from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ_REPOSITORIO / "datos" / "limpio" / "capturas_colombia_limpio.csv"
RUTA_TABLA = RAIZ_REPOSITORIO / "docs" / "tablas" / "ranking_territorial.csv"
RUTA_GRAFICO = RAIZ_REPOSITORIO / "docs" / "graficos" / "ranking.html"
FUENTE = (
    "Fuente: archivo agregado suministrado por el estudiante; "
    "fuente original pendiente de confirmación."
)


def crear_grafico(ranking: pd.DataFrame) -> alt.TopLevelMixin:
    seleccion = alt.selection_point(
        fields=["departamento"],
        on="click",
        clear="dblclick",
        empty=True,
    )
    colores = alt.condition(
        seleccion,
        alt.value("#1f5a85"),
        alt.value("#b7c8d6"),
    )
    dominio_x = [0, float(ranking["capturas"].max()) * 1.32]
    barras = (
        alt.Chart(ranking)
        .mark_bar()
        .encode(
            y=alt.Y(
                "departamento:N",
                title="Territorio",
                sort=alt.SortField(field="posicion", order="ascending"),
                axis=alt.Axis(labelLimit=330),
            ),
            x=alt.X(
                "capturas:Q",
                title="Capturas registradas",
                scale=alt.Scale(domain=dominio_x, nice=False),
            ),
            color=colores,
            tooltip=[
                alt.Tooltip("departamento:N", title="Territorio"),
                alt.Tooltip("posicion:Q", title="Posición", format="d"),
                alt.Tooltip("capturas:Q", title="Capturas", format="d"),
                alt.Tooltip("participacion_porcentual:Q", title="Participación (%)", format=".2f"),
            ],
        )
        .add_params(seleccion)
        .properties(width=760, height=820)
    )
    etiquetas = (
        alt.Chart(ranking)
        .mark_text(align="left", baseline="middle", dx=4, fontSize=10, color="#263746")
        .encode(
            y=alt.Y(
                "departamento:N",
                sort=alt.SortField(field="posicion", order="ascending"),
            ),
            x=alt.X("capturas:Q", scale=alt.Scale(domain=dominio_x, nice=False)),
            text="etiqueta:N",
        )
    )
    grafico = (barras + etiquetas).properties(
        title=alt.TitleParams(
            text="¿Qué departamentos presentan los mayores y menores registros de capturas?",
            subtitle=f"Ranking descendente · n = {len(ranking)} territorios",
            anchor="start",
        )
    )
    pie = (
        alt.Chart(pd.DataFrame({"fuente": [f"{FUENTE}  Selecciona una barra para resaltarla; doble clic para limpiar."]}))
        .mark_text(align="left", fontSize=11, color="#4b5563")
        .encode(text="fuente:N")
        .properties(width=760, height=28)
    )
    return (
        alt.vconcat(grafico, pie, spacing=8)
        .configure_axis(labelFont="Arial", titleFont="Arial", gridColor="#e5e7eb")
        .configure_view(stroke=None)
    )


def main() -> None:
    if not RUTA_DATOS.is_file():
        raise FileNotFoundError(f"No se encontró el dataset limpio: {RUTA_DATOS}")

    datos = pd.read_csv(RUTA_DATOS, sep=";", encoding="utf-8-sig")
    if not {"departamento", "capturas"}.issubset(datos.columns):
        raise ValueError("El dataset limpio no tiene las columnas esperadas.")
    total = int(datos["capturas"].sum())
    if total <= 0:
        raise ValueError("El total de capturas debe ser mayor que cero.")

    ranking = datos.sort_values(
        ["capturas", "departamento"],
        ascending=[False, True],
    ).reset_index(drop=True)
    ranking.insert(0, "posicion", range(1, len(ranking) + 1))
    ranking["participacion_porcentual"] = ranking["capturas"] / total * 100
    ranking["participacion_acumulada_porcentual"] = (
        ranking["participacion_porcentual"].cumsum()
    )
    ranking["etiqueta"] = ranking.apply(
        lambda fila: f"{int(fila['capturas'])} · {fila['participacion_porcentual']:.1f} %",
        axis=1,
    )

    RUTA_TABLA.parent.mkdir(parents=True, exist_ok=True)
    RUTA_GRAFICO.parent.mkdir(parents=True, exist_ok=True)
    ranking.drop(columns="etiqueta").to_csv(RUTA_TABLA, index=False, encoding="utf-8")
    crear_grafico(ranking).save(RUTA_GRAFICO)

    print(f"Territorios incluidos: {len(ranking)}")
    print("Cinco primeros:")
    print(ranking.head(5)[["posicion", "departamento", "capturas", "participacion_porcentual"]].to_string(index=False))
    print("Cinco últimos:")
    print(ranking.tail(5)[["posicion", "departamento", "capturas", "participacion_porcentual"]].to_string(index=False))
    print(f"Tabla: {RUTA_TABLA.relative_to(RAIZ_REPOSITORIO)}")
    print(f"Gráfico: {RUTA_GRAFICO.relative_to(RAIZ_REPOSITORIO)}")


if __name__ == "__main__":
    main()
