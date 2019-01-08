# Funcionarios 
Detección de cambios en los organigramas de Provincia y Municipalidad de Córdoba

## Publicacion

Esperamos tener un sitio web con todos los registros. Por el momento la cuenta 
de twitter [@funcionariosCBA](https://twitter.com/funcionariosCBA) publica manualmente los cambios.  

![](img/twt.png)

## Base de datos

La base de datos **general** se administra en django en [funcgo/](funcgo/README.md) (**func**ionarios-djan**go**).  
Luego cada institucion (provincia, muni, cuerpos legislativos, etc) tiene un directorio con una metodología de detección de cambios diferente.  

## Provincia de Córdoba

En [funcionarios_prov_cba/](funcionarios_prov_cba/README.md)
Scrape al sitio web, no encontramos nómina en algún formato reutilizable.  

## Municipalidad de Córdoba

Pendiente de carga leyendo [el webservice](https://gobiernoabierto.cordoba.gob.ar/api/funciones/)  
