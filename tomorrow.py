import requests
import dotenv, os

#39.254520, -76.709507

url = "https://api.tomorrow.io/v4/timelines"

querystring = {
"location":"39.254520, -76.709507",
"fields":["temperature", "cloudCover", "sunsetTime"],
"units":"metric",
"timesteps":"1d",
"apikey":os.getenv("tomorrowAPIKey")}

response = requests.request("GET", url, params=querystring)
print(response.text)

