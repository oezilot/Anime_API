# das ziel beim testen ist die print statements im eigentlichen code in tests umzuwandeln!
# folgendes muss man testen: mocking API request, mocking a client using the interface of the application, testing if there is any data and what happens if there is none (ich will tests auf eine art machn sodass ich einen bestimmten test mehrmals mit verschiedenen random zahlen durchgeführt wird!)
# --> 2 sachen können none sein: die daten der request wegen den paramtern oder weil die parameter udn page none sind

import pytest
from selber2 import app2, url_animes, url_anime, url_characters  # Stelle sicher, dass der Pfad zur App korrekt ist


#============ URL BUILDER FUNKTIONEN =============
# spezialfälle: leere werte, negative/zu grosse pages (werden die default-werte richtig angewendet?)

# Test für die URL-Builder-Funktion url_animes
def test_url_animes():
    page = 1
    params = {
        "param1": "type",
        "param2": 3
    }
    expected_url = "https://api.jikan.moe/v4/anime?page=1&param1=type&param2=3"
    assert url_animes(page, params) == expected_url

# Test für die URL-Builder-Funktion url_anime
def test_url_anime():
    anime_id = 1
    expected_url = "https://api.jikan.moe/v4/anime/1"
    assert url_anime(anime_id) == expected_url

# Test für die URL-Builder-Funktion url_characters
def test_url_characters():
    anime_id = 1
    expected_url = "https://api.jikan.moe/v4/anime/1/characters"
    assert url_characters(anime_id) == expected_url


# TESTS: das muss man resten:

# client simulieren der die application bedient
# session simulieren mit sample session (nur einmal definieren und immer diese session verwenden)
# url-biulder-function (sample session)
# API-call simulieren sumulieren (sample api-urls)
# session correctly updated (pagination, filters, default values)
# buttons displayed correctly ()
# existieren die daten, dara correctly fetched???...return-dictionary simulieren?!


'''
session tests:
- session inizialised correctly? (default session)
- session updated correctly? (filters)

url-builder-function: (bei den tests immer noch das resultat ausprinten umd mit mehreren verschiedenen inputs testen die random generiert werden)
- url_animes()-function with an empty session (empty params)
- url-animes()-function with random session values (page, params)
- url-builder-function() mit speziellen characters für das value 'q'

fetch data:
- testen ob der api-call erfolgreich gemacht wurde (eception)..existiert der api-url überhaut?
- testen ob eine erfolgreiche response generiert wurde/gefetched
- testen ob daten überhaupt existieren
'''


# FRAGE: muss ich sachen testen die eh nicht vorkommen wie zum beisiel der fall dass page -2 ist wenn das nicht vorkommen kann
