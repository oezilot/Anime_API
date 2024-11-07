# das ziel beim testen ist die print statements im eigentlichen code in tests umzuwandeln!
# beim testen sollte man immer alle arten von tests für die selbe application machen (unit, functional, integration)
# folgendes muss man testen: mocking API request, mocking a client using the interface of the application, testing if there is any data and what happens if there is none (ich will tests auf eine art machn sodass ich einen bestimmten test mehrmals mit verschiedenen random zahlen durchgeführt wird!)
# --> 2 sachen können none sein: die daten der request wegen den paramtern oder weil die parameter udn page none sind

import requests
import pytest
from selber2 import app2, url_animes, fetch_animes  # Stelle sicher, dass der Pfad zur App korrekt ist
from unittest.mock import patch, MagicMock # genutzt für das mocken des api-calls

# =================== Session simulieren =====================
# arrange (session simulieren)...dieser teil wird gar nicht genutzt
@pytest.fixture
def client():
    app2.config["TESTING"] = True
    with app2.test_client as client:
        with client.session_transaction() as session:
            session["params"] = {
                "q": "naruto",
                "genres": "4"
            }
            session["page"] = 1


# =================== URL-Builder Function (4 Tests-Functions )=====================
# test url-builder function with various inputs (different scenarios)

# random werte für params und page
def test_url_animes_filled():
    # arrange
    page = 2
    params = {
        "q":"naruto",
        "genres":"4"
    }
    # act
    result_api_url = url_animes(page, params) # als input werden automatisch die sessiondaten verwendet?

    # prints
    print(f"session_page = {page}, session_params = {params}") # input
    print(f"result_api_url = {result_api_url}") # output

    # assert
    assert result_api_url == "https://api.jikan.moe/v4/anime?page=2&q=naruto&genres=4"

# defaultwerte page und params wenn nicht spezifiziert wurde (= das form wurde nicht abgeschickt!)
def test_url_animes_default():
    page = 1
    params = {}
    results_api_url = url_animes(page, params)
    assert results_api_url == "https://api.jikan.moe/v4/anime?page=1&"

# wenn params-dictionary leer ist (bei der filtersuche würde man dan nach allen ergebnissen suchen)
def test_url_animes_emptyP():
    page = 1
    params = {
        "q":"",
        "genres":""
    }

    result_api_url = url_animes(page, params) # als input werden automatisch die sessiondaten verwendet?

    print(f"session_page = {page}, session_params = {params}, result_api_url = {result_api_url}") # input

    assert result_api_url == "https://api.jikan.moe/v4/anime?page=1&q=&genres="

# spezielle characters wie abstände oder prozentzeichen
def test_url_animes_specialC():
    page = 1
    params = {
        "q":"tokyo ghoul %",
        "genres":""
    }

    result_api_url = url_animes(page, params) # als input werden automatisch die sessiondaten verwendet?

    print(f"session_page = {page}, session_params = {params}, result_api_url = {result_api_url}") # input

    assert result_api_url == "https://api.jikan.moe/v4/anime?page=1&q=tokyo+ghoul+%25&genres="


# =================== Fetchen und API-call (4 Test-Functions) =====================
# den api call mocken, das requests-modul der application mocken!
# für jedes szenario einen seperaten test 
# hätte man beim testen nicht eifach blos auf die messaage im return der aplllikation schauen sollen?
import pytest
from unittest.mock import patch, MagicMock
import requests
from app2 import fetch_animes  # Stelle sicher, dass du auf die Funktion zugreifst, ohne auf Module zurückzugreifen


# =================== TEST 1: Fetch Anime Success ====================
@patch('app2.requests.get')  # Mock the requests.get function
def test_fetch_animes_success(mock_get):
    # Mock the API response
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
                {'mal_id': 4, 'type': 'anime', 'name': 'Comedy', 'url': 'https://myanimelist.net/anime/genre/4/Comedy'},
                {'mal_id': 41, 'type': 'anime', 'name': 'Suspense', 'url': 'https://myanimelist.net/anime/genre/41/Suspense'}
            ]
        }]
    }
    mock_get.return_value = mock_response  # Replaces the requests.get method

    # Call the function under test
    result = fetch_animes()

    # Check pagination data
    assert result['pagination']['has_next_page'] == False
    assert result['pagination']['last_visible_page'] == 1

    # Check the data (list of anime dictionaries)
    assert len(result['data']) == 1
    assert result['data'][0]['title'] == 'Kakegurui Picture Drama'
    assert result['data'][0]['type'] == 'Special'
    assert 'Comedy' in [genre['name'] for genre in result['data'][0]['genres']]
    assert 'Suspense' in [genre['name'] for genre in result['data'][0]['genres']]


# =================== TEST 2: Fetch Anime No Data ====================
@patch('app2.requests.get')  # Mock the requests.get function
def test_fetch_animes_nodata(mock_get):
    # Mock response for no data
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [],
        "pagination": {
            "current_page": 1,
            "has_next_page": False,
            "total_pages": 1
        }
    }
    mock_get.return_value = mock_response

    # Call the function under test
    result = fetch_animes()
    
    # Assert error message for no data
    assert result['message'] == "No Anime Data Found"
    assert len(result['data']) == 0


# =================== TEST 3: Fetch Anime Error 404 ====================
@patch('app2.requests.get')  # Mock the requests.get function
def test_fetch_animes_error404(mock_get):
    # Mock response for 404 error
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    # Call the function under test
    result = fetch_animes()

    # Assert error message for 404 error
    assert result['message'] == "Error fetching data: 404"
    assert len(result['data']) == 0


# =================== TEST 4: Fetch Anime Exception ====================
@patch('app2.requests.get')  # Mock the requests.get function
def test_fetch_animes_exception(mock_get):
    # Simulate a request exception (e.g., network failure)
    mock_get.side_effect = requests.RequestException("Network Error")

    # Call the function under test
    result = fetch_animes()

    # Assert error message for request exception
    assert result['message'] == "Request failed: Network Error"
    assert len(result['data']) == 0


# TESTS: das muss man tzesten:

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

fetch data:
- testen ob der api-call erfolgreich gemacht wurde (eception)..existiert der api-url überhaut?
- testen ob eine erfolgreiche response generiert wurde/gefetched
- testen ob daten überhaupt existieren
'''

'''
fragen:
- alle arten von tests machen?
- für jede function einen test
- auch das testen was gar nicht auftreten kann
- wie arbeiten die verschiedenen funktionen miteinander wenn ich alles mit unittests teste
'''
# FRAGE: muss ich sachen testen die eh nicht vorkommen wie zum beisiel der fall dass page -2 ist wenn das nicht vorkommen kann


# so runne ich das test-file wenn mehrere test-ordner existieren: pytest ordner/file.py
# bestimmter test innerhalb des files testen: pytest ordner/file.py::test_example (-s zeigt alle print ausgaben auch die von der applikation)