# how tests work: with this file i can create a client which simulated requests to my application and sends errormessages back if something has failed!
# contains fixtures and configurations for testing (arguments for testing)

import pytest
from selber import app #selber is tha name of the applivation: selber.py

# creating a client
@pytest.fixture
def client():
    app.config['TESTING'] = True #sends helpful messages for debugging
    with app.test_client() as client:
        yield client

# test clients?

# yield



