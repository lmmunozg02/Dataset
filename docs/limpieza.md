# Limpieza y transformación

## Validaciones

- Registros iniciales: 33.
- Registros finales: 33.
- Filas completamente vacías: 0.
- Filas duplicadas completas: 0.
- Nombres territoriales vacíos: 0.
- Valores faltantes: 0 en las dos columnas.
- Conteos no numéricos: 0; la columna se detectó como entera.
- Conteos negativos: 0.
- Filas eliminadas: 0; no se eliminaron observaciones.

## Transformaciones

- Columnas renombradas: `Departamento` → `departamento`; `Recuento de Capturas_por_delitos_sexuales_contra_niños,_niñas_y_adolescentes_en_Colombia_20260825.csv` → `capturas`.
- Conteos conservados sin cambios.
- Nombres territoriales estandarizados a denominaciones legibles basadas en DIVIPOLA. No se fusionaron Bogotá y Cundinamarca.

## Correspondencias territoriales

Fuente consultada: [DANE, DIVIPOLA - Códigos departamentos](https://www.datos.gov.co/d/vcjz-niiq), atribución DANE. Fecha de consulta: 2026-11-24. El catálogo identifica la cobertura como nacional y la licencia como Creative Commons Attribution-ShareAlike 4.0 International. Los nombres del CSV se contrastaron con el campo oficial `nombre_departamento`; la capitalización se presenta en formato legible.

| Nombre original | Nombre normalizado |
|---|---|
| `VICHADA` | `Vichada` |
| `VAUPÉS` | `Vaupés` |
| `VALLE` | `Valle del Cauca` |
| `TOLIMA` | `Tolima` |
| `SUCRE` | `Sucre` |
| `SANTANDER` | `Santander` |
| `SAN ANDRÉS` | `Archipiélago de San Andrés, Providencia y Santa Catalina` |
| `RISARALDA` | `Risaralda` |
| `QUINDÍO` | `Quindío` |
| `PUTUMAYO` | `Putumayo` |
| `NORTE DE SANTANDER` | `Norte de Santander` |
| `NARIÑO` | `Nariño` |
| `META` | `Meta` |
| `MAGDALENA` | `Magdalena` |
| `HUILA` | `Huila` |
| `GUAVIARE` | `Guaviare` |
| `GUAJIRA` | `La Guajira` |
| `GUAINÍA` | `Guainía` |
| `CUNDINAMARCA` | `Cundinamarca` |
| `CÓRDOBA` | `Córdoba` |
| `CHOCÓ` | `Chocó` |
| `CESAR` | `Cesar` |
| `CAUCA` | `Cauca` |
| `CASANARE` | `Casanare` |
| `CAQUETÁ` | `Caquetá` |
| `CALDAS` | `Caldas` |
| `BOYACÁ` | `Boyacá` |
| `BOLÍVAR` | `Bolívar` |
| `BOGOTA` | `Bogotá, D.C.` |
| `ATLÁNTICO` | `Atlántico` |
| `ARAUCA` | `Arauca` |
| `ANTIOQUIA` | `Antioquia` |
| `AMAZONAS` | `Amazonas` |

## Conservación de registros y hashes

- Total original: 2221 capturas registradas.
- Total limpio: 2221 capturas registradas.
- Cambios en conteos: ninguno.
- SHA-256 del archivo original antes: `f42f8deebaf51de8875ec395735d372e76d71eae6e994812683d376592a3036a`.
- SHA-256 del archivo original después: `f42f8deebaf51de8875ec395735d372e76d71eae6e994812683d376592a3036a`.
- Igualdad de hashes: sí.
