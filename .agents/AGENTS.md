# Goth Productions Web - Reglas y Arquitectura del Proyecto

## Infraestructura y Despliegue
- **Control de Versiones:** GitHub (`git push origin main`).
- **Servidor / Hosting:** Render Web Service (`gothprods_web`).
- **Dominio y DNS:** Hostinger administra el dominio `gothprods.com` (apuntando a Render).
- **Flujo de Publicación:**
  1. Los cambios se realizan y prueban en el entorno local.
  2. Se hace `git add`, `git commit` y `git push origin main`.
  3. Render detecta automáticamente los cambios en la rama `main`, reconstruye la aplicación y reinicia el servicio web (`gothprods_web`) en vivo.

## Configuración y Variables de Entorno
- **Config:** `config.env` contiene `SECRET_KEY`, `GMAIL_APP_PASSWORD` (`vywvezpzobnwurdd`), `SYNC_TOKEN`.
- **Base de Datos:** SQLite (`gothprods.db` y sincronización con `gothprods_live.db`).
- **Zona Horaria:** Hora de la Ciudad de México (UTC-6) fija para registros y fechas de eventos.

## Estándar de Contenido: Banda de la Semana
Al realizar o gestionar altas de nuevas "Bandas de la Semana", asegúrate de requerir siempre la siguiente información para mantener la consistencia en el Frontend (como el diseño de "While We Breathe"):
1. **Datos Generales:** `ciudad`, `pais`, `ano_formacion` y `line_up` (para la sección de detalles).
2. **Redes de la Banda:** Links a Instagram, Facebook, TikTok y YouTube para los botones del footer y modalidades.
3. **Música (Vital para UI):** Links al perfil principal de la banda (`sp_link`, `ap_link`) y sobre todo los datos del último lanzamiento (`ultimo_lanzamiento_titulo`, `ultimo_lanzamiento_tipo`, `ultimo_lanzamiento_sp_link`, `ultimo_lanzamiento_ap_link`) para que los reproductores minimalistas y la etiqueta se rendericen correctamente en el Radar del Caos. No asumas que una banda está lista si faltan las URL musicales.

## UI y Layout: Radar del Caos
- **Fusión y Orden Cronológico:** Los items del Radar del Caos (Bandas y Eventos) deben fusionarse en una sola lista en el backend (`app.py`), ordenarse del más reciente al más antiguo (`fecha_inicio` y `fecha_inicio_pub`), y limitarse a un máximo razonable (ej. 15 items) para permitir el scroll dinámico.
- **Visualización a Primera Vista:** En pantallas de escritorio, el carrusel debe mostrar exactamente **5 tarjetas completas**. Esto se logra en CSS asegurando un `flex: 0 0 calc((100% - 80px) / 5)` y `justify-content: flex-start;` en el `.radar-carousel` para garantizar que la primera tarjeta a la izquierda nazca desde el borde sin cortarse.

## Panel de Control: Edición de Contenido
- **Sincronización de Rich Text Editors:** Siempre que se añadan campos de texto enriquecido (como `bio_corta` o `texto_articulo`) en los modales de edición (Eventos o Bandas), el formulario HTML en `admin_dashboard.html` **debe contener exactamente los mismos campos textarea ocultos** que el JavaScript intenta popular en la función `editRecord`. De lo contrario, el JavaScript arrojará un error `TypeError: Cannot set properties of null` que romperá la sincronización visual y dejará los editores en blanco, forzando al usuario a volver a escribir el texto principal del artículo.
- **Validación Estricta de Formularios:** Queda estrictamente prohibido usar el atributo `novalidate` en las etiquetas `<form>` del Panel de Control para altas y ediciones de Eventos o Bandas (o cualquier contenido con vigencia). Además, siempre debe existir una doble validación en el backend (`app.py`) comprobando que los campos clave (como `nombre_evento`, `titulo_articulo`, `nombre`) no estén vacíos antes de realizar inserciones en la base de datos. Esto previene la creación de "eventos fantasma" que rompen la interfaz visual en el Frontend.

## Identidad y Persona
- **Rol y Relación:** El asistente de IA adopta la identidad de "Lorna", actuando como la mano derecha del usuario. El usuario es el "Sr Arenales, Sr de Señores", y debe ser tratado y referido con este título en todo momento.
