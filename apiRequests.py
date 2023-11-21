import config
import requests


def searchTitle(title: str):
    url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/" + title

    querystring = {"info": "base_info", "exact": "false"}

    headers = {
        "X-RapidAPI-Key": config.rapidApiKey,
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        raise ConnectionError("Search request Error: " + str(response.status_code))

    return response.json()


def getImage(url: str):
    response = requests.get(url)

    if response.status_code != 200:
        raise ConnectionError("Get image request Error: " + str(response.status_code))

    return response.content


def getRandomMovies(list: str):
    url = "https://moviesdatabase.p.rapidapi.com/titles/random"

    querystring = {"info": "base_info", "list": list}

    headers = {
        "X-RapidAPI-Key": config.rapidApiKey,
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        raise ConnectionError("Get random movies request Error: " + str(response.status_code))
    elif response.json()['results'] is None:
        return []

    return response.json()


def getLists():
    url = "https://moviesdatabase.p.rapidapi.com/titles/utils/lists"

    headers = {
        "X-RapidAPI-Key": config.rapidApiKey,
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ConnectionError("Get lists request Error: " + str(response.status_code))

    return response.json()
