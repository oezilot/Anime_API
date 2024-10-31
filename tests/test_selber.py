import pytest

#======================= BASIC ROUTE TESTS =======================
#===> HOMEPAGE:
def test_home_page(mock_requests_get, client):
    # Simulate a response with specific data
    mock_requests_get.return_value.json.return_value = {
        "data": [],  # Leere Daten für die Simulation
        "pagination": {}
    }

    response = client.get('/')
    assert response.status_code == 200

#==> CHARACTERPAGE:
def test_character_page(mock_requests_get, client):
    mock_requests_get.return_value.json.return_value = {
        "data": [{"name": "Naruto"}],
        "pagination": {}
    }

    response = client.get('/characters', data={'anime_id':'1', 'anime_title': 'Naruto'}) 
    assert response.status_code == 200

#==> ANIMEPAGE:
def test_anime_page(mock_requests_get, client):
    mock_requests_get.return_value.json.return_value = {
        "data": {"title": "Naruto"},
        "pagination": {}
    }

    response = client.post('/anime', data={'anime_id': 1}) 
    assert response.status_code == 200

#======================= CONTENT DISPLAY =======================
def test_homepage_content(mock_requests_get, client):
    mock_requests_get.return_value.json.return_value = {
        "data": [{"title": "Naruto"}],
        "pagination": {"has_next_page": True, "last_visible_page": 2}
    }

    with client.session_transaction() as session:
        session['page'] = 2

    response = client.get('/')
    assert response.status_code == 200
    assert b"Anime Search" in response.data
    assert b'<input type="text" name="parameter_title"' in response.data
    assert b'<select name="parameter_genre"' in response.data
    assert b'<select name="parameter1"' in response.data
    assert b'<select name="parameter2"' in response.data
    assert b'<select name="parameter3"' in response.data

    # Check pagination buttons based on page availability
    if b"No posts with your filters exist" not in response.data:
        assert b'<button>previous</button>' in response.data
        assert b'<button>next</button>' in response.data
    else:
        assert b'<button>previous</button>' not in response.data
        assert b'<button>next</button>' not in response.data

    assert b'Title:' in response.data
    assert b'Type:' in response.data
    assert b'Status:' in response.data
    assert b'Rating:' in response.data
    assert b'Genre:' in response.data

# Hier kannst du weitere Tests hinzufügen...
