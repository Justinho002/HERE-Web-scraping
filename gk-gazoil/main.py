import requests
import json
import re
from bs4 import BeautifulSoup


def get_data():
    r = requests.get('https://gk-gazoil.ru/')
    soup = BeautifulSoup(r.text, features='html.parser')
    fuel_inputs = soup.find_all('input', {'name': 'map_type'})
    fuel = [x['value'] for x in fuel_inputs]
    reg_selector = soup.find('ul', {'class': 'region-list'})
    cities_inputs = reg_selector.find_all('a', {'class': 'city_select'})
    cities = [x['data-code'] for x in cities_inputs]
    places = []
    for city in cities:
        cookies = {'THIS_CITY': city}
        r = requests.post('https://gk-gazoil.ru/include/ajax/map-new.php/',
                          data={'fuelTypes': ','.join(fuel)},
                          cookies=cookies)
        placemarks = re.findall(r'myPlacemark = new ymaps\.Placemark\(.*?}\);', r.text, flags=re.S)
        for placemark in placemarks:
            text_coord = re.findall(r'\[.*\]', placemark)[0].strip('[').strip(']')
            coord = [float(x) for x in text_coord.split(',')]
            name = re.findall(r"hintContent: '.*'", placemark)[0].strip("hintContent: '").strip("'")
            places.append({'coord': coord, 'name': name})
    return places


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
                'coordinates': [point['coord'][1], point['coord'][0]]
            },
            'properties': {
                'name': point['name'],
            }
        })
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(output, indent=2, ensure_ascii=False))


places = get_data()
to_geojson(places, 'places.geojson')
