# assert: checking if something is equal

# check if response == 200
def test_home_page(client):
    # Use the client fixture to make a GET request to the homepage
    response = client.get('/')
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


# check if homepage render expected content
def test_homepage_content(client):
    response = client.get('/')

    # Check if the content includes specific text
    assert b"Anime Search" in response.data # b stands for bytes





# check session
# check api_url
# check if data exists
