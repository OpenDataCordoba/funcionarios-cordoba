# Funcionamiento

Para detectar los cambios correr el script `daily.sh`

El script ejecuta el archivo `detect-changes.py` que:
 - Scrapea la [web de autoridades](http://www.tcpcordoba.gov.ar/tc/institucional/autoridades)
 - Lee los datos almacenados del ultimo scrapping hecho de la carpeta `post-process/data/`
 - Compara si hay cambios en las autoridades
 - Guarda un nuevo csv con las autoridades scrapeadas en esta ejecucion

La salida de `detect-changes.py` (si hay cambios o no) sobreescribe el archivo `post-process/chg.txt`
