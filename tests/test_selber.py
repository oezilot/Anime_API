# assert: checking if something is equal

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








# check session
# check api_url
# check if data exists
