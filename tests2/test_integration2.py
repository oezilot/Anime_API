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
    

# simulate POST-request

# check if the session was correclty updated