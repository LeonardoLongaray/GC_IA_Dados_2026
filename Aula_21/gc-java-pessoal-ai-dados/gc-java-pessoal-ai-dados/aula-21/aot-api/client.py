
import requests


BASE_URL = "https://api.attackontitanapi.com"


class Character:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


def get_characters():
    response = requests.get(f"{BASE_URL}/characters")
    response.raise_for_status()

    data = response.json()

    characters = []

    for item in data["results"]:
        character = Character(item["name"])
        characters.append(character)

    return characters


for character in get_characters():
    print(character)
