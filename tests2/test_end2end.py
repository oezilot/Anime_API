# eror: the mock is not applied properly..why??!
# test_e2e.py
import pytest
from flask import session
from unittest.mock import patch, MagicMock
from selber2 import app2, fetch_animes  # Import the app and functions

@pytest.fixture
def client():
    app2.config["TESTING"] = True
    with app2.test_client() as client:
        with app2.app_context():
            yield client

@patch('selber2.requests.get')  # Mock requests.get to simulate API call inside fetch_animes
def test_e2e_user_flow(mock_get, client):
    """
    E2E Test simulating a full user journey, from form submission to pagination.
    """
    # Step 1: Define a sample response JSON that simulates API data
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Data fetched successfully",
        "data": [
            {"title": "Naruto", "type": "TV", "genres": [{"name": "Action"}, {"name": "Adventure"}]},
            {"title": "One Piece", "type": "TV", "genres": [{"name": "Action"}, {"name": "Adventure"}]}
        ],
        "pagination": {
            "has_next_page": True,
            "last_visible_page": 5
        }
    }
    mock_get.return_value = mock_response

    # Step 2: Simulate form submission to update session with search filters
    form_data = {
        "param_title": "naruto",
        "param_genre": "1"
    }
    response = client.post('/update_session', data=form_data, follow_redirects=True)

    # Check session update after form submission
    with client.session_transaction() as sess:
        assert sess['params']['q'] == "naruto"
        assert sess['params']['genres'] == "1"
        assert sess['page'] == 1  # Page should reset to 1

    # Step 3: Verify initial data is displayed correctly
    # Call fetch_animes to get the mock data
    result = fetch_animes()  # This call should now use the mocked response from requests.get

    # Assertions to check the behavior of fetch_animes with the mock data
    assert result["message"] == "Data fetched successfully"
    assert result["pagination"]["has_next_page"] == True
    assert result["pagination"]["last_visible_page"] == 5  # This should now pass
    assert len(result["data"]) == 2
    assert result["data"][0]["title"] == "Naruto"
    assert result["data"][1]["title"] == "One Piece"

    # Step 4: Test pagination - Increment page and check session updates
    for _ in range(4):
        client.post('/inc', follow_redirects=True)

    with client.session_transaction() as sess:
        assert sess['page'] == 5  # Verify page incremented to 5

    # Step 5: Attempt to increment beyond the last page and check limit
    client.post('/inc', follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess['page'] == 5  # Page should stop at last_visible_page

    # Step 6: Test decrementing back to the first page
    for _ in range(5):
        client.post('/dec', follow_redirects=True)

    with client.session_transaction() as sess:
        assert sess['page'] == 1  # Page should not go below 1

    # Final assertions to ensure the response and session are valid
    assert response.status_code == 200




'''
this version did not work: whyyyyyy (apparantily the mocking did not work here...)
# test_e2e.py
import pytest
from flask import session
from unittest.mock import patch, MagicMock
from selber2 import app2, fetch_animes  # Import the app and functions

@pytest.fixture
def client():
    app2.config["TESTING"] = True
    with app2.test_client() as client:
        with app2.app_context():
            yield client

@patch('selber2.fetch_animes')  # Mock fetch_animes directly
def test_e2e_user_flow(mock_fetch_animes, client):
    """
    E2E Test simulating a full user journey, from form submission to pagination.
    """
    # Step 1: Define a sample response JSON that simulates API data
    mock_fetch_animes.return_value = {
        "message": "Data fetched successfully",
        "data": [
            {"title": "Naruto", "type": "TV", "genres": [{"name": "Action"}, {"name": "Adventure"}]},
            {"title": "One Piece", "type": "TV", "genres": [{"name": "Action"}, {"name": "Adventure"}]}
        ],
        "status": "success",
        "pagination": {
            "has_next_page": True,
            "last_visible_page": 5
        }
    }

    # Step 2: Simulate form submission to update session with search filters
    form_data = {
        "param_title": "naruto",
        "param_genre": "1"
    }
    response = client.post('/update_session', data=form_data, follow_redirects=True)

    # Check session update after form submission
    with client.session_transaction() as sess:
        assert sess['params']['q'] == "naruto"
        assert sess['params']['genres'] == "1"
        assert sess['page'] == 1  # Page should reset to 1

    # Step 3: Verify initial data is displayed correctly
    # Call fetch_animes to get the mock data
    result = fetch_animes()  # This call should now use the mocked return value

    # Assertions to check the behavior of fetch_animes with the mock data (am besten nimmt man hier eine response diees mit dem echten api nicht gibt denn dann kann man sehen ob das mocking wirklich funktioniert hat!!!)
    assert result["message"] == "Data fetched successfully"
    assert result["pagination"]["has_next_page"] == True
    assert result["pagination"]["last_visible_page"] == 5
    assert len(result["data"]) == 2
    assert result["data"][0]["title"] == "Naruto"
    assert result["data"][1]["title"] == "One Piece"

    # Increment page until reaching the last visible page
    for _ in range(5):
        client.post('/inc', follow_redirects=True)

    with client.session_transaction() as sess:
        assert sess['page'] == 5  # Page should be at the last_visible_page

    # Attempt to increment beyond the last visible page
    client.post('/inc', follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess['page'] == 5  # Page should not exceed last_visible_page

    # Test decrementing back down to the first page
    for _ in range(5):
        client.post('/dec', follow_redirects=True)

    with client.session_transaction() as sess:
        assert sess['page'] == 1  # Page should not go below 1

    # Final assertions to ensure the response and session are valid
    assert response.status_code == 200
'''