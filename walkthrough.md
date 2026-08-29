# Resumen de Cambios: Recuperación de Entrevistas Under

## El Problema Detectado
El Sr. Arenales reportó que en la página web solo se visualizaban 3 registros en la sección de *Entrevistas Under*.
Al analizar la base de datos y la lógica de sincronización (`sync_rss.py`), descubrí que el sistema solo estaba enviando a esa sección los audios y videos que contenían explícitamente la palabra **"Entrevista"** o **"Interview"** en su título. Sin embargo, históricamente, la gran mayoría de las entrevistas se han publicado bajo el formato **"Especial | [Nombre de la Banda] en La Galería Nocturna"** (ej. *Especial | Noumenia en La Galería Nocturna*). Como el sistema no reconocía este formato, las catalogaba incorrectamente dentro de *La Galería Nocturna*.

## Solución Aplicada
1. **Limpieza y Reasignación en Base de Datos:** Ejecuté un comando para buscar todos los episodios antiguos que cumplieran con el formato de bandas "en La Galería Nocturna" (excluyendo podcasts de opinión como "Doble Filo" o "Lo Que Sucedió") y los moví masivamente a su sección correspondiente. 
2. **Actualización de Reglas de Sincronización:** Modifiqué el archivo `sync_rss.py` para que, de ahora en adelante, la herramienta de auto-sincronización reconozca automáticamente este patrón de títulos y los envíe siempre a *Entrevistas Under* desde el primer momento.

## Resultados y Validación
La base de datos de producción (`gothprods_live.db`) ya ha sido actualizada. Pasamos de tener **solo 3 registros** a tener un total de **61 Entrevistas Under** correctamente catalogadas y visibles en la página web.
