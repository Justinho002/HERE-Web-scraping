import requests
import json


def get_data():
    r = requests.get("https://azsgazprom.ru/price/price.csv")
    encoded = r.text.encode(encoding='latin_1')
    rows = encoded.decode('utf-8').split('\n')
    table = []
    for row in rows:
        if row != '':
            table.append(row.split(';'))
    return table


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
                'coordinates': [float(point[3]), float(point[2])]
            },
            'properties': {
                'address': point[4],

            }
        })
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(output, indent=2, ensure_ascii=False))


places = get_data()
to_geojson(places, 'places.geojson')
