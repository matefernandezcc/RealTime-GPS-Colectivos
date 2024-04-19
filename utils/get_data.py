import pandas as pd
import requests
import zipfile
import os
import folium
import sys
import math
#import networkx as nx
#from shapely.geometry import Point

## Defino arrays con todas las paradas del 145C ordenadas por su stop_id
stop_hacia_utn = [2032595,2032591,205731,205979,20887,2032582,201900,202112,203146,201898,205194,20904,201912,207358,20998,20983]
stop_desde_utn = [205735,6427102313,20869,203134,205721,203144,2031251,201817,2032583,201917,202811,202059,2032582,201874,6427102319,205201,20877,202800,
                     202094,2032584,206899,201925,2032586,20933,205202,202093,205203,6427118750,205199]
stops_importantes = [2032582,204647,206164,201745,201974,205822,201259,201258,201256,201252,201246]
stops_todas = [2032582, 204647, 206164, 201745, 201974, 205822, 201259, 201258, 201256, 201252, 201246,
               205735, 6427102313, 20869, 203134, 205721, 203144, 2031251, 201817, 2032583, 201917, 202811,
               202059, 201874, 6427102319, 205201, 20877, 202800, 202094, 2032584, 206899, 201925, 2032586,
               20933, 205202, 202093, 205203, 6427118750, 205199, 2032595, 2032591, 205731, 205979, 20887,
               201900, 202112, 203146, 201898, 205194, 20904, 201912, 207358, 20998, 20983,6490111646,202109,6490101154,203557]

def procesar_colectivo(tipo, path_json, csv, id_colectivo, ubicaciones_historicas, mapa):
    # Filtrar por el ID de colectivo
    if tipo == 1:
        data_by_id = csv
    else:
        response = pd.read_json(path_json, encoding='utf-8')
        data_by_id = response[response['id'] == id_colectivo] 
        if data_by_id.empty:
            sys.exit("El colectivo no está en circulación, elige otro.")
    
    # Extraer las coordenadas del colectivo
    coordenadas = data_by_id[['latitude', 'longitude']]
    latitud = coordenadas['latitude'].iloc[0]
    longitud = coordenadas['longitude'].iloc[0]
    print(f"Coordenadas actuales: {latitud}, {longitud}")

    # Marcador diferente para la primera parada
    if len(ubicaciones_historicas) == 0:
        folium.Marker([latitud, longitud], popup="Inicio del recorrido", icon=folium.Icon(color='green')).add_to(mapa)
    else:
        folium.Marker([latitud, longitud], popup="Ubicación actual").add_to(mapa)

    # Agregar la ubicación actual a las ubicaciones históricas
    ubicaciones_historicas.append([latitud, longitud])

    # Dibujar líneas que conectan las ubicaciones históricas en el mapa
    if len(ubicaciones_historicas) > 1:
        folium.PolyLine(ubicaciones_historicas, color="blue", weight=2.5, opacity=1).add_to(mapa)

def txt_to_csv(directory):
    # Obtener la lista de archivos en el directorio
    files = os.listdir(directory)
    
    # Filtrar los archivos .txt
    txt_files = [file for file in files if file.endswith(".txt")]
    
    # Renombrar cada archivo .txt a .csv
    for txt_file in txt_files:
        # Obtener el nombre del archivo y la extensión
        file_name, file_extension = os.path.splitext(txt_file)
        
        # Construir las rutas de archivo de entrada y salida
        txt_file_path = os.path.join(directory, txt_file)
        csv_file_path = os.path.join(directory, f"{file_name}.csv")
        
        # Renombrar el archivo .txt a .csv
        os.rename(txt_file_path, csv_file_path)
        
        print(f"Archivo {txt_file} renombrado a {file_name}.csv")
    
    # Eliminar archivos .zip del directorio
    for file in files:
        if file.endswith(".zip"):
            file_path = os.path.join(directory, file)
            os.remove(file_path)
            print(f"Archivo {file} eliminado.")

