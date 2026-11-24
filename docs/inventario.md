# Inventario de variables

Inventario generado a partir de `datos/crudo/capturas_colombia.csv`; las categorías se contrastaron con los tipos y valores observados.

| Nombre original | Nombre corto propuesto | Descripción | Tipo de variable | Valores válidos | Faltantes | Valores únicos | Tres ejemplos |
|---|---|---|---|---:|---:|---:|---|
| `Departamento` | `departamento` | Nombre del territorio consignado en el archivo. | Categórica nominal y geográfica | 33 | 0 | 33 | `VICHADA`, `VAUPÉS`, `VALLE` |
| `Recuento de Capturas_por_delitos_sexuales_contra_niños,_niñas_y_adolescentes_en_Colombia_20260825.csv` | `capturas` | Conteo de capturas registrado para cada territorio. | Cuantitativa discreta | 33 | 0 | 29 | `11`, `8`, `203` |

## Criterio de clasificación

La columna territorial se clasificó como categórica nominal/geográfica por contener nombres de territorios. La columna de capturas se clasificó como cuantitativa discreta porque la carga detectó valores enteros. El inventario no normaliza nombres ni modifica el dataset.

La fuente documental, el periodo de referencia y la metodología de recolección no están especificados en el archivo y permanecen pendientes de confirmación.

## Revisión del estudiante

Pendiente de aprobación antes de comenzar la limpieza.
