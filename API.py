import requests
import json
from conf import API_Weather


def weather():
    City_Name = 'Kazan'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={City_Name}&appid={API_Weather}&units=metric"
    response = requests.get(url)
    converted = json.loads(response.text)
    res = {"Temperature": converted['main']['feels_like'], "Status": converted["weather"][0]["main"],
           "Wind_Speed": converted["wind"]["speed"]}
    return res
