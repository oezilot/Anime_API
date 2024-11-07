# Arrange, Act, Assert (AAA-method)

import pytest
from flask import session
from unittest.mock import patch, MagicMock
import requests
from selber2 import app2, url_animes, fetch_animes  # Correct module import

# =================== Set up a test client fixture =====================
@pytest.fixture
def client():
    app2.config["TESTING"] = True
    with app2.test_client() as client:
        with app2.app_context():
            yield client


# =================== Tests for URL Builder Function =====================
# Test url_animes with various inputs

def test_url_animes_filled():
    """Test url_animes with specific page and filled params."""
    page = 2
    params = {
        "q": "naruto",
        "genres": "4"
    }
    result_api_url = url_animes(page, params)
    assert result_api_url == "https://api.jikan.moe/v4/anime?page=2&q=naruto&genres=4"


def test_url_animes_default():
    """Test url_animes with default page and empty params."""
    page = 1
    params = {}
    result_api_url = url_animes(page, params)
    assert result_api_url == "https://api.jikan.moe/v4/anime?page=1&"


def test_url_animes_empty_params():
    """Test url_animes with empty params for all results."""
    page = 1
    params = {
        "q": "",
        "genres": ""
    }
    result_api_url = url_animes(page, params)
    assert result_api_url == "https://api.jikan.moe/v4/anime?page=1&q=&genres="


def test_url_animes_special_chars():
    """Test url_animes with special characters in query params."""
    page = 1
    params = {
        "q": "tokyo ghoul %",
        "genres": ""
    }
    result_api_url = url_animes(page, params)
    assert result_api_url == "https://api.jikan.moe/v4/anime?page=1&q=tokyo+ghoul+%25&genres="


# =================== Tests for fetch_animes Function =====================
# Mock API responses to test fetch_animes with different scenarios

@patch('selber2.requests.get')  # Mock the requests.get function
def test_fetch_animes_success(mock_get, client):
    """Test fetch_animes with a successful API response and data returned."""
    with app2.test_request_context('/'):
        with client.session_transaction() as sess:
            sess["page"] = 1
            sess["params"] = {
                "q": "naruto",
                "genres": "4"
            }

        # Mock successful API response with data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'pagination': {
                'has_next_page': False,
                'last_visible_page': 1,
            },
            'data': [{
                'title': 'Kakegurui Picture Drama',
                'type': 'Special',
                'genres': [
                    {'mal_id': 4, 'type': 'anime', 'name': 'Comedy'},
                    {'mal_id': 41, 'type': 'anime', 'name': 'Suspense'}
                ]
            }]
        }
        mock_get.return_value = mock_response  # Replace requests.get with mock

        # Call the function under test
        result = fetch_animes()

        # Assertions
        assert result['pagination']['has_next_page'] == False
        assert result['pagination']['last_visible_page'] == 1
        assert len(result['data']) == 1
        assert result['data'][0]['title'] == 'Kakegurui Picture Drama'
        assert 'Comedy' in [genre['name'] for genre in result['data'][0]['genres']]
        assert 'Suspense' in [genre['name'] for genre in result['data'][0]['genres']]


@patch('selber2.requests.get')
def test_fetch_animes_no_data(mock_get, client):
    """Test fetch_animes when no data is returned from the API."""
    with app2.test_request_context('/'):
        with client.session_transaction() as sess:
            sess["page"] = 1
            sess["params"] = {
                "q": "naruto",
                "genres": "4"
            }

        # Mock response with no data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [],
            "pagination": {
                "has_next_page": False,
                "last_visible_page": 1
            }
        }
        mock_get.return_value = mock_response

        # Call the function under test
        result = fetch_animes()

        # Assertions for empty data and pagination structure
        assert result['message'] == "No Anime Data Found"
        assert result['data'] == []
        assert result['pagination']['has_next_page'] == False


@patch('selber2.requests.get')
def test_fetch_animes_error404(mock_get, client):
    """Test fetch_animes handling a 404 error from the API."""
    with app2.test_request_context('/'):
        with client.session_transaction() as sess:
            sess["page"] = 1
            sess["params"] = {
                "q": "naruto",
                "genres": "4"
            }

        # Mock response for a 404 error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Call the function under test
        result = fetch_animes()

        # Assert error message for 404 response
        assert result['message'] == "Error fetching data: 404"
        assert result['data'] == []


@patch('selber2.requests.get')
def test_fetch_animes_exception(mock_get, client):
    """Test fetch_animes handling a network failure exception."""
    with app2.test_request_context('/'):
        with client.session_transaction() as sess:
            sess["page"] = 1
            sess["params"] = {
                "q": "naruto",
                "genres": "4"
            }

        # Simulate a network failure
        mock_get.side_effect = requests.RequestException("Network Error")

        # Call the function under test
        result = fetch_animes()

        # Assert error message for exception
        assert result['message'] == "Request failed: Network Error"
        assert result['data'] == []
