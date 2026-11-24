"""Genera un inventario verificable de las variables del CSV original."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ_REPOSITORIO / "datos" / "crudo" / "capturas_colombia.csv"
RUTA_SALIDA = RAIZ_REPOSITORIO / "docs" / "inventario.md"


def clasificar_variable(datos: pd.DataFrame, posicion: int) -> tuple[str, str, str]:
    """Clasifica cada columna únicamente si su contenido respalda la categoría."""
    nombre = datos.columns[posicion]

    if posicion == 0:
        if not pd.api.types.is_string_dtype(datos[nombre].dtype):
            raise TypeError(
                f"La variable territorial {nombre!r} no tiene un tipo de texto esperado: "
                f"{datos[nombre].dtype}"
            )
        return (
            "departamento",
            "Nombre del territorio consignado en el archivo.",
            "Categórica nominal y geográfica",
        )

    if posicion == 1:
        if not pd.api.types.is_integer_dtype(datos[nombre].dtype):
            raise TypeError(
                f"La variable de capturas {nombre!r} no tiene un tipo entero esperado: "
                f"{datos[nombre].dtype}"
            )
        return (
            "capturas",
            "Conteo de capturas registrado para cada territorio.",
            "Cuantitativa discreta",
        )

    raise ValueError(f"No se definió clasificación para la columna {nombre!r}.")


def valor_markdown(valor: object) -> str:
    """Representa ejemplos de forma legible y segura dentro de una tabla Markdown."""
    texto = str(valor).replace("|", r"\|").replace("\n", " ")
    return f"`{texto}`"


def generar_inventario(datos: pd.DataFrame) -> str:
    if len(datos.columns) != 2:
        raise ValueError(
            f"Se esperaban 2 variables para el inventario; se encontraron {len(datos.columns)}."
        )

    filas = [
        "# Inventario de variables",
        "",
        "Inventario generado a partir de `datos/crudo/capturas_colombia.csv`; "
        "las categorías se contrastaron con los tipos y valores observados.",
        "",
        "| Nombre original | Nombre corto propuesto | Descripción | Tipo de variable | Valores válidos | Faltantes | Valores únicos | Tres ejemplos |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]

    for posicion, nombre in enumerate(datos.columns):
        nombre_corto, descripcion, tipo = clasificar_variable(datos, posicion)
        columna = datos[nombre]
        ejemplos = columna.dropna().drop_duplicates().head(3).tolist()
        ejemplos_md = ", ".join(valor_markdown(valor) for valor in ejemplos)
        filas.append(
            f"| `{nombre}` | `{nombre_corto}` | {descripcion} | {tipo} | "
            f"{int(columna.count())} | {int(columna.isna().sum())} | "
            f"{int(columna.nunique(dropna=True))} | {ejemplos_md} |"
        )

    filas.extend(
        [
            "",
            "## Criterio de clasificación",
            "",
            "La columna territorial se clasificó como categórica nominal/geográfica por "
            "contener nombres de territorios. La columna de capturas se clasificó como "
            "cuantitativa discreta porque la carga detectó valores enteros. El inventario "
            "no normaliza nombres ni modifica el dataset.",
            "",
            "La fuente documental, el periodo de referencia y la metodología de recolección "
            "no están especificados en el archivo y permanecen pendientes de confirmación.",
            "",
            "## Revisión del estudiante",
            "",
            "Pendiente de aprobación antes de comenzar la limpieza.",
            "",
        ]
    )
    return "\n".join(filas)


def main() -> None:
    if not RUTA_DATOS.is_file():
        raise FileNotFoundError(f"No se encontró el dataset original copiado: {RUTA_DATOS}")

    datos = pd.read_csv(RUTA_DATOS, sep=";", encoding="utf-8-sig", encoding_errors="strict")
    inventario = generar_inventario(datos)
    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    RUTA_SALIDA.write_text(inventario, encoding="utf-8")
    print(inventario)
    print(f"\nInventario guardado en: {RUTA_SALIDA.relative_to(RAIZ_REPOSITORIO)}")


if __name__ == "__main__":
    main()
