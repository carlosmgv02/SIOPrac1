import http.server
import socketserver
from queries import (generate_capital_based_map,
                           generate_movie_count_map, generate_genre_count_map)

PORT = 8000

class GeoJSONHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/templates/index.html'
        elif self.path == '/map/countries':
            generate_countries_map()  # Function needs to be implemented
            self.path = '/templates/countries_map.html'
        elif self.path == '/map/continents':
            generate_continents_map()  # Function needs to be implemented
            self.path = '/templates/continents_map.html'
        elif self.path == '/map/capitals/genres':
            generate_capital_based_map()  # Function needs to be implemented
            self.path = '/templates/capital_genre_map.html'
        elif self.path == '/map/movies':
            generate_movie_count_map()  # Ensure this function generates the correct HTML file
            self.path = '/templates/movie_count_map.html'
        elif self.path == '/map/genres':
            generate_genre_count_map()  # Ensure this function generates the correct HTML file
            self.path = '/templates/genre_heatmap.html'
        elif self.path == '/map/bubble':
            generate_bubble_map()  # Function needs to be implemented
            self.path = '/templates/bubble_map.html'
        else:
            # Fallback to serving other static files correctly
            return super().do_GET()

# Start and run the server
with socketserver.TCPServer(("", PORT), GeoJSONHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
