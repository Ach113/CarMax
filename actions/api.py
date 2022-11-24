import sqlite3
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from uszipcode import SearchEngine
# from geopy.geocoders import Nominatim


def find_state_api(zipcode):
    """ finds the state based on a zipcode using `uszipcode` api """
    engine = SearchEngine()
    zipcode = engine.by_zipcode(zipcode)

    conn = sqlite3.connect('./rasa.db')
    query = 'SELECT * FROM states;'

    df = pd.read_sql_query(query, conn)
    state_map = dict(zip(df['Abbr'].values, df['State'].values))

    if not zipcode:
        return 'california'
    else:
        return state_map[zipcode.state].lower()


# def find_zip_api(location):
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     try:
#         location = geolocator.geocode(location)
#         x = location.raw['display_name'].split(', ')[4]
#         return x
#     except:
#         return '95112'


def find_car_api(model_name, zip):
    """ browses `cars.com` using search queries """
    header = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
    })

    model_name = '-'.join(x for x in model_name.split(' '))
    # search for a particular keyword
    # model_name_processed = '-'.join(x for x in model_name.split(' '))
    url = f"https://www.cars.com/shopping/results/?models[]={model_name}&page_size=20&sort=best_match_desc&zip={zip}"
    html = BeautifulSoup(requests.get(url, headers=header).text, 'html.parser')

    # collect all the prices
    prices = [x.get_text(strip=True) for x in html.find_all('span', attrs={'class': 'primary-price'})]
    prices = [x.replace(',', '')[1:] for x in prices]
    prices = [np.inf if 'Priced' in str(x) else int(x) for x in prices]
    # prices = list(filter(lambda x: 'Priced' not in str(x), prices))
    if len(prices) == 0 or all([x == np.inf for x in prices]):
        return f'No car with the model {model_name} could be found'

    min_idx = np.argmin(prices)

    # collect the hyperlink to those vehicles
    hrefs = [x.get('href') for x in html.find_all('a', attrs={'class': 'vehicle-card-link js-gallery-click-link'})]
    car_url = r'https://www.cars.com' + hrefs[min_idx]
    min_price = prices[min_idx]

    return f'Found {model_name} with lowest price ({min_price}$) at {car_url}'
