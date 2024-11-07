import pytest
from flask import session
from unittest.mock import patch, MagicMock
from selber2 import app2, fetch_animes

@pytest.fixture
def client():
    app2.config["TESTING"] = True
    with app2.test_client() as client:
        with app2.app_context():
            yield client

@patch('selber2.fetch_animes')
def test_update_session_and_pagination(mock_fetch_animes, client):
    # Mock API response with pagination data for upper bound limit
    mock_fetch_animes.return_value = {
        "message": "Data fetched successfully",
        "data": [{"title": "Naruto"}],
        "status": "success",
        "pagination": {
            "has_next_page": True,
            "last_visible_page": 5  # Mocked last visible page for boundary testing
        }
    }

    # Simulate form data for updating session
    form_data = {
        "param_title": "naruto",
        "param_genre": "1"
    }
    response = client.post('/update_session', data=form_data, follow_redirects=True)

    # Check if session was correctly updated with parameters
    with client.session_transaction() as sess:
        assert sess['params']['q'] == "naruto"
        assert sess['params']['genres'] == "1"
        assert sess['page'] == 1  # Ensure page resets to 1 on form submission

    # Test incrementing page up to last_visible_page
    for _ in range(5):
        client.post('/inc', follow_redirects=True)

    # Verify page is at last_visible_page
    with client.session_transaction() as sess:
        assert sess['page'] == 5  # Page should reach but not exceed last_visible_page

    # Attempt to increment beyond last_visible_page
    client.post('/inc', follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess['page'] == 5  # Page should remain at last_visible_page

    # Test decrementing back to 1
    for _ in range(5):
        client.post('/dec', follow_redirects=True)

    with client.session_transaction() as sess:
        assert sess['page'] == 1  # Page should not go below 1

    # Verify response status code to ensure the page loads successfully
    assert response.status_code == 200
