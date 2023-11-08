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

    return response.json()


def getImage(url: str):
    return requests.get(url).content
