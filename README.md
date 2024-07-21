# openrta-tools
Herramientas para procesar el registro turístico de la Junta de Andalucía

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
- [Características](#características)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Instalación

- Instala python versión 3 (Las pruebas se han hecho con la versión 3.12.4)
- Instala las librerías necesarias
  pip install -r requirements.txt

## Uso

- Descarga y descomprime el fichero openrta.json de la web de datos abiertos de la junta de andalucía
- Edita o copia el fichero de configuración rta2map.json para indicar la localización del fichero de datos json, el nombre del fichero de salida, las coordenadas centrales del mapa, el nivel de zoom, el radio de los puntos y las expresiones regulares para filtrar las provincias y los municipios
- Ejecuta python rta2map.py <fichero de configuración|vacío> Creará un fichero con nombre <fichero de salida> que se puede incluir en un servidor web. Si no se especifica fichero de configuración utilizará el nombre rta2map.json

## Características

El programa crea un mapa con las viviendas de uso turístico (en rojo) y apartamentos turísticos en negro. No se incluyen las viviendas que alquilan habitaciones ni los estabelecimiento hoteleros.

## Contacto

https://cadizresiste.org

