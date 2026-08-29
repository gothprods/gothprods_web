# Resumen de Cambios: Resolución de Duplicados

## 1. Corrección de Duplicados
Al cambiar la fuente de sincronización de YouTube a Ivoox, el sistema detectó algunos episodios como "nuevos" debido a que tenían títulos distintos en cada plataforma, generando duplicados visuales en el carrusel de *La Galería Nocturna*. 

Se han unificado los siguientes episodios en la base de datos, fusionando sus enlaces para que no aparezcan dos veces:
- *LA CRISIS DE LOS CONCIERTOS EN MÉXICO YA EMPEZÓ* (YouTube) se fusionó con *LIVE: Esto ya es grave...* (Ivoox).
- *3er Aniversario Mexapedia* (YouTube) se fusionó con *LIVE: De enciclopedia a motor...* (Ivoox).

## 2. Episodios Faltantes
Dado que YouTube bloqueó nuestro acceso automatizado (RSS), **el botón "Sincronizar" ahora solo puede extraer episodios que ya estén disponibles en el feed de Ivoox**. 
Si el Live faltante fue transmitido recientemente en YouTube y aún no se ha distribuido al feed de Ivoox, el sistema no podrá detectarlo de forma automática.

Para agregarlo sin tener que esperar a Ivoox, se recomienda utilizar el botón "Agregar" en el Panel de Control.
