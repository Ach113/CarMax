# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from .api import *


class ActionStoreLocation(Action):

    def name(self) -> Text:
        return "action_store_location"

    def run(self, dispatcher, tracker, domain):
        SlotSet("is_old_user", True)


class ActionRunCarQuery(Action):

    def name(self) -> Text:
        return "action_run_car_query"

    def run(self, dispatcher, tracker, domain):
        car_model = tracker.get_slot('car_model')
        loc = tracker.get_slot('location')

        # 1st api call
        zip = find_zip_api(loc)
        # 2nd api call
        response = find_car_api(car_model, zip)

        dispatcher.utter_message(text=response)
