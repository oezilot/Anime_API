# test_unit.py
import pytest
from selber2 import url_animes

# Test url_animes with various inputs

def test_url_animes_filled():
    page = 2
    params = {
        "q": "naruto",
        "genres": "4"
    }
    result_api_url = url_animes(page, params)
    assert result_api_url == "https://api.jikan.moe/v4/anime?page=2&q=naruto&genres=4"

def test_url_animes_default():
    page = 1
    params = {}
    result_api_url = url_animes(page, params)
    assert result_api_url == "https://api.jikan.moe/v4/anime?page=1&"

def test_url_animes_empty_params():
    page = 1
    params = {
        "q": "",
        "genres": ""
    }
    result_api_url = url_animes(page, params)
    assert result_api_url == "https://api.jikan.moe/v4/anime?page=1&q=&genres="

def test_url_animes_special_chars():
    page = 1
    params = {
        "q": "tokyo ghoul %",
        "genres": ""
    }
    result_api_url = url_animes(page, params)
    assert result_api_url == "https://api.jikan.moe/v4/anime?page=1&q=tokyo+ghoul+%25&genres="
