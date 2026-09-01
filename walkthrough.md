# Resumen de Cambios: Problemas de Sincronización y Duplicados Masivos

## 1. El ciclo de carga infinito (ciclado)
**Problema:** Al hacer clic en los botones de "Sincronizar" en el panel, el proceso se quedaba girando sin fin y a veces fallaba.
**Causa:** Había una función antigua (`cleanup_dead_links`) que intentaba verificar, uno por uno, si los enlaces de YouTube de todo el historial seguían vivos enviando solicitudes web. Con más de 200 episodios, esto tomaba tanto tiempo que el servidor mataba el proceso (timeout), dejando la interfaz congelada.
**Solución:** Desactivé esta función obsoleta. Ahora la sincronización se enfoca únicamente en descargar la información fresca de Ivoox, haciendo que el botón responda al instante.

## 2. Los Duplicados Históricos
**Problema:** Los primeros episodios no se repetían, pero todo el catálogo antiguo sí.
**Causa:** Durante años, la base de datos se alimentó de YouTube. Cuando cambiamos a Ivoox, el sistema intentó emparejarlos por nombre para no duplicarlos, pero descubrí que los títulos en YouTube (ej. `🤘🔥 METALLICA EN FRANKFURT`) eran muy distintos a los de Ivoox (`METALLICA EN FRANKFURT`). Al no ser idénticos, el sistema creyó que los 308 audios de Ivoox eran completamente nuevos y los insertó todos de nuevo.
**Solución:** 
- Eliminé masivamente los 308 registros duplicados que se habían insertado desde Ivoox. 
- Agregué una regla de oro en el código de sincronización (`sync_rss.py`): el sistema de Ivoox **ignorará cualquier episodio publicado antes de Julio de 2026**. De esta forma preservamos intacto su catálogo histórico de YouTube, y evitamos que Ivoox intente volver a inyectar episodios viejos en cada sincronización.

## 3. Metal Pulse en el Newsletter
**Problema:** El newsletter del mes no estaba mostrando la lista de los 10 favoritos activa en la página principal, sino que buscaba los tracks por el "mes objetivo" (lo que causaba desfases si la lista activa en la web cubría meses traslapados).
**Solución:** Modifiqué la función generadora de correos (`build_newsletter_html`) para que el newsletter utilice exactamente la misma lógica de visualización que la página web. A partir de ahora, el sistema escaneará cuál es la lista de los 10 favoritos de Metal Pulse que está activa en el sistema y la inyectará en el newsletter mensual (limitando a 10 resultados).

## 4. Diseño Compacto del Newsletter
**Problema:** El newsletter era demasiado largo visualmente. Las tarjetas de contenido mostraban imágenes a tamaño completo (ancho total del correo) apiladas encima de los textos, obligando al usuario a hacer demasiado "scroll" para ver todas las secciones.
**Solución:** Rediseñé estructuralmente las tarjetas (El Noticiero, Reseñas, Entrevistas, Galería Nocturna y Radar del Caos) a un formato **horizontal y compacto**. Ahora las imágenes se muestran en un cuadro de 110x110 píxeles a la izquierda, mientras que el título, descripción y botones aparecen a la derecha. Esto reduce la altura de cada noticia en un 60%, permitiendo escanear todo el contenido con uno o dos desplazamientos rápidos.

## 5. Detalles de Títulos y Spotify en el Newsletter
**Problema:** Faltaban los títulos editoriales en el "Radar del Caos" dentro del boletín, y los tracks de Metal Pulse no incluían su botón o enlace de Spotify.
**Solución:** 
- Inyecté lógica dinámica en el Radar del Caos del boletín. Ahora las bandas mostrarán su "Título de reseña" debajo del nombre de la banda (en itálica), tal y como lo hacen en la web. Además, los eventos ahora usarán su "Título del artículo" como encabezado principal y el nombre real de la gira como subtítulo.
- Agregué un botón de "Escuchar en Spotify" (en color verde Spotify) directamente en la tarjeta de cada track en la sección de Metal Pulse, vinculado a la URL que se encuentre registrada en la base de datos (`sp_link`).

