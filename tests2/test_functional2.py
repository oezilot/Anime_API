# test_functional.py
import pytest
from unittest.mock import patch, MagicMock
from flask import session
from selber2 import app2, fetch_animes

@pytest.fixture
def client():
    app2.config["TESTING"] = True
    with app2.test_client() as client:
        with app2.app_context():
            yield client

@patch('selber2.requests.get')
def test_fetch_animes_success(mock_get, client):
    # Set up the session within the request context
    with app2.test_request_context('/'):
        with client.session_transaction() as sess:
            sess["page"] = 1
            sess["params"] = {
                "q": "naruto",
                "genres": "4"
            }

        # Mock successful API response
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
        mock_get.return_value = mock_response

        # Call fetch_animes
        result = fetch_animes()

        # Assertions
        assert result['pagination']['has_next_page'] == False
        assert result['pagination']['last_visible_page'] == 1
        assert len(result['data']) == 1
        assert result['data'][0]['title'] == 'Kakegurui Picture Drama'

@patch('selber2.requests.get')
def test_fetch_animes_no_data(mock_get, client):
    # Mock response with no data
    with app2.test_request_context('/'):
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

        result = fetch_animes()
        assert result['message'] == "No Anime Data Found"
        assert result['data'] == []
        assert result['pagination']['has_next_page'] == False

@patch('selber2.requests.get')
def test_fetch_animes_error404(mock_get):
    # Mock response for a 404 error
    with app2.test_request_context('/'):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = fetch_animes()
        assert result['message'] == "Error fetching data: 404"
        assert result['data'] == []

@patch('selber2.requests.get')
def test_fetch_animes_exception(mock_get):
    # Simulate a network failure
    with app2.test_request_context('/'):
        mock_get.side_effect = requests.RequestException("Network Error")

        result = fetch_animes()
        assert result['message'] == "Request failed: Network Error"
        assert result['data'] == []
