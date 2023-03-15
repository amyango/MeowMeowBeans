import requests
import json
import urllib

API_URL = "https://api.jikan.moe/v4/anime"

def print_json(dict):
    json_object = json.dumps(dict, indent=4)
    print(json_object)

payload = dict(q='my hero academia', limit=1, order_by="popularity", sort = "asc", type="tv")
urllib.parse.urlencode(payload)

response = requests.get(API_URL, params=payload)
json_response = json.loads(response.text)
animu = json_response["data"]
print_json(animu)
print(animu[0]["title_english"])
mal_id = animu[0]["mal_id"]

print(mal_id)
char_url = API_URL + "/" + str(mal_id) + "/characters"
response = requests.get(char_url)
json_response = json.loads(response.text)
char = json_response["data"]
print_json(char)