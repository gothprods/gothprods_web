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
