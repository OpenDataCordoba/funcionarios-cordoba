# Funcionarios 
Detección de cambios en los organigramas de Provincia y Municipalidad de Córdoba

## Publicacion

Esperamos tener un sitio web con todos los registros. Por el momento la cuenta 
de twitter [@funcionariosCBA](https://twitter.com/funcionariosCBA) publica manualmente los cambios.  

![](img/twt.png)

## Base de datos

La base de datos **general** se administrará (sin terminar) en django en [funcgo/](funcgo/README.md) (**func**ionarios-djan**go**).  
Luego cada institucion (provincia, muni, cuerpos legislativos, etc) tiene un directorio con una metodología de detección de cambios diferente.  

### Ejecutar

Cargar variables de entorno

```
# cargar variables de entorno
source .env

# detectar cambios en cada ámbito
# ############################################
./funcionarios_prov_cba/daily.sh

***********
INICIO COMPARACION 278 registros vs 278 del anterior
Funcionarios a analizar 276 de 278 (se sacan duplicados)
***********
FIN ARCHIVO funcionarios-2019-01-06.csv: nuevos: 0 repetidos: 276 cambiaron: 0 muertos: 0

# ############################################
./funcionarios_ciudad_cba/daily.sh

***********
INICIA ARCHIVO data/funcionarios-2019-01-08.csv
*********** 309 registros
***********
INICIO COMPARACION 309 registros vs 309 del anterior
Funcionarios a analizar 309 de 309 (se sacan duplicados)
***********
FIN ARCHIVO funcionarios-2019-01-08.csv: nuevos: 0 repetidos: 309 cambiaron: 0 muertos: 0

# ############################################
./funcionarios_tribunal_de_cuentas_provincia

Inicio de Comparacion para la Fecha: 2019-01-08
Entre 2019-01-01 00:00:00 y 2019-01-08 el cargo Presidente se mantiene sin cambios.
Entre 2019-01-01 00:00:00 y 2019-01-08 el cargo Vocal por la Mayoria se mantiene sin cambios.
Entre 2019-01-01 00:00:00 y 2019-01-08 el cargo Vocal por la Minoria se mantiene sin cambios.
Entre 2019-01-01 00:00:00 y 2019-01-08 el cargo Secretaria de Fiscalizacion Legal se mantiene sin cambios.
Entre 2019-01-01 00:00:00 y 2019-01-08 el cargo Prosecretaria de Fiscalizacion Legal se mantiene sin cambios.
Entre 2019-01-01 00:00:00 y 2019-01-08 el cargo Secretaria de Fiscalizacion Presupuestaria se mantiene sin cambios.
Entre 2019-01-01 00:00:00 y 2019-01-08 el cargo Prosecretaria de Fiscalizacion Presupuestaria se mantiene sin cambios.
Entre 2019-01-01 00:00:00 y 2019-01-08 el cargo Fiscalia se mantiene sin cambios.
######## Fin Comparacion ###########

```