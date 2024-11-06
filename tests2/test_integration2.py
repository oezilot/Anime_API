import pytest
from flask import session
from selber2 import app2

# setting up a test client for form submissions (setting up a fake session too???)
# test_client (= methode) bildet eine test-umgebung von dem test-client-object erzeigt...erlaubt dem server https anfragen zustellen ohne den echten browser zu benützen müssen
@pytest.fixture
def client():
    app2.config["TESTING"] = True
    with app2.test_client() as client:
        with app2.app_context():
            yield client


def test_update_session(client):
    # simulate data for the POST-request
    form_data = {
        "q":"naruto",
        "genres":"1"
    }

    # simulate the POST-request: der client postet doe form_data an die funktion update_session
    response = client.post('update_session', data=form_data, follow_redirects=True)

    # check if the session was correclty updated (with client)
    with client.session_transaction() as sess:
        assert sess['params'].get('q') == form_data.get('param_title')
        assert sess['params'].get('genres') == form_data.get('param_genre')


    # verify the reset
    assert response.status_code == 200