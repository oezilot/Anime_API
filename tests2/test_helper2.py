# das ziel beim testen ist die print statements im eigentlichen code in tests umzuwandeln!
# beim testen sollte man immer alle arten von tests für die selbe application machen (unit, functional, integration)
# folgendes muss man testen: mocking API request, mocking a client using the interface of the application, testing if there is any data and what happens if there is none (ich will tests auf eine art machn sodass ich einen bestimmten test mehrmals mit verschiedenen random zahlen durchgeführt wird!)
# --> 2 sachen können none sein: die daten der request wegen den paramtern oder weil die parameter udn page none sind

import pytest
from selber2 import app2, url_animes  # Stelle sicher, dass der Pfad zur App korrekt ist


# =================== Session simulieren =====================
# arrange (session simulieren)
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


# =================== URL-Builder Function =====================
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