import pytest
from flask import session
from selber2 import app2

# setting up a test client for form submissions (setting up a fake session too???)
@pytest.fixture
def client():
    app2.config["TESTING"] = True
    with app2.test_client as client:
        with app2.app_context():
            yield client


def test_update_session():
    # simulate data for the POST-request
    form_data = {
        "q":"naruto",
        "genres":"1"
    }

    # simulate the POST-request: der client postet doe form_data an die funktion update_session
    response = client.post('update_session', data=form_data, follow_redicrects=True)

    # check if the session was correclty updated (with client)
    with client.session_transaction() as sess:
        assert sess['params']['q'] == "naruto"
        assert sess['params']['genres'] == "1"

    # verify the reset
    assert response.status_code == 200