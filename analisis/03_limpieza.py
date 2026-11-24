"""Valida, documenta y estandariza los datos territoriales sin alterar conteos."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
RUTA_ORIGINAL = RAIZ_REPOSITORIO / "datos" / "crudo" / "capturas_colombia.csv"
RUTA_LIMPIA = RAIZ_REPOSITORIO / "datos" / "limpio" / "capturas_colombia_limpio.csv"
RUTA_DOCUMENTACION = RAIZ_REPOSITORIO / "docs" / "limpieza.md"
SEPARADOR = ";"
CODIFICACION = "utf-8-sig"
SHA256_ORIGINAL_VERIFICADO = "f42f8deebaf51de8875ec395735d372e76d71eae6e994812683d376592a3036a"
FECHA_CONSULTA_FUENTE = "2026-11-24"
URL_FUENTE_OFICIAL = "https://www.datos.gov.co/d/vcjz-niiq"
FUENTE_OFICIAL = "DANE, DIVIPOLA - Códigos departamentos"

# Correspondencias comprobadas con los nombres publicados por DANE en DIVIPOLA.
NOMBRES_OFICIALES = {
    "AMAZONAS": "Amazonas",
    "ANTIOQUIA": "Antioquia",
    "ARAUCA": "Arauca",
    "ATLÁNTICO": "Atlántico",
    "BOGOTA": "Bogotá, D.C.",
    "BOLÍVAR": "Bolívar",
    "BOYACÁ": "Boyacá",
    "CALDAS": "Caldas",
    "CAQUETÁ": "Caquetá",
    "CASANARE": "Casanare",
    "CAUCA": "Cauca",
    "CESAR": "Cesar",
    "CHOCÓ": "Chocó",
    "CÓRDOBA": "Córdoba",
    "CUNDINAMARCA": "Cundinamarca",
    "GUAINÍA": "Guainía",
    "GUAJIRA": "La Guajira",
    "GUAVIARE": "Guaviare",
    "HUILA": "Huila",
    "MAGDALENA": "Magdalena",
    "META": "Meta",
    "NARIÑO": "Nariño",
    "NORTE DE SANTANDER": "Norte de Santander",
    "PUTUMAYO": "Putumayo",
    "QUINDÍO": "Quindío",
    "RISARALDA": "Risaralda",
    "SAN ANDRÉS": "Archipiélago de San Andrés, Providencia y Santa Catalina",
    "SANTANDER": "Santander",
    "SUCRE": "Sucre",
    "TOLIMA": "Tolima",
    "VALLE": "Valle del Cauca",
    "VAUPÉS": "Vaupés",
    "VICHADA": "Vichada",
}


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def validar_y_limpiar(datos: pd.DataFrame) -> tuple[pd.DataFrame, list[tuple[str, str]]]:
    if len(datos.columns) != 2:
        raise ValueError(f"Se esperaban 2 columnas; se encontraron {len(datos.columns)}.")
    if len(datos) != 33:
        raise ValueError(f"Se esperaban 33 filas; se encontraron {len(datos)}. No se modificaron datos.")

    filas_vacias = int(datos.isna().all(axis=1).sum())
    if filas_vacias:
        raise ValueError(
            f"Se encontraron {filas_vacias} filas completamente vacías; "
            "se detiene la limpieza sin eliminarlas."
        )

    faltantes = datos.isna().sum()
    if int(faltantes.sum()):
        raise ValueError(
            "Se encontraron valores faltantes; se detiene la limpieza sin imputarlos: "
            f"{faltantes.to_dict()}"
        )

    duplicados = int(datos.duplicated().sum())
    if duplicados:
        raise ValueError(
            f"Se encontraron {duplicados} filas duplicadas; se detiene la limpieza sin eliminarlas."
        )

    columna_territorio, columna_conteo = datos.columns
    if not pd.api.types.is_string_dtype(datos[columna_territorio].dtype):
        raise TypeError(
            f"La columna territorial debe ser texto; se detectó {datos[columna_territorio].dtype}."
        )
    if not pd.api.types.is_integer_dtype(datos[columna_conteo].dtype):
        raise TypeError(
            f"La columna de capturas debe ser entera; se detectó {datos[columna_conteo].dtype}."
        )
    if bool((datos[columna_conteo] < 0).any()):
        raise ValueError("Se encontraron conteos negativos; no se modificaron los datos.")

    nombres_originales = datos[columna_territorio]
    nombres_sin_espacios = nombres_originales.str.strip()
    if bool(nombres_sin_espacios.eq("").any()):
        raise ValueError("Se encontraron nombres territoriales vacíos; no se eliminarán.")

    claves = nombres_sin_espacios.str.upper()
    nombres_no_verificados = sorted(set(claves) - set(NOMBRES_OFICIALES))
    if nombres_no_verificados:
        raise ValueError(
            "Hay nombres sin correspondencia oficial verificada; no se normalizarán: "
            f"{nombres_no_verificados}"
        )

    nombres_normalizados = claves.map(NOMBRES_OFICIALES)
    if nombres_normalizados.duplicated().any():
        duplicados_normalizados = nombres_normalizados[
            nombres_normalizados.duplicated(keep=False)
        ].tolist()
        raise ValueError(
            "La normalización produciría territorios duplicados; no se fusionarán: "
            f"{duplicados_normalizados}"
        )

    correspondencias = list(zip(nombres_originales.tolist(), nombres_normalizados.tolist()))
    datos_limpios = datos.rename(
        columns={columna_territorio: "departamento", columna_conteo: "capturas"}
    ).copy()
    datos_limpios["departamento"] = nombres_normalizados.to_numpy()

    if not datos_limpios["capturas"].equals(datos[columna_conteo]):
        raise ValueError("Los conteos cambiaron durante la transformación; se cancela la salida.")
    if int(datos_limpios["capturas"].sum()) != int(datos[columna_conteo].sum()):
        raise ValueError("El total de capturas cambió durante la transformación.")

    return datos_limpios, correspondencias


def generar_documentacion(
    datos_originales: pd.DataFrame,
    datos_limpios: pd.DataFrame,
    correspondencias: list[tuple[str, str]],
    hash_antes: str,
    hash_despues: str,
) -> str:
    suma_original = int(datos_originales.iloc[:, 1].sum())
    suma_limpia = int(datos_limpios["capturas"].sum())
    filas_correspondencia = [
        f"| `{original}` | `{normalizado}` |"
        for original, normalizado in correspondencias
    ]

    lineas = [
        "# Limpieza y transformación",
        "",
        "## Validaciones",
        "",
        f"- Registros iniciales: {len(datos_originales)}.",
        f"- Registros finales: {len(datos_limpios)}.",
        "- Filas completamente vacías: 0.",
        "- Filas duplicadas completas: 0.",
        "- Nombres territoriales vacíos: 0.",
        "- Valores faltantes: 0 en las dos columnas.",
        "- Conteos no numéricos: 0; la columna se detectó como entera.",
        "- Conteos negativos: 0.",
        "- Filas eliminadas: 0; no se eliminaron observaciones.",
        "",
        "## Transformaciones",
        "",
        "- Columnas renombradas: `Departamento` → `departamento`; "
        "`Recuento de Capturas_por_delitos_sexuales_contra_niños,_niñas_y_adolescentes_en_Colombia_20260825.csv` → `capturas`.",
        "- Conteos conservados sin cambios.",
        "- Nombres territoriales estandarizados a denominaciones legibles basadas en DIVIPOLA. "
        "No se fusionaron Bogotá y Cundinamarca.",
        "",
        "## Correspondencias territoriales",
        "",
        f"Fuente consultada: [{FUENTE_OFICIAL}]({URL_FUENTE_OFICIAL}), "
        f"atribución DANE. Fecha de consulta: {FECHA_CONSULTA_FUENTE}. "
        "El catálogo identifica la cobertura como nacional y la licencia como "
        "Creative Commons Attribution-ShareAlike 4.0 International. "
        "Los nombres del CSV se contrastaron con el campo oficial `nombre_departamento`; "
        "la capitalización se presenta en formato legible.",
        "",
        "| Nombre original | Nombre normalizado |",
        "|---|---|",
        *filas_correspondencia,
        "",
        "## Conservación de registros y hashes",
        "",
        f"- Total original: {suma_original} capturas registradas.",
        f"- Total limpio: {suma_limpia} capturas registradas.",
        "- Cambios en conteos: ninguno.",
        f"- SHA-256 del archivo original antes: `{hash_antes}`.",
        f"- SHA-256 del archivo original después: `{hash_despues}`.",
        f"- Igualdad de hashes: {'sí' if hash_antes == hash_despues else 'no'}.",
        "",
    ]
    return "\n".join(lineas)


def main() -> None:
    if not RUTA_ORIGINAL.is_file():
        raise FileNotFoundError(f"No se encontró el archivo original: {RUTA_ORIGINAL}")
    hash_antes = sha256(RUTA_ORIGINAL)
    if hash_antes != SHA256_ORIGINAL_VERIFICADO:
        raise ValueError(
            "El hash del dataset original no coincide con el verificado en la etapa 3; "
            "se detiene la limpieza."
        )

    datos_originales = pd.read_csv(
        RUTA_ORIGINAL,
        sep=SEPARADOR,
        encoding=CODIFICACION,
        encoding_errors="strict",
    )
    datos_limpios, correspondencias = validar_y_limpiar(datos_originales)

    RUTA_LIMPIA.parent.mkdir(parents=True, exist_ok=True)
    if RUTA_LIMPIA.exists():
        datos_existentes = pd.read_csv(
            RUTA_LIMPIA,
            sep=SEPARADOR,
            encoding=CODIFICACION,
            encoding_errors="strict",
        )
        if not datos_existentes.equals(datos_limpios):
            raise FileExistsError(
                f"El archivo limpio existe y difiere del resultado esperado; "
                f"no se sobrescribirá: {RUTA_LIMPIA}"
            )
    else:
        datos_limpios.to_csv(
            RUTA_LIMPIA,
            sep=SEPARADOR,
            index=False,
            encoding=CODIFICACION,
        )

    datos_verificados = pd.read_csv(
        RUTA_LIMPIA,
        sep=SEPARADOR,
        encoding=CODIFICACION,
        encoding_errors="strict",
    )
    if not datos_verificados.equals(datos_limpios):
        raise ValueError("La lectura de control no coincide con el archivo limpio exportado.")

    hash_despues = sha256(RUTA_ORIGINAL)
    if hash_despues != hash_antes:
        raise ValueError("El hash del archivo original cambió durante la limpieza.")

    documentacion = generar_documentacion(
        datos_originales,
        datos_limpios,
        correspondencias,
        hash_antes,
        hash_despues,
    )
    RUTA_DOCUMENTACION.write_text(documentacion, encoding="utf-8")

    print(documentacion)
    print(f"Archivo limpio guardado en: {RUTA_LIMPIA.relative_to(RAIZ_REPOSITORIO)}")
    print(f"Documentación guardada en: {RUTA_DOCUMENTACION.relative_to(RAIZ_REPOSITORIO)}")


if __name__ == "__main__":
    main()
