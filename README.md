# Geografía de las capturas por delitos sexuales contra niños, niñas y adolescentes en Colombia

> **Borrador académico para revisión y aprobación del estudiante.** Las referencias marcadas como pendientes no se han confirmado y no deben interpretarse como datos establecidos.

## ¿Cuál es el análisis de datos?

### Contexto

Este proyecto explora la distribución territorial de las capturas registradas por delitos sexuales contra niños, niñas y adolescentes (NNA) en Colombia. Una captura no equivale necesariamente a una víctima, una denuncia, una condena ni a la totalidad de delitos cometidos. Un mayor conteo no constituye evidencia directa de una mayor incidencia delictiva.

**Proyecto original del libro:** pendiente de confirmación por el estudiante.

**Autor/a:** pendiente de confirmación.

### Pregunta principal

¿Cómo se distribuyen territorialmente las capturas por delitos sexuales contra niños, niñas y adolescentes en Colombia y qué departamentos presentan los mayores registros?

### Preguntas orientadoras

- ¿Cuáles son los territorios con mayores y menores registros?
- ¿Cómo se distribuyen las capturas entre territorios?
- ¿Qué porcentaje del total corresponde a los cinco territorios con mayores registros?
- ¿Cuál es el promedio y la mediana de capturas por territorio?
- ¿Qué patrones descriptivos de concentración pueden observarse?
- ¿Qué limitaciones tiene comparar cantidades absolutas entre departamentos?

### Objetivos

**General:** describir exploratoriamente la distribución territorial de los registros de capturas disponibles, sin inferir incidencia delictiva ni causalidad.

**Específicos:**

1. Validar e inventariar las variables y documentar las transformaciones reproducibles.
2. Resumir la distribución y el ranking de los conteos por territorio.
3. Explorar la representación geográfica únicamente si se verifica una fuente cartográfica y una correspondencia territorial.
4. Comunicar resultados, procedencia de datos y limitaciones de forma transparente.

## Descripción de los datos

- **Dataset:** `capturas_colombia.csv`, copia de `Hoja 3_data (1).csv`.
- **Unidad de observación:** territorio agregado (departamento o Bogotá, D. C.).
- **Registros y variables:** 33 registros territoriales y 2 variables, según la validación inicial del archivo.
- **Cobertura geográfica:** 33 territorios consignados en el CSV; su correspondencia con divisiones administrativas oficiales queda sujeta a verificación.
- **Fuente original:** pendiente de confirmación documental.
- **Periodo de referencia y metodología de recolección:** pendientes de confirmación. La cadena `20260825` del encabezado no se toma como periodo de observación.

| Nombre original | Nombre corto propuesto | Descripción | Tipo observado |
|---|---|---|---|
| `Departamento` | `departamento` | Nombre territorial consignado en el archivo. | Categórica nominal y geográfica. |
| `Recuento de Capturas_por_delitos_sexuales_contra_niños,_niñas_y_adolescentes_en_Colombia_20260825.csv` | `capturas` | Conteo de capturas registrado por territorio. | Cuantitativa discreta (entero en la carga inicial). |

## Alcance analítico

| Tipo de análisis | Aplica inicialmente | Justificación y límites |
|---|---|---|
| Distribución | Sí | Hay una variable de conteo cuantitativo; describe su distribución entre los territorios observados. |
| Ranking | Sí | Hay una categoría territorial y un conteo agregado; ordena registros, no incidencia ni riesgo. |
| Relación | No | El archivo no ofrece dos variables apropiadas para analizar asociaciones. |
| Cambio en el tiempo | No | No hay una serie temporal documentada. |
| Espacial | Sí, condicionado | Hay nombres territoriales; requiere una fuente cartográfica verificable y correspondencias resueltas. |

## Metodología y limitaciones

El análisis se realizará con scripts reproducibles de Python y pandas; las visualizaciones se producirán con Altair. El archivo original se conservará sin cambios y se verificará mediante SHA-256. No se imputarán valores faltantes ni se eliminarán observaciones por ser atípicas. Toda normalización territorial se documentará y no se fusionará Bogotá con Cundinamarca.

Los conteos absolutos no son tasas poblacionales. Las diferencias pueden estar relacionadas, entre otros factores posibles, con el tamaño poblacional, las denuncias, la capacidad institucional y la actividad policial; este dataset por sí solo no permite verificar esas explicaciones. No hay información suficiente para estimar directamente víctimas, estudiar cambios temporales o establecer relaciones causales. El análisis es exploratorio y descriptivo.

## Estructura del repositorio

```text
.
├── AGENTS.md
├── README.md
├── requirements.txt
├── datos/
│   ├── crudo/capturas_colombia.csv
│   └── limpio/capturas_colombia_limpio.csv
├── analisis/
│   ├── 01_carga.py
│   ├── 02_inventario.py
│   ├── 03_limpieza.py
│   ├── 04_distribucion.py
│   ├── 05_ranking.py
│   ├── 06_espacial.py
│   └── 07_estadisticas.py
├── docs/
│   ├── inventario.md
│   ├── limpieza.md
│   ├── espacial.md
│   ├── lecturas.md
│   ├── css/
│   ├── graficos/
│   └── tablas/
└── bitacora/prompts.md
```

Los scripts, tablas, gráficos y documentos de las etapas posteriores se crearán cuando correspondan y después de las aprobaciones requeridas; no se consideran entregables terminados en este borrador.

## Reproducibilidad

Se requiere Python 3.14.2 para reproducir el entorno inicial observado. Desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
python analisis/01_carga.py
python analisis/02_inventario.py
python analisis/03_limpieza.py
python analisis/04_distribucion.py
python analisis/05_ranking.py
python analisis/06_espacial.py
python analisis/07_estadisticas.py
```

El script de carga informa el esquema, muestra, tipos, valores faltantes, duplicados, codificación, separador, territorios únicos y hash. El inventario genera `docs/inventario.md`; la limpieza genera el CSV limpio y `docs/limpieza.md`. Los scripts 04–07 producen estadísticas, tablas y gráficos HTML. La capa DANE no pudo descargarse desde este entorno; `06_espacial.py` genera una alternativa en barras, no un mapa, y documenta la limitación en `docs/espacial.md`. `docs/lecturas.md` deja los campos de hallazgo, duda y elección principal para el estudiante. Ejecuta los pasos en orden y revisa sus resultados.

## Sitio web y vista previa local

La página editorial se encuentra en `docs/index.html`. Sus indicadores y tablas consumen resultados JSON agregados, generados por `04_distribucion.py`, `05_ranking.py` y `07_estadisticas.py`. Después de generar los resultados, verifica su consistencia con:

```bash
python analisis/08_validacion.py
```

Para revisar el sitio localmente, desde la raíz del repositorio ejecuta:

```bash
python -m http.server 8000 --directory docs
```

Abre `http://localhost:8000`. La publicación mediante GitHub Pages y la URL definitiva están pendientes de autorización y configuración.

## Herramientas

- Python y pandas para carga y procesamiento.
- Altair para visualizaciones interactivas.
- HTML, CSS y JavaScript para la página estática; Vega y Vega-Lite para renderizar los gráficos.

## Créditos, publicación y revisión

**Autor/a:** pendiente de confirmación. **Fuente y créditos de los datos:** pendientes de confirmación documental. Este README es un borrador y requiere revisión y aprobación personal del estudiante.

**GitHub Pages:** pendiente de publicación y verificación. La publicación no se realizará sin autorización; una página puede ser pública aunque el repositorio sea privado.
