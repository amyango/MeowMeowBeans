import requests
import json
import urllib


def print_json(dict):
    json_object = json.dumps(dict, indent=4)
    print(json_object)

def test_animu():
    API_URL = "https://api.jikan.moe/v4/anime"

    payload = dict(q='my hero', limit=10, order_by="popularity", sort = "asc", type="tv")
    urllib.parse.urlencode(payload)

    response = requests.get(API_URL, params=payload)
    json_response = json.loads(response.text)
    animu = json_response["data"]

    for anime in animu:
        if anime["popularity"] != 0:
            break

    print(anime["title"])

    print_json(animu)
    print(animu[0]["title_english"])
    mal_id = animu[0]["mal_id"]

    print(mal_id)
    char_url = API_URL + "/" + str(mal_id) + "/characters"
    response = requests.get(char_url)
    json_response = json.loads(response.text)
    char = json_response["data"]
    print_json(char)

def test_va():
    people_url = "https://api.jikan.moe/v4/people"
    payload = dict(q='masuda toshiki', limit=1)
    urllib.parse.urlencode(payload)

    response = requests.get(people_url, params=payload)
    json_response = json.loads(response.text)
    person = json_response["data"]

    print_json(person)

test_va()

#test_animu()

exit(0)

