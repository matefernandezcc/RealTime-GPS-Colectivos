import pandas as pd
import sys

def by_linea_colectivo(file, linea):
    file_by_linea = file[file.route_short_name.str.contains(linea, case=False)]
    return file_by_linea

def radio_de_llegada(array_de_id, csv145):
    """
    Función para calcular el radio de llegada a partir de una lista de IDs de paradas.

    Args:
        array_de_id (list): Lista de IDs de paradas.
        csv145 (DataFrame): DataFrame que contiene los datos de los vehículos.

    Returns:
        int: El número de ID de las parada donde encontro un colectivo.
    """
    i = 0
    filtro = None

    # Bucle while que se ejecuta mientras el DataFrame filtro esté vacío
    while filtro is None or filtro.empty:
        # Verificar si hemos agotado todos los elementos en array_de_id
        if i >= len(array_de_id):
            print("No se encontraron colectivos de la línea 145 en las paradas proporcionadas.")
            sys.exit()
            return i
        
        # Obtener el stop_id actual
        stop_id_actual = array_de_id[i]
        
        # Filtrar el DataFrame csv145 según el stop_id_actual
        filtro = csv145[csv145["stop_id"] == stop_id_actual]
        
        # Incrementar el índice para pasar al próximo stop_id en la siguiente iteración
        i += 1
    
    print(f"Se encontraron colectivos de la línea 145 en la parada con stop_id {stop_id_actual}.\n")
    return stop_id_actual