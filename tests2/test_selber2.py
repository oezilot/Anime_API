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
