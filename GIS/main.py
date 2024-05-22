import http.server
import socketserver
import geopandas as gpd
import pandas as pd
import plotly.express as px
from io import BytesIO
import json
from urllib.parse import parse_qs
import os

PORT = 8000


class GeoJSONHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            content_type = self.headers['Content-Type']
            if 'multipart/form-data' in content_type:
                boundary = content_type.split("=")[1].encode()
                remaining_bytes = int(self.headers['Content-Length'])
                line = self.rfile.readline()
                remaining_bytes -= len(line)
                if boundary not in line:
                    return

                files = {}
                while remaining_bytes > 0:
                    line = self.rfile.readline()
                    remaining_bytes -= len(line)
                    if boundary in line:
                        break
                    if b'Content-Disposition' in line:
                        disposition_data = line.decode().strip().split('; ')
                        file_key = disposition_data[1].split('=')[1].strip('"')
                        file_name = disposition_data[2].split('=')[1].strip('"')
                        file_data = BytesIO()
                        line = self.rfile.readline()
                        remaining_bytes -= len(line)  # Skip Content-Type line
                        line = self.rfile.readline()
                        remaining_bytes -= len(line)  # Skip empty line
                        while remaining_bytes > 0:
                            line = self.rfile.readline()
                            remaining_bytes -= len(line)
                            if boundary in line:
                                break
                            file_data.write(line)
                        file_data.seek(0)
                        files[file_key] = file_data

                # Leer y procesar los archivos
                gdf_countries = gpd.read_file(files['countries'])
                gdf_continents = gpd.read_file(files['continents'])
                df_capitals = pd.read_csv(files['capitals'], delimiter=';')

                # Estandarizar nombres de países
                df_capitals['COUNTRY'] = df_capitals['COUNTRY'].str.lower()
                gdf_countries['ADMIN'] = gdf_countries['ADMIN'].str.lower()

                # Merge GeoDataFrames
                merged_gdf = gdf_countries.merge(df_capitals, left_on='ADMIN', right_on='COUNTRY')

                # Crear visualización con Plotly y Mapbox
                fig = px.choropleth_mapbox(merged_gdf,
                                           geojson=merged_gdf.geometry,
                                           locations=merged_gdf.index,
                                           color="CONTINENT",  # Cambiar a la columna que te interesa visualizar
                                           mapbox_style="carto-positron",
                                           zoom=3,
                                           center={"lat": 20.0, "lon": 0.0},
                                           opacity=0.5)

                # Guardar la figura en un archivo HTML
                fig.write_html("map.html")

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "message": "File processed and map created!",
                    "map_url": "http://localhost:8000/map.html"
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


# Crear y ejecutar el servidor
with socketserver.TCPServer(("", PORT), GeoJSONHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()