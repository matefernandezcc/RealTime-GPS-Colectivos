import sys
import os
import time
import pandas as pd

# Agregar el directorio padre al sys.path
src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
sys.path.append(project_dir)
import utils.filters as filter
import utils.get_data as get

def main():
    # Tokens para acceder a la API
    client_id = 'TOKEN_PARA_API'
    client_secret = 'TOKEN_PARA_API'

    # # Llamar a la función para descargar y descomprimir el archivo GTFS
    # print("Descargando datos GTFS de colectivos...")
    # get.colectivos_feed_gtfs(client_id, client_secret)
    # time.sleep(2)

    # Leer archivos csv del data
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    # agency = routes = pd.read_csv(os.path.join(data_dir, "agency.csv"))
    # calendar_dates = routes = pd.read_csv(os.path.join(data_dir, "calendar_dates.csv"))
    routes = pd.read_csv(os.path.join(data_dir, "routes.csv"))
    # shapes = pd.read_csv(os.path.join(data_dir, "shapes.csv"))
    stop_times = pd.read_csv(os.path.join(data_dir, "stop_times.csv"), dtype={'trip_id': str, 'stop_id': str})
    stops = pd.read_csv(os.path.join(data_dir, "stops.csv"))
    # trips = pd.read_csv(os.path.join(data_dir, "trips.csv"), dtype={'trip_id': str, 'service_id': str})

    # Filtros
    routes_145 = filter.by_linea_colectivo(routes, "145")
    print("\t=============== Rutas de la línea 145 - hasta UTN ===============")
    print(routes_145[routes_145['route_id'] == 1854])
    print("\n")

    print("\t=============== Rutas que pasan por Mozart ===============")
    print(stops[stops.stop_name.str.contains("MOZART", case=False)])
    print("\n")

    print("\t=============== Tiempos de llegada 145 a UTN por Mozart ===============")
    print(stop_times[(stop_times['stop_id'].str.contains("204647", case=False)) & (stop_times['trip_id'].str.contains("236453-1", case=False))])
    print("\n")


if __name__ == "__main__":
    main()