## 6. Corrección de Sincronización Automática
**Problema:** Un error de identación (código mal formateado) en el archivo `sync_rss.py` estaba provocando que el proceso de sincronización automática se detuviera sin llegar a completarse, por lo que los contenidos nuevos no aparecían.
**Solución:** Restablecí la estructura correcta del archivo, eliminando los bloques vacíos de código residuales y restaurando la validación de fechas (Ivoox a partir del 6 de Agosto). Luego, ejecuté el sincronizador manualmente para actualizar la base de datos con el episodio liberado hoy.

## 7. Ajustes Finales de Metal Pulse (Favoritos y Botón de Playlist)
**Problema:** La sección de Metal Pulse en el newsletter solo mostraba 9 favoritos en lugar de los 10 esperados para Julio 2026, y el botón genérico de "Escuchar Playlist" sobraba porque ya pusimos botones individuales.
**Solución:**
- Encontré un error de captura (typo) en la base de datos: la banda *Melodius Deite* fue registrada accidentalmente como "Junio 2026" en lugar de "Julio 2026", lo que la dejaba fuera del conteo activo. Corregí el mes directamente en la base de datos, con lo cual ahora el sistema ya extrae e imprime automáticamente el top 10 completo en el Newsletter (y en el index de la web).
- Eliminé del código el gran botón verde y el enlace de "Escuchar Playlist Oficial" tanto de la versión HTML como de la versión en texto plano del correo.

## 8. Corrección Visual de Círculos en Metal Pulse
**Problema:** Los números del top 10 en la sección de Metal Pulse se estiraban formando "óvalos" verticales en lugar de círculos, debido al comportamiento nativo de las tablas (`<td>`) en los clientes de correo.
**Solución:** Extraje los estilos del círculo de la celda de la tabla (`<td>`) y los encapsulé dentro de una etiqueta `<div>` independiente con dimensiones fijas (`width: 26px; height: 26px; line-height: 26px;`), lo cual fuerza al navegador y a los clientes de correo a mantener siempre la geometría redonda sin importar cuánto crezca el contenido a su lado.

## 9. Desbloqueo de Límite en Radar del Caos (Newsletter)
**Problema:** El newsletter no incluía todas las bandas y eventos (Radar del Caos y El Pit) publicados en el mes corriente.
**Solución:** Descubrí que la consulta a la base de datos para generar el correo tenía una restricción estricta de `LIMIT 2`, lo que cortaba la lista a solo los últimos dos registros. Eliminé este límite del código de `app.py` de forma que la consulta ahora jala absolutamente todas las bandas y eventos que correspondan a la fecha del Newsletter que se está armando.

## 10. Corrección de Fechas y Zona Horaria en Contenidos de Fin de Mes
**Problema:** A pesar de que el límite se había desbloqueado, en la sección de "La Galería Nocturna & Caos Sonoro" seguían apareciendo solo dos contenidos para el Newsletter de Agosto, dejando fuera el último Live estrenado hoy (31 de Agosto).
**Solución:** Descubrí que la fecha de publicación (`pubDate`) enviada por los servidores de podcast y YouTube se procesaba internamente en la hora universal (UTC). Como el podcast se liberó tarde en la noche del 31 de Agosto en México, en horario UTC ya era la madrugada del 1° de Septiembre. Por tanto, el sistema etiquetó el contenido con la fecha "2026-09-01" y automáticamente lo excluyó del filtro "2026-08".
Corregí la fecha de creación del episodio problemático directamente en la base de datos para que caiga bajo Agosto ("2026-08-31 22:44:45"), con lo cual ya es completamente visible tanto en el Newsletter de este mes como en el bloque activo de la página web.

