import http.server
import socketserver
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from io import StringIO

PORT = 8000

class GeoJSONHandler(http.server.SimpleHTTPRequestHandler):
    def parse_multipart(self, data):
        boundary = data.split(b'\r\n')[0]
        parts = data.split(boundary)
        files = {}
        for part in parts:
            if b'Content-Disposition' in part:
                header, content = part.split(b'\r\n\r\n', 1)
                disposition_data = header.split(b'; ')
                if len(disposition_data) > 2:
                    file_key = disposition_data[1].split(b'=')[1].strip(b'"')
                    file_data = content.rstrip(b'\r\n--')
                    files[file_key.decode()] = StringIO(file_data.decode())
        return files

    def do_POST(self):
        if self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            files = self.parse_multipart(post_data)

            # Leer y procesar los archivos
            gdf_countries = gpd.read_file(files['countries'])
            gdf_continents = gpd.read_file(files['continents'])
            df_capitals = pd.read_csv(files['capitals'], delimiter=';')

            # Convertir las capitales a GeoDataFrame
            gdf_capitals = gpd.GeoDataFrame(df_capitals, geometry=gpd.points_from_xy(df_capitals.LONGITUDE, df_capitals.LATITUDE))

            # Crear visualización con Plotly y Mapbox
            fig = go.Figure()

            # Añadir países
            fig.add_trace(go.Choroplethmapbox(
                geojson=json.loads(gdf_countries.to_json()),
                locations=gdf_countries.index,
                z=gdf_countries.index,
                text=gdf_countries['ADMIN'],  # Añadir nombres de los países como etiquetas
                colorscale="Viridis",
                marker_line_width=0,
                hoverinfo="text+z",  # Mostrar información del texto y valor z en el hover
                hovertext=gdf_countries['ADMIN'],  # Texto que se mostrará en el hover
                visible=True,
                name='Countries'
            ))

            # Añadir continentes
            fig.add_trace(go.Choroplethmapbox(
                geojson=json.loads(gdf_continents.to_json()),
                locations=gdf_continents.index,
                z=gdf_continents.index,
                text=gdf_continents['continent'],  # Añadir nombres de los continentes como etiquetas
                colorscale="Inferno",
                marker_line_width=0,
                hoverinfo="text+z",  # Mostrar información del texto y valor z en el hover
                hovertext=gdf_continents['continent'],  # Texto que se mostrará en el hover
                visible=False,
                name='Continents'
            ))

            # Añadir capitales
            fig.add_trace(go.Scattermapbox(
                lat=gdf_capitals.geometry.y,
                lon=gdf_capitals.geometry.x,
                mode='markers',
                marker=go.scattermapbox.Marker(size=9, color='red'),
                text=gdf_capitals['CAPITAL'],  # Añadir nombres de las capitales como etiquetas
                hoverinfo="text",  # Mostrar solo el texto en el hover
                visible=True,
                name='Capitals'
            ))

            # Añadir mapa de calor
            fig.add_trace(go.Densitymapbox(
                lat=gdf_capitals.geometry.y,
                lon=gdf_capitals.geometry.x,
                z=[1] * len(gdf_capitals),  # Pesos uniformes para todas las capitales
                radius=10,
                colorscale='YlOrRd',
                opacity=0.6,
                visible=False,
                name='Heatmap'
            ))

            # Añadir mapa de bombolles
            fig.add_trace(go.Scattermapbox(
                lat=gdf_capitals.geometry.y,
                lon=gdf_capitals.geometry.x,
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=15,
                    color='blue',
                    opacity=0.6
                ),
                text=gdf_capitals['CAPITAL'],
                hoverinfo="text",
                visible=False,
                name='Bubble Map'
            ))

            fig.update_layout(
                mapbox_style="carto-positron",
                mapbox_zoom=1.5,
                mapbox_center={"lat": 20.0, "lon": 0.0},
                updatemenus=[
                    {
                        "buttons": [
                            {
                                "args": [{"visible": [True, False, False, False, False]}],
                                "label": "Countries",
                                "method": "update"
                            },
                            {
                                "args": [{"visible": [False, True, False, False, False]}],
                                "label": "Continents",
                                "method": "update"
                            },
                            {
                                "args": [{"visible": [False, False, True, False, False]}],
                                "label": "Capitals",
                                "method": "update"
                            },
                            {
                                "args": [{"visible": [False, False, False, True, False]}],
                                "label": "Heatmap",
                                "method": "update"
                            },
                            {
                                "args": [{"visible": [False, False, False, False, True]}],
                                "label": "Bubble Map",
                                "method": "update"
                            },
                            {
                                "args": [{"visible": [True, False, True, False, False]}],
                                "label": "Countries & Capitals",
                                "method": "update"
                            },
                            {
                                "args": [{"visible": [False, True, True, False, False]}],
                                "label": "Continents & Capitals",
                                "method": "update"
                            },
                            {
                                "args": [{"visible": [True, True, True, False, False]}],
                                "label": "All",
                                "method": "update"
                            }
                        ],
                        "direction": "left",
                        "pad": {"r": 10, "t": 10},
                        "showactive": True,
                        "type": "buttons",
                        "x": 0.1,
                        "xanchor": "left",
                        "y": 1.1,
                        "yanchor": "top"
                    }
                ]
            )

            # Guardar la figura en un archivo HTML
            fig.write_html("templates/map.html")

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
        elif self.path == '/map.html':
            self.path = 'templates/map.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


# Crear y ejecutar el servidor
with socketserver.TCPServer(("", PORT), GeoJSONHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
