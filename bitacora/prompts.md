# Bitácora del uso de inteligencia artificial

## 2026-11-24 — Instrucción maestra del proyecto

- **Etapa:** definición del proyecto y etapas 1–3.
- **Prompt utilizado:** solicitud maestra del estudiante para construir un análisis exploratorio reproducible de la geografía de las capturas por delitos sexuales contra NNA en Colombia, con las siete etapas, reglas de integridad, documentación, aprobación, análisis, visualizaciones, página y publicación especificadas en su mensaje inicial.
- **Qué hizo el agente:** inspeccionó el repositorio y el entorno; identificó el CSV, verificó su estructura preliminar y solicitó autorización antes de cambios. Tras recibir autorización para las etapas 2 y 3, creó estructura y documentación iniciales y preparó la validación reproducible de carga.
- **Archivos creados o modificados:** README.md, AGENTS.md, requirements.txt, .gitignore, analisis/01_carga.py, datos/crudo/capturas_colombia.csv, marcadores .gitkeep y esta bitácora.
- **Resultados:** autorización recibida para las etapas 2 y 3. Se verificaron 33 filas, 2 columnas, 33 territorios únicos, cero valores faltantes y cero filas duplicadas; las columnas se detectaron como texto y entero. El CSV usa `;` y `utf-8-sig`; no se observaron problemas de codificación. SHA-256 antes y después de copiar: `f42f8deebaf51de8875ec395735d372e76d71eae6e994812683d376592a3036a`. Python 3.14.2, pandas 3.1.1 y Altair 6.3.0.
- **Errores encontrados:** pandas y Altair no estaban instalados al inspeccionar el entorno; ambos se instalaron desde `requirements.txt`. La carga y validación concluyeron correctamente. No se registraron correcciones del estudiante.
- **Correcciones solicitadas por el estudiante:** ninguna.
- **Decisiones:** separar por `;`, intentar primero `utf-8-sig` y conservar el CSV original; documentar referencias desconocidas como pendientes. El alcance se limita a distribución, ranking y análisis espacial condicionado, con base en el esquema observado.
- **Aprobaciones:** el estudiante autorizó iniciar las etapas 2 y 3; no se solicitó ni se recibió aprobación para etapas posteriores.
- **Estado de verificación:** etapas 2 y 3 verificadas; copia byte por byte coincidente, script de carga ejecutado y validación estructural correcta. Etapas posteriores pendientes de autorización.

## 2026-11-24 — Etapa 4: inventario de variables

- **Prompt utilizado:** autorización del estudiante para iniciar únicamente el inventario de la etapa 4; presentar el inventario para su aprobación y detenerse antes de la limpieza.
- **Qué hizo el agente:** creó y ejecutó un script reproducible que inventaría las variables del CSV original, verifica que los tipos observados respalden la clasificación y genera la tabla en Markdown.
- **Archivos creados o modificados:** `analisis/02_inventario.py`, `docs/inventario.md` y `README.md`.
- **Resultados:** 2 variables inventariadas con 33 valores válidos y 0 faltantes cada una. `Departamento`: categórica nominal/geográfica, 33 valores únicos; ejemplos `VICHADA`, `VAUPÉS`, `VALLE`. Conteo: cuantitativa discreta, 29 valores únicos; ejemplos `11`, `8`, `203`.
- **Errores encontrados:** ninguno.
- **Correcciones solicitadas por el estudiante:** ninguna.
- **Decisiones:** no normalizar nombres ni modificar datos en el inventario. La limpieza queda detenida hasta que el estudiante apruebe el inventario y, posteriormente, el plan detallado de limpieza.
- **Aprobaciones:** el estudiante aprobó el inventario y luego aprobó el plan de limpieza antes de la creación del script.
- **Estado de verificación:** script ejecutado correctamente y `docs/inventario.md` generado. La limpieza se realizó después de la aprobación separada del plan.

## 2026-11-24 — Limpieza de datos

- **Prompt utilizado:** aprobación del estudiante para ejecutar el plan detallado de limpieza, con la condición de detenerse ante anomalías o correspondencias oficiales no verificables.
- **Qué hizo el agente:** verificó las denominaciones territoriales con el conjunto DIVIPOLA de DANE en Datos Abiertos, aplicó correspondencias explícitas, conservó los conteos y generó el CSV limpio y su documentación.
- **Archivos creados o modificados:** `analisis/03_limpieza.py`, `datos/limpio/capturas_colombia_limpio.csv`, `docs/limpieza.md`, `README.md` y esta bitácora.
- **Resultados:** 33 registros iniciales y finales; 0 filas vacías, duplicadas o eliminadas; 0 valores faltantes, no numéricos o negativos. Se renombraron las dos columnas, se normalizaron las 33 denominaciones territoriales con correspondencias documentadas y se conservaron los 2.221 conteos agregados. El SHA-256 del CSV original antes y después permaneció idéntico: `f42f8deebaf51de8875ec395735d372e76d71eae6e994812683d376592a3036a`.
- **Errores encontrados:** una URL antigua de consulta inicial devolvió 404; se localizó el recurso oficial actual de DIVIPOLA y se verificó la lista completa de departamentos antes de aplicar equivalencias. La ejecución aprobada finalizó correctamente.
- **Corrección técnica del agente:** para permitir reproducir el orden documentado, el script acepta una salida limpia existente solo si coincide exactamente con la transformación esperada; si difiere, se detiene sin sobrescribirla.
- **Correcciones solicitadas por el estudiante:** ninguna.
- **Decisiones:** utilizar las denominaciones basadas en `nombre_departamento` del DANE; Bogotá permanece separada de Cundinamarca. No imputar, eliminar ni alterar conteos.
- **Aprobaciones:** inventario y plan de limpieza aprobados por el estudiante antes de escribir y ejecutar `03_limpieza.py`.
- **Estado de verificación:** script ejecutado correctamente; CSV limpio leído de vuelta y validado, documentación generada, totales y hash del original conservados. Etapa 4 completada.

