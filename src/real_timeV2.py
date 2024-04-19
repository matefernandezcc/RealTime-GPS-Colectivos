import time
import folium
import sys
import os
src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
sys.path.append(project_dir)
from utils.filters import *
from utils.get_data import *
from utils.json import *

# Lista para almacenar las ubicaciones históricas del colectivo
ubicaciones_historicas = []

# ========================================================================= #
# Función para obtener los datos de la API y trazar el recorrido en el mapa #
# ========================================================================= #
primer_iteracion = True

def GPS(url_api, path_json, path_csv, mapa, linea_colectivo, id_colectivo):
    global primer_iteracion
    global id_elegidoV2
    try:
        # Hacer una solicitud a la API para obtener los datos del colectivo
        response = guardar_json_desde_url(url_api, path_json)

        if(linea_colectivo == "145C"):
            if primer_iteracion:
                arreglar_json(response) # Esto es necesario porque por alguna razón el 145 tiene mal formateado su json :)
                json2csv(path_json, path_csv)
                file_csv = pd.read_csv(path_csv)
                file_csv = renombrar_dataframe(file_csv) # Esto es porque las columnas tenian nombres raros, asi quedan más simples

                # Esto busca si hay algun colectivo en alguna de las paradas de stop_hacia_utn y si los encuentra retorna el id de la parada
                colectivos_en_una_parada = radio_de_llegada(stops_todas, file_csv)

                listar_parada = file_csv[file_csv['stop_id'] == colectivos_en_una_parada]
                print(listar_parada)
                id_elegido = input("\nIngresar el ID a trackear: ")
                id_elegidoV2 = id_elegido

                procesar_colectivo(1, path_json, listar_parada, id_elegido, ubicaciones_historicas, mapa)
                primer_iteracion = False
            else:
                response = guardar_json_desde_url(url_api, path_json)
                arreglar_json(response)
                json2csv(path_json, path_csv)
                file_csv = pd.read_csv(path_csv)
                file_csv = renombrar_dataframe(file_csv)
                procesar_colectivo(1, path_json, file_csv, id_elegidoV2, ubicaciones_historicas, mapa)
        else:
            file_csv = pd.read_csv(path_csv) # No se usa esto pero lo dejo para tener polimorfismo <3
            procesar_colectivo(0, path_json, file_csv, id_colectivo, ubicaciones_historicas, mapa)
    except Exception as e:
        print("Error al obtener datos:", e)

# ========================================================================= #
#       Información importante para el funcionamiento del script            #
# ========================================================================= #

# Tokens para acceder a la API
client_id = "TOKEN_API"
client_secret = "TOKEN_API"

# Requests para la API
gps_linea_145 = f"https://apitransporte.buenosaires.gob.ar/colectivos/vehiclePositions?client_id={client_id}&client_secret={client_secret}&json=1&agency_id=516"
gps_todas_las_lineas = f"https://apitransporte.buenosaires.gob.ar/colectivos/vehiclePositionsSimple?client_id={client_id}&client_secret={client_secret}"



# Definir la línea de colectivo a trackear (con su ramal, es decir su letra)
linea_colectivo = "145C"



# Paths donde guardar archivos json y csv
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
path_json = os.path.join(parent_dir, "data", f"{linea_colectivo}.json")
path_csv = os.path.join(parent_dir, "data", f"{linea_colectivo}.csv")


 ## Ejemplos de algunos id (sacados de https://transitfeeds.com/p/colectivos-buenos-aires/1037/latest/routes?q=109)
linea_109A_estLiniers = 15718
linea_99A = 5057
linea_160A_estLanus= 12914
linea_101A_aRetiro = 4895
linea_7B_aRetiro = 2094


# Crear un mapa html del trayecto
mapa = folium.Map(location=[-34.6037, -58.3816], zoom_start=12)

def main():
    print("Accediendo a la API...\n")


    if (linea_colectivo == "145C"):
        url_api = gps_linea_145
        id_colectivo = 0
    else:
        url_api = gps_todas_las_lineas
        id_colectivo = linea_160A_estLanus    
        # Acá tenes que poner el id del colectivo que queres trackear, se puede buscar en transitfeeds.com o con la API BA


    print(f"\t========== Localización GPS del {linea_colectivo} id: {id_colectivo} ==========")
    try:
        while True:
            GPS(url_api, path_json, path_csv, mapa, linea_colectivo, id_colectivo)
            time.sleep(60) # La API se actualiza cada 30 segundo asi que la llamo cada 60 para asegurar la info
    except KeyboardInterrupt:
        print("\nDeteniendo el programa...")

        # Guardar el mapa como un archivo HTML
        mapa.save(("mapa_colectivo.html"))
        print("Mapa guardado como 'mapa_colectivo.html'.")
        sys.exit()

if __name__ == "__main__":
    main()
