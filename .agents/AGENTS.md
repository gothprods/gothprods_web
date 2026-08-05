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
