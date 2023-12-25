# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Password@123',
                database='rasa'
            )
cursor = connection.cursor()

class ActionFetchDataFromMySQL(Action):
    def name(self) -> Text:
        return "action_fetch_data_mysql"  # Name of your action

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            
            
            if connection.is_connected():
                
                
                
                cursor.execute('SELECT distinct location FROM restaurant')
                result = cursor.fetchall()
                print(result)
                # cursor.close()
                # connection.close()

                # Process the result
                for row in result:
                     
                    row = ', '.join(row)
                    dispatcher.utter_message(text= row)
                

        except Exception as e:
            print(f"Error connecting to MySQL database: {e}")
            # Handle errors here

        return []

class ActionFetchHotelFromMySQL(Action):
    def name(self) -> Text:
        return "action_fetch_hotel_mysql" 

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            
            
            if connection.is_connected():
                place =  next(tracker.get_latest_entity_values("place"),None)
               
                print('Connected to MySQL database')

                cursor.execute('SELECT name FROM restaurant where location= %s',(place,))
                result = cursor.fetchall()
                # print(result)
                # cursor.close()
                # connection.close()

               
                for row in result:
                    row = ', '.join(row)
                     
                    dispatcher.utter_message(text= row)
                # dispatcher.utter_message(text="Specify one...")
                


        except Exception as e:
            print(f"Error connecting to MySQL database: {e}")
            # Handle errors here

        return []


class reservationconfirm(Action):

    def name(self) -> Text:
        return "action_reservation_confirm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('reservation confirm')
        # print(tracker.latest_message)
        
        # hotel =  next(tracker.get_latest_entity_values("hotel"),None)
        hotel = tracker.get_slot("hotel")
        print(hotel)
        number =  next(tracker.get_latest_entity_values("number"),None)

        dispatcher.utter_message(text=f"you are booking for {hotel} for {number} people")

        return []