import pytest
from flask import session
from selber2 import app2

# setting up a test client for form submissions (setting up a fake session too???)
# test_client (= methode) bildet eine test-umgebung von dem test-client-object erzeigt...erlaubt https anfragen zustellen ohne den echten browser/server zu benützen müssen
@pytest.fixture
def client():
    app2.config["TESTING"] = True
    with app2.test_client() as client:
        with app2.app_context():
            yield client

# ist es be integration tests üblich dass man eine funktion macht zum testen mehrerer applicationsfunktionen?
def test_update_session_and_pagination(client):
    # initialize the session (initial_title, initial_genre are placeholders dor the actual session data)...die session hier zu initialisieren ist unnötig?!!
    with client.session_transaction() as sess:
        sess['params'] = {"q": "initial_title", "genres": "initial_genre"}
        sess['page'] = 3  # Start on page 3 to test if pagination and filters reset properly

    # simulate data for the POST-request
    # die key-names müssen den namen der forms entsprechen
    form_data = {
        "param_title":"naruto",
        "param_genre":"1"
    }

    # simulate the POST-request: der client postet das form_data an die funktion update_session
    response = client.post('/update_session', data=form_data, follow_redirects=True)

    # check if the session was correclty updated (with client)
    with client.session_transaction() as sess:
        assert sess['params']['q'] == "naruto"
        assert sess['params']['genres'] == "1"
        # pagination (pagereset with the refresh)
        assert sess['page'] == 1 # muss man das nicht seperat in einem unittest testen???

    # wo wird gesagt was der aktuelle sessionwert für die page ist? es wird ja nicht jedes mal wenn die page geändert wird auch die filters geändert...(müsste man nicht allgemein eine session zu beginn simulieren?!)
    client.post('/inc', follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess['page'] == 2

    client.post('/dec' ,follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess['page'] == 1 # man geht hier davon aus dass man von der page 2 decrementiert

    # muss man hier testen ob die pagination unter 1 geht?... der button wird in diesem szenario gar nicht dargestellt!

    # verify the reset
    assert response.status_code == 200




    
    