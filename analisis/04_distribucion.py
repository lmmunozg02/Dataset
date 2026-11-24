"""Resume y grafica la distribución de capturas entre los territorios."""

from __future__ import annotations

import math
from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ_REPOSITORIO / "datos" / "limpio" / "capturas_colombia_limpio.csv"
RUTA_TABLA = RAIZ_REPOSITORIO / "docs" / "tablas" / "frecuencias_distribucion.csv"
RUTA_GRAFICO = RAIZ_REPOSITORIO / "docs" / "graficos" / "distribucion.html"
FUENTE = (
    "Fuente: archivo agregado suministrado por el estudiante; "
    "fuente original pendiente de confirmación."
)


def crear_intervalos(capturas: pd.Series) -> tuple[list[int], pd.DataFrame]:
    """Calcula intervalos contiguos desde cero con el criterio de Sturges."""
    numero_territorios = len(capturas)
    if numero_territorios == 0:
        raise ValueError("No hay territorios para construir la distribución.")
    if bool((capturas < 0).any()):
        raise ValueError("La variable contiene valores negativos; no se generará el histograma.")

    maximo = int(capturas.max())
    numero_intervalos = max(1, round(1 + math.log2(numero_territorios)))
    rango_desde_cero = maximo
    ancho = max(
        1,
        math.ceil((rango_desde_cero / numero_intervalos) / 10) * 10,
    )
    limite_superior = math.ceil((maximo + 1) / ancho) * ancho
    bordes = list(range(0, limite_superior + ancho, ancho))
    categorias = pd.cut(capturas, bins=bordes, right=False, include_lowest=True)
    frecuencias = categorias.value_counts(sort=False)

    tabla = pd.DataFrame(
        {
            "intervalo_desde": bordes[:-1],
            "intervalo_hasta": bordes[1:],
            "intervalo": [
                f"[{inicio}, {fin})"
                for inicio, fin in zip(bordes[:-1], bordes[1:])
            ],
            "territorios": frecuencias.to_numpy(dtype=int),
        }
    )
    return bordes, tabla


def crear_grafico(
    tabla: pd.DataFrame,
    promedio: float,
    mediana: float,
    numero_territorios: int,
    limite_superior: int,
) -> alt.TopLevelMixin:
    barras = (
        alt.Chart(tabla)
        .mark_bar(color="#315b7d", stroke="#ffffff", strokeWidth=1)
        .encode(
            x=alt.X(
                "intervalo_desde:Q",
                title="Número de capturas",
                scale=alt.Scale(domain=[0, limite_superior], nice=False),
                axis=alt.Axis(values=list(range(0, limite_superior + 1, 50))),
            ),
            x2=alt.X2("intervalo_hasta:Q"),
            y=alt.Y(
                "territorios:Q",
                title="Número de territorios",
                scale=alt.Scale(domainMin=0),
                axis=alt.Axis(tickMinStep=1),
            ),
            tooltip=[
                alt.Tooltip("intervalo:N", title="Intervalo de capturas"),
                alt.Tooltip("territorios:Q", title="Territorios", format="d"),
            ],
        )
        .properties(width=760, height=380)
    )

    referencias = pd.DataFrame(
        [
            {"medida": "Promedio", "valor": promedio},
            {"medida": "Mediana", "valor": mediana},
        ]
    )
    lineas = (
        alt.Chart(referencias)
        .mark_rule(strokeDash=[5, 4], strokeWidth=2)
        .encode(
            x=alt.X("valor:Q"),
            color=alt.Color(
                "medida:N",
                title="Referencia",
                scale=alt.Scale(
                    domain=["Promedio", "Mediana"],
                    range=["#d17a22", "#6a4c93"],
                ),
            ),
            tooltip=[
                alt.Tooltip("medida:N", title="Medida"),
                alt.Tooltip("valor:Q", title="Capturas", format=".2f"),
            ],
        )
    )

    grafico = (barras + lineas).properties(
        title=alt.TitleParams(
            text="¿Cómo se distribuye el número de capturas entre los territorios de Colombia?",
            subtitle=f"Histograma de conteos agregados · n = {numero_territorios} territorios",
            anchor="start",
        )
    )
    pie = (
        alt.Chart(pd.DataFrame({"fuente": [f"{FUENTE}  Intervalos calculados con Sturges."]}))
        .mark_text(align="left", fontSize=11, color="#4b5563")
        .encode(text="fuente:N")
        .properties(width=760, height=28)
    )
    return (
        alt.vconcat(grafico, pie, spacing=8)
        .configure_axis(labelFont="Arial", titleFont="Arial", gridColor="#e5e7eb")
        .configure_legend(labelFont="Arial", titleFont="Arial")
        .configure_view(stroke=None)
    )


def main() -> None:
    if not RUTA_DATOS.is_file():
        raise FileNotFoundError(f"No se encontró el dataset limpio: {RUTA_DATOS}")

    datos = pd.read_csv(RUTA_DATOS, sep=";", encoding="utf-8-sig")
    if not {"departamento", "capturas"}.issubset(datos.columns):
        raise ValueError("El dataset limpio no tiene las columnas esperadas.")

    bordes, tabla = crear_intervalos(datos["capturas"])
    RUTA_TABLA.parent.mkdir(parents=True, exist_ok=True)
    RUTA_GRAFICO.parent.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(RUTA_TABLA, index=False, encoding="utf-8")

    grafico = crear_grafico(
        tabla=tabla,
        promedio=float(datos["capturas"].mean()),
        mediana=float(datos["capturas"].median()),
        numero_territorios=len(datos),
        limite_superior=bordes[-1],
    )
    grafico.save(RUTA_GRAFICO)

    print(
        f"Histograma creado para {len(datos)} territorios con {len(tabla)} intervalos "
        f"de ancho {bordes[1] - bordes[0]}."
    )
    print(tabla.to_string(index=False))
    print(f"Tabla: {RUTA_TABLA.relative_to(RAIZ_REPOSITORIO)}")
    print(f"Gráfico: {RUTA_GRAFICO.relative_to(RAIZ_REPOSITORIO)}")


if __name__ == "__main__":
    main()
