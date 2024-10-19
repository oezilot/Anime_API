from flask import Flask, render_template, request
import requests

app = Flask(__name__)

JIKAN_API_URL = 'https://api.jikan.moe/v4/anime'

@app.route('/')
def index():
    # Get parameters from request
    page = request.args.get('page', 1, type=int)
    anime_type = request.args.get('anime_type', '', type=str)

    # Build the query string
    query = {
        'page': page,
        'type': anime_type if anime_type else None  # Filter anime type if selected
    }

    # Fetch data from Jikan API
    response = requests.get(JIKAN_API_URL, params=query)
    data = response.json()

    # Extract anime list and pagination info
    anime_list = data.get('data', [])
    pagination = data.get('pagination', {})

    return render_template('index.html', anime_list=anime_list, pagination=pagination, anime_type=anime_type)


if __name__ == '__main__':
    app.run(debug=True)
