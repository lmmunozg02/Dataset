# Reglas de análisis

- Mantener todo el código, los nombres explicativos y la documentación del proyecto en español.
- No modificar ni eliminar el dataset original; conservar una copia verificable y documentar su hash SHA-256.
- Obtener todos los cálculos mediante scripts reproducibles de Python, utilizando pandas para procesar datos y Altair para las visualizaciones.
- No rellenar valores faltantes ni eliminar observaciones solo por ser valores atípicos. No alterar conteos originales sin justificación verificable y aprobación del estudiante.
- No inventar datos, fuentes, fechas, resultados ni referencias. Marcar explícitamente lo desconocido como pendiente de confirmación; no inferir el periodo a partir del nombre del archivo.
- Documentar inventario, decisiones, transformaciones, resultados, limitaciones y correcciones en los archivos correspondientes y en `bitacora/prompts.md`.
- Solicitar aprobación antes de cambios importantes y en los puntos de aprobación académicos definidos; no publicar, sincronizar ni crear commits sin autorización.
- No publicar información personal ni registros individuales sensibles. Los gráficos deben mostrar fuente y tamaño de muestra; porcentajes deben acompañarse de conteos; las barras deben comenzar en cero.
- No hacer afirmaciones causales ni generalizar más allá de los datos. No equiparar capturas con delitos, víctimas, denuncias o condenas, ni interpretar conteos mayores como mayor incidencia.
- Mantener los resultados exploratorios y descriptivos; no forzar análisis que el dataset no permita. Documentar las limitaciones de conteos absolutos frente a tasas poblacionales.
- Cada gráfico debe tener título, fuente, tamaño de muestra y etiquetas comprensibles; acompañar porcentajes con conteos y hacer que los ejes de barras partan de cero. Guardar visualizaciones interactivas como HTML.
- En las páginas públicas no incluir datos personales ni registros individuales sensibles. Comprobar enlaces y rutas relativas y solicitar autorización antes de publicar o sincronizar cambios.
- Verificar las salidas antes de declarar una etapa completada. Conservar archivos útiles y cambios preexistentes del repositorio.

# Alcance del proyecto analítico

El archivo inspeccionado contiene las columnas `Departamento` y `Recuento de Capturas_por_delitos_sexuales_contra_niños,_niñas_y_adolescentes_en_Colombia_20260825.csv`, con 33 filas y 33 territorios únicos. La primera columna es territorial, categórica nominal/geográfica; la segunda contiene conteos enteros, cuantitativos discretos. Este alcance queda sujeto a la verificación reproducible de carga y a la revisión del estudiante.

| Análisis | Aplica inicialmente | Pregunta | Variables y tipos | Visualización propuesta | Limitaciones |
|---|---|---|---|---|---|
| Distribución | Sí | ¿Cómo se distribuye el número de capturas entre los territorios observados? | Conteo de capturas; cuantitativa discreta. | Histograma interactivo con promedio y mediana si resulta legible. | Solo describe 33 conteos absolutos; no explica causas ni representa una tasa. |
| Ranking | Sí | ¿Qué territorios presentan mayores y menores registros de capturas? | Departamento (categórica nominal/geográfica) y conteo (cuantitativa discreta). | Barras horizontales ordenadas desde cero, con conteos y porcentajes. | El orden no equivale a riesgo o incidencia; los conteos dependen de factores no incluidos. |
| Relación | No | No aplica con las variables disponibles. | Solo hay una categoría territorial y un conteo; no hay dos medidas adecuadas de asociación. | No se propone. | No forzar un análisis de asociación. |
| Cambio en el tiempo | No | No puede evaluarse una evolución temporal con el archivo disponible. | No existe variable temporal documentada. | No se propone. | No inferir fechas a partir del encabezado. |
| Espacial | Sí, condicionado | ¿Cómo se distribuyen geográficamente los registros? | Departamento (categórica nominal/geográfica) y conteo (cuantitativa discreta). | Mapa coroplético interactivo solo con límites institucionales verificables y correspondencias resueltas. | Representa cantidades absolutas, no tasas ni riesgo. No asignar cero a territorios no emparejados; si la cartografía o correspondencia no se valida, usar barras por territorio. |

El alcance espacial no autoriza a inventar geometrías, coordenadas ni emparejamientos. Las denominaciones oficiales, la fuente cartográfica y cualquier correspondencia territorial deberán verificarse antes de aplicarse.
