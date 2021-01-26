import requests
import json
from bs4 import BeautifulSoup


def get_data():
    r = requests.get("http://kirishiavtoservis.ru/stations/")
    soup = BeautifulSoup(r.text, features="html.parser")
    data_marker = soup.find("div", {'class': 'map'})
    return json.loads(data_marker['data-markers'])


def to_geojson(points, filename):
    output = {
        'type': 'FeatureCollection',
        'features': []
    }
    for point in points:
        output['features'].append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(point['lat']), float(point['lng'])]
            },
            'properties': {
                'name': point['name'],
                'address': point['address'],
                'phone': point['phone'],

            }
        })
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(output, indent=2, ensure_ascii=False))


places = get_data()
to_geojson(places, 'places.geojson')