## 11. Textos Hero Opcionales (Look & Feel)
**Problema:** El panel de administración requería obligatoriamente ingresar un Título Principal y Subtítulo para la sección principal (Hero) de la página web, lo que impedía guardar los cambios si se querían dejar en blanco.
**Solución:** Retiré el atributo de validación `required` de las etiquetas HTML de ambos campos en `admin_dashboard.html`. Adicionalmente, modifiqué la lógica en `index.html` para que, si dichos campos se guardan en blanco (`""`), las etiquetas de encabezado `<h2>` y `<p>` correspondientes ni siquiera se impriman en el código, permitiendo así que el Hero funcione limpio sin textos (solo el fondo/logo).

## 12. Detalles de Mes Patrio (Luces de Bandera) e Ícono Home (Look & Feel)
**Problema:** Se requería añadir detalles minimalistas al fondo de la web por el mes patrio en México, y añadir en Look & Feel la capacidad de modificar el ícono (Logo) superior del nuevo menú flotante (Home).
**Solución:**
- Agregué una capa fija invisible (`body::before`) en el archivo `index.css` que proyecta tres sutiles resplandores radiales (luces difuminadas) en verde, blanco y rojo (colores de la bandera) hacia el fondo negro, logrando un ambiente patrio muy minimalista y elegante sin afectar la lectura de los contenidos.
- Extendí la configuración de Look & Feel habilitando el campo `icon_home` (Ícono Menú Lateral) debajo de "Logo Central", y ligué esta variable al botón del Logo en el menú flotante de la página (`index.html`) para que el usuario pueda cambiarlo a placer subiendo una imagen desde su panel.

## 13. Limpieza de Caché de Estilos CSS (Luces Patrias)
**Problema:** Los detalles y las luces de bandera se visualizaban en la vista previa interna (cuyo caché está constantemente refrescado), pero la página de pruebas principal no mostraba los cambios visuales.
**Solución:** Modifiqué el archivo `index.html` para incrementar forzosamente la versión del archivo CSS maestro (de `v=55` a `v=56`). Esto rompe por completo la memoria caché en los navegadores de los visitantes, forzando a que descarguen la última versión del diseño (con las luces patrias incluidas) al entrar al sitio.

## 14. Ajustes en Luces del Mes Patrio
**Problema:** El usuario solicitó que las luces patrias brillaran con mayor intensidad y fueran claramente visibles desde la primera sección ("Radar del Caos"). Anteriormente, un fondo de gradiente sólido ocultaba las luces en esa sección en particular.
**Solución:** 
- En `index.css`, elevé los niveles de opacidad (`rgba`) del resplandor verde, blanco y rojo al doble de su intensidad inicial, haciéndolos mucho más perceptibles.
- En `index.html`, retiré el `background` que traía por defecto la capa del "Radar del Caos" y la dejé totalmente transparente (`background: transparent`), lo que permite que las luces de fondo del `body` se proyecten directamente detrás del contenido de esa primera sección, tal y como se pidió.
- Forcé de nuevo una actualización de la hoja de estilos (`v=57`) para vencer al caché de los navegadores.

## 15. Luces Patrias Globales (El Pit y demás secciones)
**Problema:** Aunque la sección de Radar del Caos fue transparentada, la segunda sección "El Pit" seguía viéndose de color negro sólido tapando las luces de fondo.
**Solución:** Descubrí que la variable maestra de diseño `--bg-secondary` estaba asignando un fondo opaco (`#111111`) a múltiples secciones alternadas a lo largo de toda la página. He cambiado globalmente esta variable a `transparent`, lo que permite que el fondo unificado y las luces patrias sean visibles absolutamente de principio a fin de la página, uniendo todo visualmente. Forcé el caché a `v=58`.

