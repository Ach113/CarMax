# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import sqlite3
import pandas as pd
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from .api import find_state_api, find_car_api


class ActionStoreLocation(Action):

    def name(self) -> Text:
        return "action_store_location"

    def run(self, dispatcher, tracker, domain):

        with open('log.txt', 'a') as file:
            car_model = tracker.get_slot('car_model')
            zipcode = tracker.get_slot('zip')
            file.write(f'User at {zipcode} - car model {car_model}')


class ActionRunCarQuery(Action):

    def name(self) -> Text:
        return "action_run_car_query"

    def run(self, dispatcher, tracker, domain):
        car_model = tracker.get_slot('car_model')
        zipcode = tracker.get_slot('zip')

        # 2nd api call
        response = find_car_api(car_model, zipcode)

        dispatcher.utter_message(text=response)


class ActionCheckCar(Action):

    def name(self) -> Text:
        return "action_check_car"

    def run(self, dispatcher, tracker, domain):
        car_model = tracker.get_slot('car_model')
        # connect to db
        conn = sqlite3.connect('./rasa.db')
        query = 'SELECT * FROM cars;'

        df = pd.read_sql_query(query, conn)
        df = df[df['brand'] == car_model]
        if len(df) == 0:
            response = f'{car_model} could not be found in our database. ' \
                       'Please try again if you made a typo,' \
                       'or type `search on web` if you want to search the car outside of our database'
        else:
            response = f'Found {len(df)} instances of {car_model}, ' \
                       f'please enter you zip code so we can find a car closest to you'
        dispatcher.utter_message(text=response)


class ActionDisplayResult(Action):

    def name(self) -> Text:
        return "action_display_result"

    def run(self, dispatcher, tracker, domain):
        zipcode = tracker.get_slot('zip')
        car_model = tracker.get_slot('car_model')

        # 1st api call
        state = find_state_api(zipcode)
        conn = sqlite3.connect('./rasa.db')
        query = f'select * from cars where state = "{state}";'

        df = pd.read_sql_query(query, conn)
        df = df[df['brand'] == car_model].sort_values(by='price', ascending=True).iloc[0]
        price, vin = df['price'], df['vin']
        if len(df) == 0:
            response = f'{car_model} could not be found in {state}. ' + \
                'Type `search on web` if you want to search the car outside of our database'
        else:
            response = f'Found cheapest car - {car_model} at price of {price}$.\n' \
                    f'You can check the vehicle using this vin: {vin}'
        dispatcher.utter_message(text=response)
