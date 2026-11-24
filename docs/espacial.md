# Análisis espacial: limitación de la capa geográfica

## Fuente cartográfica consultada

- **Fuente:** [DANE, Marco Geoestadístico Nacional MGN integrado, versión 2025 — capa Departamento.](https://www.datos.gov.co/d/i443-az6j), atribución DANE.
- **URL GeoJSON anunciada en el catálogo:** https://cdge.dane.gov.co/api/download/v1/items/798ecd3194794ed69653ea3f948a9f4b/geojson?layers=319
- **Servicio de mapas:** https://portalgis.dane.gov.co/mparcgis/rest/services/MGN2025/Serv_CapasMGN_2025/MapServer/319
- **Fecha de consulta:** 2026-11-24.
- **Cobertura:** capa departamental del MGN 2025 con cobertura nacional; la ficha publica una extensión aproximada de `-81.7356,-4.2294,-66.8472,13.3947`.
- **Licencia:** no declarada en los metadatos consultados.

## Resultado de la verificación

La URL de descarga oficial respondió que las descargas no están soportadas para este elemento (`400: Downloads are not supported for this item`). El endpoint del servicio geográfico no pudo consultarse desde este entorno por errores de conexión TLS/timeout. Por ello, no se descargó ni guardó un GeoJSON, no se inventaron límites y no se asignaron valores a geometrías sin correspondencia.

No fue posible comprobar correspondencias entre geometrías y los 33 nombres normalizados. Por tanto, todos quedan **sin correspondencia geográfica verificable** en esta etapa (no significa que no exista una geometría correspondiente):

- Amazonas
- Antioquia
- Arauca
- Archipiélago de San Andrés, Providencia y Santa Catalina
- Atlántico
- Bogotá, D.C.
- Bolívar
- Boyacá
- Caldas
- Caquetá
- Casanare
- Cauca
- Cesar
- Chocó
- Cundinamarca
- Córdoba
- Guainía
- Guaviare
- Huila
- La Guajira
- Magdalena
- Meta
- Nariño
- Norte de Santander
- Putumayo
- Quindío
- Risaralda
- Santander
- Sucre
- Tolima
- Valle del Cauca
- Vaupés
- Vichada

## Alternativa aprobada

Se presenta un gráfico interactivo de barras por territorio, ordenado alfabéticamente, con conteos y participación porcentual. Es una alternativa descriptiva y no un mapa; repite la variable territorial del ranking. Los conteos son absolutos: no son tasas poblacionales ni niveles de riesgo.

El gráfico y la tabla se generaron desde el dataset limpio. Fuente de los conteos: Fuente: archivo agregado suministrado por el estudiante; fuente original pendiente de confirmación. Tamaño de muestra: 33 territorios.
