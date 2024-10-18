from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Function for fetching the data with the API for a specific page and filter
def fetch_all(page_number, anime_type=None):

    # Default API URL that displays all anime on a specific page
    api_page = f"https://api.jikan.moe/v4/anime?page={page_number}"

    # If an anime_type is selected, append it to the URL
    if anime_type:
        api_page += f"&type={anime_type}"

    # Fetch the data from the API
    response = requests.get(api_page)

    # Parse the JSON response if successful
    if response.status_code == 200:
        data_json = response.json()  # Parse JSON response
        data = data_json['data']
        return data
    else:
        return []

# Route to display all anime on a specific page
@app.route('/', methods=['GET'])
def all_anime():
    # Get the current page number from the URL query parameters, default to 1
    page_number = int(request.args.get('page', 1))

    # Get the selected anime type from the URL query parameters (if any)
    anime_type = request.args.get('type')

    # Fetch the anime data for the current page and selected type
    data = fetch_all(page_number, anime_type)

    # Render the template with the data and current page number
    return render_template('loadmore.html', data=data, page_number=page_number, selected_type=anime_type)

if __name__ == '__main__':
    app.run(debug=True)
