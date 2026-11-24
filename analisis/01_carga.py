"""Carga y valida la estructura inicial del archivo de capturas."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ_REPOSITORIO / "datos" / "crudo" / "capturas_colombia.csv"
CODIFICACIONES = ("utf-8-sig", "cp1252")
SEPARADOR = ";"
FILAS_ESPERADAS = 33
COLUMNAS_ESPERADAS = 2


def cargar_csv(ruta: Path) -> tuple[pd.DataFrame, str, list[str]]:
    """Lee el CSV sin modificarlo y recurre a otra codificación solo si falla UTF-8."""
    errores_codificacion: list[str] = []
    for codificacion in CODIFICACIONES:
        try:
            datos = pd.read_csv(
                ruta,
                sep=SEPARADOR,
                encoding=codificacion,
                encoding_errors="strict",
            )
            return datos, codificacion, errores_codificacion
        except UnicodeDecodeError as error:
            errores_codificacion.append(f"{codificacion}: {error}")

    detalle = "\n".join(errores_codificacion)
    raise RuntimeError(f"No se pudo decodificar el archivo con las codificaciones previstas:\n{detalle}")


def validar_estructura(datos: pd.DataFrame) -> None:
    """Detiene el proceso si el esquema observado no cumple la estructura esperada."""
    territorios = datos.iloc[:, 0].nunique(dropna=True) if len(datos.columns) else 0
    problemas: list[str] = []

    if len(datos) != FILAS_ESPERADAS:
        problemas.append(f"filas observadas: {len(datos)}; esperadas: {FILAS_ESPERADAS}")
    if len(datos.columns) != COLUMNAS_ESPERADAS:
        problemas.append(
            f"columnas observadas: {len(datos.columns)}; esperadas: {COLUMNAS_ESPERADAS}"
        )
    if len(datos.columns) >= 1 and datos.columns[0] != "Departamento":
        problemas.append(f"primera columna observada: {datos.columns[0]!r}; esperada: 'Departamento'")
    if territorios != FILAS_ESPERADAS:
        problemas.append(
            f"territorios únicos observados: {territorios}; esperados: {FILAS_ESPERADAS}"
        )

    if problemas:
        raise ValueError("El CSV no cumple la estructura esperada:\n- " + "\n- ".join(problemas))


def main() -> None:
    if not RUTA_DATOS.is_file():
        raise FileNotFoundError(f"No se encontró el dataset copiado en: {RUTA_DATOS}")

    datos, codificacion, errores_codificacion = cargar_csv(RUTA_DATOS)
    print("=== Validación inicial del dataset ===")
    print(f"Archivo: {RUTA_DATOS.relative_to(RAIZ_REPOSITORIO)}")
    print(f"Filas de datos: {len(datos)}")
    print(f"Columnas: {len(datos.columns)}")
    print(f"Nombres exactos: {list(datos.columns)!r}")
    print("Primeras cinco filas:")
    print(datos.head().to_string(index=False))
    print("Tipos detectados:")
    print(datos.dtypes.to_string())
    print("Valores faltantes por columna:")
    print(datos.isna().sum().to_string())
    print(f"Filas duplicadas completas: {int(datos.duplicated().sum())}")
    print(f"Codificación utilizada: {codificacion}")
    print(
        "Problemas de codificación: "
        + ("ninguno" if not errores_codificacion else "; ".join(errores_codificacion))
    )
    print(f"Separador utilizado: {SEPARADOR!r}")
    print(f"Territorios únicos: {datos.iloc[:, 0].nunique(dropna=True)}")
    print(f"SHA-256: {hashlib.sha256(RUTA_DATOS.read_bytes()).hexdigest()}")

    validar_estructura(datos)
    print("Validación estructural: correcta.")


if __name__ == "__main__":
    main()
