import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

ACCESS_TOKEN = "8568aae18568aae18568aae1dd865de1a3885688568aae1ed0a1d4b31ce48cd6796003d"
V = "5.199"
URL = "https://api.vk.com/method/"
COUNT = 1


class VKAPIHandler:
    def get_cities(city_name):
        params = {
            "access_token" : ACCESS_TOKEN,
            "v" : V,
            "q" : city_name,
            "count" : COUNT
        }

        response = requests.get(f"{URL}database.getCities", params=params)
        return response.json()

    def get_universities(university_name):
        params = {
            "access_token" : ACCESS_TOKEN,
            "v" : V,
            "q" : university_name,
            "count" : COUNT
        }
    
        response = requests.get(f"{URL}database.getUniversities", params=params)
        return response.json()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/cities"):
            self.handle_cities_request()
        elif self.path.startswith("/universities"):
            self.handle_universities_request()

    
    def handle_cities_request(self):
        query = self.path.split('?')[1]
        params = dict(i.split('=') for i in query.split('&')) 
        city_name = params.get('q')

        result = VKAPIHandler.get_cities(city_name)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
        
    def handle_universities_request(self):
        request = self.path.split('?')[1]
        params = dict(i.split('=') for i in request.split('&'))
        university_name = params.get('q')

        result = VKAPIHandler.get_universities(university_name)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Выполняйте запрос в адресной строке. Пример запроса - http://localhost:8000/cities?q=Moscow")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
    