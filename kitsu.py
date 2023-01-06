import requests
import json

print("Welcome to kitsu")

api_url = "https://kitsu.io/api/edge/anime?filter[text]=academia"

response = requests.get(api_url)
json_response = json.loads(response.text)
animu = json_response["data"][0]

print(animu["attributes"]["titles"]["ja_jp"])
print(animu["attributes"]["posterImage"]["large"])