def colectivos_feed_gtfs(client_id, client_secret):
    directory = "data"
    url = f"https://apitransporte.buenosaires.gob.ar/colectivos/feed-gtfs?client_id={client_id}&client_secret={client_secret}"
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Guardar el archivo ZIP en la carpeta "../data"
        file_path = os.path.join(directory, "data.zip")
        with open(file_path, "wb") as file:
            file.write(response.content)
        
        # Descomprimir el archivo ZIP en la misma carpeta
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            print("Descomprimiendo ZIP...")
            zip_ref.extractall(directory)
        
        print("Archivo ZIP descargado y descomprimido exitosamente.")
    else:
        print(f"Error al descargar el archivo ZIP. Código de estado: {response.status_code}")
    print("Convirtiendo archivos txt en csv...")
    txt_to_csv(directory)

def coordenadas_colectivo(tipo, path_json, csv, id_colectivo, ubicaciones_historicas, mapa):
    # Filtrar por el ID de colectivo
    if tipo == 1:
        data_by_id = csv
    else:
        response = pd.read_json(path_json, encoding='utf-8')
        data_by_id = response[response['id'] == id_colectivo] 
        if data_by_id.empty:
            sys.exit("El colectivo no está en circulación, elige otro.")
    
    # Extraer las coordenadas del colectivo
    coordenadas = data_by_id[['latitude', 'longitude']]
    latitud = coordenadas['latitude'].iloc[0]
    longitud = coordenadas['longitude'].iloc[0]
    detalles_coordenadas(latitud, longitud)

    # Marcador diferente para la primera parada
    if len(ubicaciones_historicas) == 0:
        folium.Marker([latitud, longitud], popup="Inicio del recorrido", icon=folium.Icon(color='green')).add_to(mapa)
    else:
        folium.Marker([latitud, longitud], popup="Ubicación actual").add_to(mapa)

    # Agregar la ubicación actual a las ubicaciones históricas
    ubicaciones_historicas.append([latitud, longitud])

    # Dibujar líneas que conectan las ubicaciones históricas en el mapa
    if len(ubicaciones_historicas) > 1:
        folium.PolyLine(ubicaciones_historicas, color="blue", weight=2.5, opacity=1).add_to(mapa)

def direccion_coordenada(latitud, longitud):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitud}&lon={longitud}&zoom=18&addressdetails=1"
    response = requests.get(url)
    data = response.json()

    try:
        house_number = data['address'].get('house_number', '')
        road = data['address'].get('road', '')
        return f"{road} {house_number}"
    except KeyError:
        print("Alguno de los datos de dirección no está presente en la respuesta.")
        return None, None, None

def detalles_coordenadas(latitud, longitud):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitud}&lon={longitud}&zoom=18&addressdetails=1"
    response = requests.get(url)
    data = response.json()

    # Casa
    #lat = -34.602615
    #lon = -58.425800

    # Parada 145C
    lat = -34.603278
    lon = -58.435494
    nombre_parada = direccion_coordenada(lat, lon)

    try:
        house_number = data['address'].get('house_number', '')
        road = data['address'].get('road', '')
        suburb = data['address'].get('suburb', '')
        distancia = distancia_colectivo_parada(latitud, longitud, lat, lon)
        print(f"{latitud}, {longitud} | {road} {house_number}, {suburb} | A {distancia} Kms de {nombre_parada}")
    except KeyError:
        print("Alguno de los datos de dirección no está presente en la respuesta.")
        return None, None, None

def distancia_colectivo_parada(latitud_colectivo, longitud_colectivo, latitud_parada, longitud_parada):
    # Convertir las coordenadas de grados a radianes
    latitud_colectivo = math.radians(latitud_colectivo)
    longitud_colectivo = math.radians(longitud_colectivo)
    latitud_parada = math.radians(latitud_parada)
    longitud_parada = math.radians(longitud_parada)
    
    # Calcular la diferencia de latitud y longitud
    delta_latitud = latitud_parada - latitud_colectivo
    delta_longitud = longitud_parada - longitud_colectivo
    
    # Aplicar la fórmula de la distancia euclidiana en un plano cartesiano
    distancia = math.sqrt(delta_latitud ** 2 + delta_longitud ** 2) * 6371  # Radio de la Tierra en kilómetros
    
    # Truncar la distancia a dos decimales
    distancia_truncada = round(distancia, 2)
    
    return distancia_truncada



