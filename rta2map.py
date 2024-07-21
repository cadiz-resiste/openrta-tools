import sys
import os
import json
import re
import folium
from pyproj import Transformer
from branca.element import Template, MacroElement

def comprobar_expresion_regular(texto, expresion_regular):
    # Compila la expresión regular
    patron = re.compile(expresion_regular)
    
    # Comprueba si la cadena de texto cumple la expresión regular
    if patron.match(texto):
        return True
    else:
        return False

def meters_to_degrees(easting, northing, zone_number, northern_hemisphere=True):
    """
    Convierte coordenadas UTM en metros a coordenadas geográficas en grados.

    :param easting: Coordenada Este (X) en UTM.
    :param northing: Coordenada Norte (Y) en UTM.
    :param zone_number: Número de la zona UTM.
    :param northern_hemisphere: True si la coordenada está en el hemisferio norte, False si está en el hemisferio sur.
    :return: (latitud, longitud) en grados.
    """
    # Definir el EPSG code para la zona UTM específica
    if northern_hemisphere:
        epsg_code = f"epsg:326{zone_number:02d}"
    else:
        epsg_code = f"epsg:327{zone_number:02d}"
    
    # Crear el transformador desde UTM a WGS84
    transformer = Transformer.from_crs(epsg_code, "epsg:4326")
    
    # Realizar la transformación
    lat, lon = transformer.transform(easting, northing)
    
    return lat, lon


def generate_osm_map(lat, lon, zoom_start=12, output_file="osm_map.html"):
    """
    Genera un fichero HTML con un mapa de OpenStreetMap.

    :param lat: Latitud del centro del mapa.
    :param lon: Longitud del centro del mapa.
    :param zoom_start: Nivel de zoom inicial del mapa.
    :param output_file: Nombre del fichero de salida.
    """
    # Crear el mapa centrado en las coordenadas especificadas
    m = folium.Map(location=[lat, lon], zoom_start=zoom_start, tiles="CartoDB Positron")
    
    # Guardar el mapa en un fichero HTML
    m.save(output_file)

    print(f"Mapa guardado en {output_file}")



# Función para leer el fichero de configuración y asignar las variables
def leer_configuracion(fichero):
    try:
        # Abrir y leer el contenido del fichero JSON con codificación UTF-8
        with open(fichero, 'r', encoding='utf-8') as file:
            config = json.load(file)

        # Asignar las variables desde el fichero JSON
        file_var = config.get("file")
        file_out = config.get("file_out")
        zoom_start = config.get("zoom_start")
        circ_radio = config.get("circ_radio")
        reprov = config.get("reprov")
        remunicipio = config.get("remunicipio")
        lat_centro = config.get("lat_centro")
        lon_centro =config.get("lon_centro")

        return file_var, file_out, zoom_start, circ_radio, reprov, remunicipio, lat_centro, lon_centro

    except FileNotFoundError:
        print(f"El fichero {fichero} no se encuentra.")
        return None, None, None, None, None, None, None, None
    except json.JSONDecodeError:
        print("Error al decodificar el fichero JSON.")
        return None, None, None, None, None, None, None, None

