import requests
import json

#print("Welcome to kitsu")

#api_url = "https://kitsu.io/api/edge/anime?filter[text]=academia"

#api_url = "https://kitsu.io/api/edge/anime/11469/castings"

api_url = "https://kitsu.io/api/edge/anime/11469/anime-characters"

#api_url = "https://kitsu.io/api/edge/anime-characters/26108/castings"

#api_url = "https://kitsu.io/api/edge/anime-castings/61060/person"

#api_url = "https://kitsu.io/api/edge/anime-castings/61060/anime-character"

#api_url = "https://kitsu.io/api/edge/anime-characters/26108/character"  # Actual Character

response = requests.get(api_url)
json_response = json.loads(response.text)
animu = json_response["data"]

def url_to_dict(url):
    print("Fetching " + url)
    response = requests.get(url)
    if response.ok:
        json_response = json.loads(response.text)
        return json_response["data"]
    return None

def print_json(dict):
    json_object = json.dumps(dict, indent=4)
    print(json_object)

for character in animu:
    #print("\n\nI LOVE RACHIE\n\n")

    char_url = character["relationships"]["character"]["links"]["related"]
    char_data = url_to_dict(char_url)
    print_json(char_data)

    castings = url_to_dict(char_data["relationships"]["castings"]["links"]["related"])
    for casting in castings:
        print_json(url_to_dict(casting["relationships"]["character"]["links"]["related"]))
        print_json(url_to_dict(casting["relationships"]["person"]["links"]["related"]))

    exit(0)


#print(animu["attributes"]["titles"]["ja_jp"])
#print(animu["attributes"]["posterImage"]["large"])