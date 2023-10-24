import requests
from datetime import datetime

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

APP_ID = config.get('API_KEYS', 'APP_ID')
API_KEY = config.get('API_KEYS', 'API_KEY')

# Access authentication details
AUTH_USERNAME = config.get('AUTH', 'username')
AUTH_PASSWORD = config.get('AUTH', 'password')

GENDER = "male"
WEIGHT_KG = 66
HEIGHT_CM = 179
AGE = 17

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint="https://api.sheety.co/8358d87b69e9484e10374d4a728aaa27/workoutTracking/workouts"
exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}


parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)
#POST A ROW
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Basic Authentication
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        auth=(AUTH_USERNAME, AUTH_PASSWORD)
    )


    print(sheet_response.text)
