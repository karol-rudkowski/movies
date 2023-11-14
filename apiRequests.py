import config
import requests


def searchTitle(title: str):
    url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/" + title

    querystring = {"exact": "false"}

    headers = {
        "X-RapidAPI-Key": config.rapidApiKey,
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        raise ConnectionError("Error: " + str(response.status_code))

    return response.json()


def getImage(url: str):
    response = requests.get(url)

    if response.status_code != 200:
        raise ConnectionError("Error: " + str(response.status_code))

    return response.content

def getRandomMovies():
    url = "https://moviesdatabase.p.rapidapi.com/titles/random"

    querystring = {"list": "most_pop_movies"}

    headers = {
        "X-RapidAPI-Key": config.rapidApiKey,
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        raise ConnectionError("Error: " + str(response.status_code))

    return response.json()