## 2026-11-24 — Etapa 5: estadísticas y visualizaciones (avance)

- **Prompt utilizado:** autorización del estudiante para iniciar análisis estadístico, distribución, ranking y análisis espacial, con la condición de documentar o detener cualquier limitación cartográfica no resuelta.
- **Qué hizo el agente:** generó estadísticas agregadas, tablas de participación y concentración, un histograma interactivo con seis intervalos de 50 capturas (criterio de Sturges) y un ranking interactivo para los 33 territorios.
- **Archivos creados:** `analisis/04_distribucion.py`, `analisis/05_ranking.py`, `analisis/07_estadisticas.py`, dos HTML de gráficos y tablas agregadas en `docs/tablas/`.
- **Resultados verificados:** 2.221 capturas en 33 territorios; promedio 67,30, mediana 47, Q1 29, Q3 80, RIC 51, desviación estándar muestral 66,84, mínimo 4, máximo 286 y rango 282. Tres posibles valores atípicos según 1,5 × RIC (no eliminados). Participación de los tres primeros: 744 (33,50 %); cinco primeros: 996 (44,84 %); diez primeros: 1.397 (62,90 %).
- **Errores encontrados:** la fuente DANE MGN 2025 se identificó como oficial, pero su API de descarga de GeoJSON respondió que las descargas no están soportadas para el elemento; el endpoint de servicio geográfico tampoco fue accesible desde el entorno (fallo TLS/timeout). No se descargó ni guardó geometría. Una primera aserción de QA buscaba títulos Unicode sin considerar el escape `\\u` en el JSON del HTML; se corrigió la comprobación para leer la especificación Vega, y la validación pasó.
- **Correcciones solicitadas por el estudiante:** ninguna.
- **Decisiones:** no inventar límites ni sustituir unilateralmente el mapa. El estudiante aprobó barras territoriales como alternativa espacial antes de crear `06_espacial.py`.
- **Aprobaciones:** el estudiante autorizó iniciar la etapa 5 y posteriormente aprobó barras por territorio como alternativa sin mapa.
- **Estado de verificación:** los scripts 01–07 se ejecutaron en el orden del README; tablas, porcentajes y tres especificaciones HTML de Altair se validaron automáticamente. La revisión visual en navegador queda pendiente para la etapa 7.

## 2026-11-24 — Etapa 5: alternativa espacial aprobada

- **Prompt utilizado:** elección del estudiante de barras por territorio como alternativa sin mapa ante la inaccesibilidad de la capa DANE.
- **Qué hizo el agente:** creó una visualización alternativa interactiva ordenada alfabéticamente, con conteos y porcentajes, y documentó explícitamente que no es un mapa.
- **Archivos creados o modificados:** `analisis/06_espacial.py`, `docs/graficos/espacial.html`, `docs/tablas/alternativa_espacial.csv`, `docs/espacial.md`, `README.md` y esta bitácora.
- **Resultados:** generación correcta para 33 territorios; no se asignaron valores a geometrías ni se creó GeoJSON.
- **Errores encontrados:** no se resolvió el acceso a la capa geográfica oficial; la limitación quedó documentada, no ocultada.
- **Correcciones solicitadas por el estudiante:** ninguna.
- **Decisiones:** utilizar la alternativa en barras aprobada por el estudiante; no presentar el resultado como mapa ni como tasa o riesgo.
- **Aprobaciones:** alternativa sin mapa aprobada antes de crear `06_espacial.py`.
- **Estado de verificación:** script ejecutado y prueba final de estructura, título, fuente, muestra y selección interactiva aprobada. No hay mapa; la alternativa está rotulada como tal.

## 2026-11-24 — Etapa 6: preparación de lecturas

- **Prompt utilizado:** autorización del estudiante para crear la plantilla de lecturas y proponer un gráfico principal, sin redactar interpretaciones personales ni decidir por el estudiante.
- **Qué hizo el agente:** preparó una guía con preguntas, variables, tamaños de muestra, cifras verificadas, limitaciones y campos pendientes de hallazgo/duda por gráfico; propuso el ranking como candidato a gráfico principal.
- **Archivos creados o modificados:** `docs/lecturas.md`, `README.md` y esta bitácora.
- **Resultados:** plantilla preparada con cifras provenientes de las tablas y JSON generados en la etapa 5. El estudiante indicó que el histograma de distribución será el gráfico principal; todavía no aportó justificación personal ni textos de hallazgo/duda.
- **Errores encontrados:** una aserción de verificación usó por error la forma masculina para el campo «duda»; se corrigió la prueba. No afectó el documento ni sus cifras.
- **Correcciones solicitadas por el estudiante:** ninguna.
- **Decisiones:** la propuesta de gráfico principal no es definitiva. Interpretaciones, dudas, elección y justificación deben ser redactadas por el estudiante.
- **Aprobaciones:** el estudiante autorizó preparar la plantilla y comunicó su elección del histograma; la justificación personal y las interpretaciones siguen pendientes.
- **Estado de verificación:** cifras contrastadas con resultados generados; revisión personal del estudiante pendiente antes de continuar a la página.
