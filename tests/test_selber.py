# assert: checking if something is equal
# all test-functions need to have the prefix test_... ind their function-name!!!

# check if response == 200
def test_home_page(client):
    # Use the client fixture to make a GET request to the homepage
    response = client.get('/')
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


# check if homepage render expected content (mal nur den content und nicht schon die funktionalität der elemente prüfen)
def test_homepage_content(client):
    response = client.get('/')

    # Check if the content includes specific text
    assert b"Anime Search" in response.data # b stands for bytes

    # checks the resence of the form-elements (the 5 different parameters)
    assert b'<input type="text" name="parameter_title"' in response.data
    assert b'<select name="parameter_genre"' in response.data
    assert b'<select name="parameter1"' in response.data
    assert b'<select name="parameter2"' in response.data
    assert b'<select name="parameter3"' in response.data

    # Check for anime data placeholders
    assert b'Title:' in response.data
    assert b'Type:' in response.data
    assert b'Status:' in response.data
    assert b'Rating:' in response.data
    assert b'Genre:' in response.data
    #checking for images doesnt work because of the dynamic image.url?!
    #assert b'<img src=""' in response.data
    #assert b'images.jpg.image_url' in response.data  # Checks that the specific part of the image URL is included


# check form.submission and storage in the session of that information
def test_parameters_submission(client):
    # Simulate a POST request with form data (zum ausprobieren mal nur irgend ein beispiel simulieren)
    response = client.post('/parameters', data={
        'parameter1': 'tv',
        'parameter2': 'airing',
        'parameter3': 'pg13',
        'parameter_title': 'Naruto',
        'parameter_genre': '1'
    }, follow_redirects=True)

    # Check if the response status code is 200 (redirect successful)
    assert response.status_code == 200

    # assert that the data stored in the session is what was posted in the form submission
    # Access the session data to verify parameters are stored correctly (= verify session data)
    with client.session_transaction() as session:
        assert session['params']['type'] == 'tv'
        assert session['params']['status'] == 'airing'
        assert session['params']['rating'] == 'pg13'
        assert session['params']['q'] == 'Naruto'
        assert session['params']['genres'] == '1'





# check session
# check api_url
# check if data exists
