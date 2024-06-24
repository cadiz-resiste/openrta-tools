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
- Edita el fichero de configuración rta2map.json para indicar la localización de l fichero de datos json
- Ejecuta python rta2map.py. Creará un fichero con nombre cadiz_map.html que se puede incluir en un servidor web.

## Características

El programa crea un mapa con las viviendas de uso turístico (en rojo) y apartamentos turísticos en negro. No se incluyen las viviendas que aluilan habitaciones ni los estabelecimiento hoteleros.

## Contacto

https://cadizresiste.org

