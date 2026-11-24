"""Calcula estadísticas descriptivas y exporta tablas agregadas reutilizables."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ_REPOSITORIO / "datos" / "limpio" / "capturas_colombia_limpio.csv"
DIRECTORIO_TABLAS = RAIZ_REPOSITORIO / "docs" / "tablas"
RUTA_INDICADORES_WEB = RAIZ_REPOSITORIO / "docs" / "data" / "indicadores.json"


def calcular_estadisticas(
    datos: pd.DataFrame,
) -> tuple[dict[str, object], pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if datos.empty or not {"departamento", "capturas"}.issubset(datos.columns):
        raise ValueError("Se requiere el dataset limpio con departamento y capturas.")
    capturas = datos["capturas"]
    total = int(capturas.sum())
    if total <= 0 or bool((capturas < 0).any()):
        raise ValueError("El total debe ser positivo y no debe haber conteos negativos.")

    q1 = float(capturas.quantile(0.25))
    q3 = float(capturas.quantile(0.75))
    rango_intercuartil = q3 - q1
    limite_inferior = q1 - 1.5 * rango_intercuartil
    limite_superior = q3 + 1.5 * rango_intercuartil

    ordenados = datos.sort_values(
        ["capturas", "departamento"],
        ascending=[False, True],
    ).reset_index(drop=True)
    participacion = ordenados[["departamento", "capturas"]].copy()
    participacion.insert(0, "posicion", range(1, len(participacion) + 1))
    participacion["participacion_porcentual"] = participacion["capturas"] / total * 100
    participacion["participacion_acumulada_porcentual"] = (
        participacion["participacion_porcentual"].cumsum()
    )

    concentraciones: list[dict[str, object]] = []
    for cantidad in (3, 5, 10):
        primeros = ordenados.head(cantidad)
        conteo = int(primeros["capturas"].sum())
        concentraciones.append(
            {
                "cantidad_territorios": cantidad,
                "capturas": conteo,
                "total_capturas": total,
                "participacion_porcentual": conteo / total * 100,
                "territorios": "; ".join(primeros["departamento"].tolist()),
            }
        )
    tabla_concentraciones = pd.DataFrame(concentraciones)

    mascara_atipicos = (capturas < limite_inferior) | (capturas > limite_superior)
    atipicos = datos.loc[mascara_atipicos, ["departamento", "capturas"]].copy()
    atipicos["limite_inferior_1_5_ric"] = limite_inferior
    atipicos["limite_superior_1_5_ric"] = limite_superior
    atipicos["criterio"] = "Valores fuera de Q1 - 1,5 × RIC o Q3 + 1,5 × RIC"

    valores_minimos = sorted(
        datos.loc[capturas.eq(capturas.min()), "departamento"].tolist()
    )
    valores_maximos = sorted(
        datos.loc[capturas.eq(capturas.max()), "departamento"].tolist()
    )
    estadisticas: dict[str, object] = {
        "total_capturas": total,
        "numero_territorios": int(datos["departamento"].nunique()),
        "tamano_muestra_territorios": int(len(datos)),
        "promedio_capturas_por_territorio": float(capturas.mean()),
        "mediana_capturas_por_territorio": float(capturas.median()),
        "minimo_capturas": int(capturas.min()),
        "territorios_minimo": valores_minimos,
        "maximo_capturas": int(capturas.max()),
        "territorios_maximo": valores_maximos,
        "rango_capturas": int(capturas.max() - capturas.min()),
        "desviacion_estandar_muestral": float(capturas.std(ddof=1)),
        "primer_cuartil": q1,
        "tercer_cuartil": q3,
        "rango_intercuartil": rango_intercuartil,
        "limite_inferior_1_5_ric": limite_inferior,
        "limite_superior_1_5_ric": limite_superior,
        "posibles_valores_atipicos": [
            {
                "departamento": str(fila.departamento),
                "capturas": int(fila.capturas),
            }
            for fila in atipicos.itertuples(index=False)
        ],
        "concentracion_top": {
            str(fila.cantidad_territorios): {
                "capturas": int(fila.capturas),
                "total_capturas": total,
                "participacion_porcentual": float(fila.participacion_porcentual),
            }
            for fila in tabla_concentraciones.itertuples(index=False)
        },
        "fuente": (
            "Archivo agregado suministrado por el estudiante; "
            "fuente original pendiente de confirmación."
        ),
    }

    filas_estadisticas = [
        ("Total de capturas registradas", total, "capturas"),
        ("Número de territorios analizados", estadisticas["numero_territorios"], "territorios"),
        ("Promedio por territorio", estadisticas["promedio_capturas_por_territorio"], "capturas"),
        ("Mediana por territorio", estadisticas["mediana_capturas_por_territorio"], "capturas"),
        ("Mínimo", estadisticas["minimo_capturas"], "capturas"),
        ("Máximo", estadisticas["maximo_capturas"], "capturas"),
        ("Rango", estadisticas["rango_capturas"], "capturas"),
        ("Desviación estándar muestral", estadisticas["desviacion_estandar_muestral"], "capturas"),
        ("Primer cuartil", q1, "capturas"),
        ("Tercer cuartil", q3, "capturas"),
        ("Rango intercuartílico", rango_intercuartil, "capturas"),
        ("Límite inferior 1,5 × RIC", limite_inferior, "capturas"),
        ("Límite superior 1,5 × RIC", limite_superior, "capturas"),
        ("Posibles valores atípicos identificados", len(atipicos), "territorios"),
    ]
    tabla_estadisticas = pd.DataFrame(
        filas_estadisticas,
        columns=["indicador", "valor", "unidad"],
    )
    return estadisticas, tabla_estadisticas, participacion, tabla_concentraciones, atipicos


def main() -> None:
    if not RUTA_DATOS.is_file():
        raise FileNotFoundError(f"No se encontró el dataset limpio: {RUTA_DATOS}")

    datos = pd.read_csv(RUTA_DATOS, sep=";", encoding="utf-8-sig")
    (
        estadisticas,
        tabla_estadisticas,
        participacion,
        concentraciones,
        atipicos,
    ) = calcular_estadisticas(datos)

    DIRECTORIO_TABLAS.mkdir(parents=True, exist_ok=True)
    RUTA_INDICADORES_WEB.parent.mkdir(parents=True, exist_ok=True)
    tabla_estadisticas.to_csv(
        DIRECTORIO_TABLAS / "estadisticas_descriptivas.csv",
        index=False,
        encoding="utf-8",
    )
    participacion.to_csv(
        DIRECTORIO_TABLAS / "participacion_territorial.csv",
        index=False,
        encoding="utf-8",
    )
    concentraciones.to_csv(
        DIRECTORIO_TABLAS / "concentracion_territorial.csv",
        index=False,
        encoding="utf-8",
    )
    atipicos.to_csv(
        DIRECTORIO_TABLAS / "posibles_valores_atipicos.csv",
        index=False,
        encoding="utf-8",
    )
    (DIRECTORIO_TABLAS / "estadisticas.json").write_text(
        json.dumps(estadisticas, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    indicadores_web = {
        "indicadores": estadisticas,
        "metadatos": {
            "fecha_generacion": date.today().isoformat(),
            "autor": None,
            "institucion": None,
            "periodo_referencia": None,
            "fuente_original": None,
            "registros_originales": int(len(datos)),
            "registros_finales": int(len(datos)),
            "unidad_observacion": "Territorio agregado",
            "variables": [
                {
                    "nombre": "departamento",
                    "tipo": "Categórica nominal y geográfica",
                },
                {
                    "nombre": "capturas",
                    "tipo": "Cuantitativa discreta",
                },
            ],
            "herramientas": ["Python", "pandas", "Altair", "Vega-Lite"],
        },
    }
    RUTA_INDICADORES_WEB.write_text(
        json.dumps(indicadores_web, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(tabla_estadisticas.to_string(index=False))
    print("\nConcentración acumulada:")
    print(concentraciones.to_string(index=False))
    print("\nPosibles valores atípicos (no eliminados):")
    print(atipicos.to_string(index=False) if not atipicos.empty else "Ninguno según 1,5 × RIC.")
    print(f"\nResultados guardados en: {DIRECTORIO_TABLAS.relative_to(RAIZ_REPOSITORIO)}")
    print(
        "Indicadores para el sitio: "
        f"{RUTA_INDICADORES_WEB.relative_to(RAIZ_REPOSITORIO)}"
    )


if __name__ == "__main__":
    main()