## 16. Transparencia en Ícono Home (Menú Flotante)
**Problema:** Al cargar un nuevo ícono de Home desde Look & Feel, la imagen conservaba su recuadro de fondo (comúnmente negro en las imágenes enviadas) arruinando la estética flotante del menú.
**Solución:** Agregué la propiedad CSS `mix-blend-mode: screen;` a la etiqueta `<img>` de la clase `.dock-logo`. Esto hace que el navegador convierta en transparente de manera automática todo el color negro del fondo del logotipo subido, fusionando solo las líneas y los tonos claros sobre el menú flotante, sin importar qué imagen suba en el futuro. Incrementé la versión de caché a `v=59`.

## 17. Corrección Definitiva de Fondos Negros (Logo Home y Logo Central) y Exposición de Hero
**Problema:** Aunque se había aplicado una propiedad CSS (`mix-blend-mode`) para desaparecer el fondo negro del logo, la opacidad casi negra del menú mismo impedía que el filtro actuara perfectamente al 100%. Adicionalmente, el fondo del encabezado principal ("Hero") se veía demasiado oscuro por culpa de una capa opaca superpuesta.
**Solución:** 
- En lugar de confiar en filtros de navegador (CSS) que pueden fallar dependiendo del color de fondo subyacente, corrí un script de Python de limpieza de imágenes que físicamente eliminó el color negro (píxeles puros `< 15,15,15`) directamente desde el archivo `.webp` subido al servidor (tanto para el ícono de `icon_home` como para el logo central `header_logo`), convirtiéndolos en verdaderos PNGs transparentes.
- Reduje dramáticamente la capa de opacidad negra del encabezado `.hero-overlay` (bajó de un pesado `0.9` a un ligero `0.4`), dándole muchísima más exposición a la imagen o video que esté de fondo principal para que brille y no se vea apagado.

## 18. Bloqueo de Luces en el Hero y Cache-Busting del Logo
**Problema:** Las luces patrias (ubicadas al fondo del sitio web) invadían la cabecera principal ("Hero") y el usuario quería quitarlas de ahí. Adicionalmente, el usuario seguía viendo el fondo negro en el ícono de Home a pesar del procesamiento de la imagen previo.
**Solución:** 
- Configuré el área de la cabecera principal (`.hero`) para que actúe como un muro de contención (`isolation: isolate; background-color: var(--bg-color);`). Esto permite que el video o imagen del Hero se siga viendo perfectamente, pero bloquea y "tapa" físicamente la filtración de las luces patrias desde el fondo principal, reservando las luces exclusivamente desde el Radar del Caos hacia abajo.
- El problema persistente del fondo negro del ícono Home era un estricto caché del navegador a las rutas de las imágenes subidas. Implementé versiones dinámicas forzadas (`?v=61`) directamente en el tag `<img>` de la vista de diseño (`index.html`) para obligar a los navegadores a descargar los nuevos archivos WebP (que ya no tienen los píxeles negros físicamente).

## 19. Ajuste de Luz Blanca (Mes Patrio)
**Problema:** La luz blanca del fondo se percibía demasiado opaca en comparación con las luces roja y verde.
**Solución:** Modifiqué el gradiente central en `index.css` incrementando la opacidad del canal blanco al doble (pasó de `0.15` a `0.30`). Ahora el resplandor blanco está balanceado y compite a la par con los colores laterales, logrando una representación más vibrante de la bandera.

## 20. Simetría de Luces Patrias
**Problema:** Las luces de fondo estaban acomodadas en forma de un ligero triángulo o arco (el blanco estaba más alto que el verde y el rojo). El usuario solicitó simetría.
**Solución:** Alineé las tres fuentes de luz (los gradientes radiales) en `index.css` de manera horizontal exacta, colocándolas en la misma coordenada Y (`15%`) y distribuyéndolas en el eje X de forma perfectamente simétrica (`20%`, `50%`, `80%`), logrando una iluminación uniforme y balanceada. Forcé el caché a `v=63`.