# Función para leer y filtrar registros de un fichero JSON en formato UTF-8
def genera_mapa_desde_rtajson(fichero, lat, lon, zoom_start, circ_radio, reprov, remunicipio):
    try:
        # Abrir y leer el contenido del fichero JSON con codificación UTF-8
        with open(fichero, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Crear el mapa centrado en las coordenadas especificadas
        zoom_start=14
        m = folium.Map(location=[lat, lon], zoom_start=zoom_start, tiles="CartoDB Positron")
        # Crear una leyenda personalizada usando una plantilla HTML
        template = """
                {% macro html(this, kwargs) %}
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <style>
                        .legend {
                            position: fixed;
                            bottom: 50px;
                            left: 50px;
                            width: 250px;
                            height: auto;
                            padding: 10px;
                            background: white;
                            border: 2px solid grey;
                            z-index: 1000;
                            font-size: 14px;
                        }
                        .legend h4 {
                            margin: 0;
                            padding: 0;
                        }
                        .legend div {
                            margin-bottom: 5px;
                        }
                        .circle {
                            height: 12px;
                            width: 12px;
                            border-radius: 50%;
                            display: inline-block;
                            margin-right: 5px;
                        }
                    </style>
                </head>
                <body>
                    <div class='legend'>
                        <h4>Leyenda</h4>
                        <div><span class='circle' style='background:red;'></span>Vivienda de Uso Turístico</div>
                        <div><span class='circle' style='background:black;'></span>Apartamento Turístico</div>
                    </div>
                </body>
                </html>
                {% endmacro %}
        """

        macro = MacroElement()
        macro._template = Template(template)

        # Añadir la leyenda al mapa
        m.get_root().add_child(macro)


        # Filtrar registros según los criterios especificados
        registros_filtrados = []
        for registro in data:
            if (comprobar_expresion_regular(str(registro.get("PROVINCIA")), reprov) and
                comprobar_expresion_regular(str(registro.get("MUNICIPIO")), remunicipio) and
                registro.get("TIPO_OBJETO") in ["Vivienda de uso turístico", "Apartamento turístico"] and
                registro.get("COORD_X") not in ["", "null", None] and
                registro.get("COORD_Y") not in ["", "null", None]):

                # Asignar la variable name según la condición especificada
                name = registro.get("NOMBRE") if registro.get("NOMBRE") not in ["", "null"] else registro.get("COD_REGISTRO")
                registro["name"] = name
                coord_x_ = str(registro.get("COORD_X")).replace(",", ".")
                coord_y_ = str(registro.get("COORD_Y")).replace(",", ".")
                lat, lon = meters_to_degrees(float(coord_x_),float(coord_y_), zone_number, northern_hemisphere)
                # print(f"lat= {lat}")
                # print(f"lon= {lon}")
                licencia=str(registro.get("COD_REGISTRO"))
                texto_html = f"""
                    <!DOCTYPE html>
                    <html lang="es">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>VUT</title>
                    </head>
                    <body>
                        <h1>{licencia}</h1>
                        <p>{name}</p>
                    </body>
                    </html>
                """
                if (registro.get("TIPO_OBJETO") in  ["Vivienda de uso turístico"] and
                    registro.get("GRUPO") != "Completa"):
                    color="blue"
                    radius=10
                elif (registro.get("TIPO_OBJETO") in  ["Vivienda de uso turístico"] and
                    registro.get("GRUPO") == "Completa"):
                    color="red"
                    radius=20
                elif (registro.get("TIPO_OBJETO") in  ["Apartamento turístico"]):
                    color="black"
                    radius=30

                tooltip=licencia
                #folium.Marker([lat, lon], popup=str(registro.get("ID")), tooltip="tooltip").add_to(m) 
                # Crear un círculo
                if (color != "blue"):
                    circulo = folium.CircleMarker(
                        location=[lat, lon],
                        radius=circ_radio,  # Radio en pixels
                        color=color,
                        fill=True,
                        fillOpacity=1.0,
                        fill_color=color
                    )
                    # Añadir el popup al círculo
                    popup = folium.Popup(texto_html, max_width=300)
                    circulo.add_child(popup)

                    # Agregar el círculo al mapa
                    circulo.add_to(m)



        # Imprimir los campos de los registros filtrados
#        for i, registro in enumerate(registros_filtrados):
#            print(f"Registro {i + 1}:")
#            for campo, valor in registro.items():
#                print(f"  {campo}: {valor}")
#            print()
        # Guardar el mapa en un fichero HTML
        m.save(file_out)

    except FileNotFoundError:
        print(f"El fichero {fichero} no se encuentra.")
    except json.JSONDecodeError:
        print("Error al decodificar el fichero JSON.")

def obtener_nombre_fichero_configuracion():
    # Obtiene el nombre del programa en ejecución
    nombre_programa = os.path.basename(__file__)
    
    # Cambia la extensión del nombre del programa de .py a .json
    nombre_configuracion_por_defecto = os.path.splitext(nombre_programa)[0] + '.json'
    
    # Obtiene los argumentos de la línea de comandos
    argumentos = sys.argv
    
    # Si hay al menos un argumento después del nombre del programa, úsalo como nombre de fichero de configuración
    if len(argumentos) > 1:
        nombre_configuracion = argumentos[1]
    else:
        # Si no, usa el nombre por defecto
        nombre_configuracion = nombre_configuracion_por_defecto
    
    return nombre_configuracion

if __name__ == "__main__":
    nombre_fichero_configuracion = obtener_nombre_fichero_configuracion()
    print(f"Nombre del fichero de configuración: {nombre_fichero_configuracion}")
    fichero_config = nombre_fichero_configuracion

    # Llamar a la función para leer el fichero de configuración y asignar las variables
    file_var, file_out, zoom_start, circ_radio, reprov, remunicipio, lat_centro, lon_centro = leer_configuracion(fichero_config)
    
    # Imprimir los valores de las variables asignadas
    print(f"file: {file_var}")
    print(f"file_out: {file_out}")
    
    # lat_centro = 36.52612  # Latitud del centro del mapa (Cadiz, España)
    # lon_centro = -6.28871  # Longitud del centro del mapa (Cadiz, España)
    # easting_utm = 205812.726053923  # Coordenada Este en UTM
    # northing_utm = 4047326.36246818  # Coordenada Norte en UTM
    zone_number = 30  # Número de la zona UTM
    northern_hemisphere = True  # Hemisferio norte
    
    print(f"latitud: {lat_centro}")
    print(f"longitud: {lon_centro}")
    print(f"Exp Regular Provincia: {reprov}")
    print(f"Exp Regular Municipio: {remunicipio}")
    
    # Llamar a la función para leer y filtrar los registros del JSON
    genera_mapa_desde_rtajson(file_var, lat_centro, lon_centro, zoom_start, circ_radio, reprov, remunicipio)
    
