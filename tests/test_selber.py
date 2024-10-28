# assert: checking if something is equal

# check if response == 200
def test_home_page(client):
    # Use the client fixture to make a GET request to the homepage
    response = client.get('/')
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


# check homepage-data, what does the html display?





# check session
# check api_url
# check if data exists
