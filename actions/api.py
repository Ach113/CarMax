import requests
import numpy as np
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim


def find_zip_api(location):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode(location)
        x = location.raw['display_name'].split(', ')[4]
        return x
    except:
        return '95112'


def find_car_api(model_name, zip):
    header = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
    })

    # search for a particular keyword
    model_name_processed = '-'.join(x for x in model_name.split(' '))
    url = f"https://www.cars.com/shopping/results/?models[]={model_name_processed}&page_size=20&sort=best_match_desc&zip={zip}"
    html = BeautifulSoup(requests.get(url, headers=header).text, 'html.parser')

    # collect all the prices
    prices = [x.get_text(strip=True) for x in html.find_all('span', attrs={'class': 'primary-price'})]
    if len(prices) == 0:
        return f'No car with the model {model_name} could be found'
    prices = [int(x.replace(',', '')[1:]) for x in prices]
    min_idx = np.argmin(prices)

    # collect the hyperlink to those vehicles
    hrefs = [x.get('href') for x in html.find_all('a', attrs={'class': 'vehicle-card-link js-gallery-click-link'})]
    car_urls = [r'https://www.cars.com' + href for href in hrefs]

    return f'Found {model_name} with lowest price ({min(prices)}$) at {car_urls[min_idx]}'
