# how tests work: with this file i can create a client which simulated requests to my application and sends errormessages back if something has failed!
# contains fixtures and configurations for testing (arguments for testing)

import pytest
from unittest.mock import patch
from selber import app #selber is tha name of the applivation: selber.py (hier kann man noch funktionen einfügen theoretisch)

# creating a client
@pytest.fixture
def client():
    app.config['TESTING'] = True #sends helpful messages for debugging
    with app.test_client() as client:
        yield client
    
@pytest.fixture(autouse=True)
def mock_requests_get():
    with patch('requests.get') as mock_get:
        # Standardantwort für alle Tests festlegen (kann je nach Test angepasst werden)
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": [],  # Standardmäßig leere Daten
            "pagination": {}
        }
        yield mock_get


