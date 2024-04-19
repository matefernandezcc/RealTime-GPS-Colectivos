import json
import requests
import pandas as pd

def arreglar_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    entity_data = data.get("_entity", [])
    
    with open(json_file, 'w') as f:
        json.dump(entity_data, f, indent=4)

def json2csv(json_file_path, csv_file_path):
    """
    Convierte un archivo JSON en un archivo CSV con columnas seleccionadas.

    Args:
        json_file_path (str): La ruta del archivo JSON.
        csv_file_path (str): La ruta del archivo CSV de salida.
    """
    try:
        # Cargar el JSON desde el archivo
        with open(json_file_path, "r") as f:
            json_data = json.load(f)

        # Convertir el JSON en un DataFrame
        df = pd.json_normalize(json_data)

        # Seleccionar las columnas relevantes
        selected_columns = ['_id', '_vehicle._vehicle._id', '_vehicle._position._latitude', '_vehicle._position._longitude', 
                            '_vehicle._position._speed', '_vehicle._stop_id', '_vehicle._timestamp', 
                            '_vehicle._trip._route_id', '_vehicle._trip._trip_id']
        df_selected = df[selected_columns]

        # Guardar el DataFrame como un archivo CSV
        df_selected.to_csv(csv_file_path, index=False)

    except Exception as e:
        print("Error:", e)

def guardar_json_desde_url(url, file_path):
    """
    Guarda un JSON desde una URL en un archivo especificado.

    Args:
        url (str): La URL desde donde obtener el JSON.
        file_path (str): La ruta del archivo donde guardar el JSON.

    Returns:
        str: El nombre del archivo guardado si la operación se realizó con éxito, None en caso contrario.
    """
    try:
        # Realizamos la solicitud HTTP
        response = requests.get(url)

        # Verificamos si la solicitud fue exitosa
        if response.status_code == 200:
            # Cargamos el JSON desde la respuesta
            data = response.json()

            # Guardamos el JSON en el archivo especificado
            with open(file_path, "w") as outfile:
                json.dump(data, outfile, indent=4)
            
            return file_path
        else:
            print("Error al realizar la solicitud:", response.status_code)
            return None
    except Exception as e:
        print("Error:", e)
        return None

def filtrar_json(json):
    json_filtrado = []

    for index, row in json.iterrows():
        json_filtrado.append({
            "_id": row["_id"],
            "_vehicle": row["_vehicle"]
        })

    return json_filtrado

def renombrar_dataframe(df):
    """
    Función para renombrar las columnas de un DataFrame.

    Args:
        df (DataFrame): DataFrame de Pandas.

    Returns:
        DataFrame: DataFrame con las columnas renombradas.
    """
    nuevos_nombres = {
        '_id': 'id_empresa',
        '_vehicle._vehicle._id':'id_colectivo',
        '_vehicle._position._latitude': 'latitude',
        '_vehicle._position._longitude': 'longitude',
        '_vehicle._position._speed': 'velocidad',
        '_vehicle._stop_id': 'stop_id',
        '_vehicle._timestamp': 'timestamp',
        '_vehicle._trip._route_id': 'ruta_id',
        '_vehicle._trip._trip_id': 'trip_id'
    }

    df = df.rename(columns=nuevos_nombres)
    df['stop_id'] = df['stop_id'].astype('Int64')
    
    return df
