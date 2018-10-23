# Funcionarios 
Detección de cambios en los organigramas de Provincia y Municipalidad de Córdoba


## Provincia de Córdoba

Scrape al sitio web, no encontramos nómina en algún formato reutilizable.  
El scrape comienza desde aquí: http://www.cba.gov.ar/reparticiones/  
Se obtiene datos de todas las oficinas existentes y los funcionarios a cargo.  

Ejecutar para detectar cambios periodicamente:
```
./daily.sh
```
## Municipalidad de Córdoba

Pendiente de carga leyendo [el webservice](https://gobiernoabierto.cordoba.gob.ar/api/funciones/)  

## Publicacion

Esperamos tener un sitio web con todos los registros. Por el momento la cuenta 
de twitter [@funcionariosCBA](https://twitter.com/funcionariosCBA) publica manualmente los cambios.  

![](img/twt.png)