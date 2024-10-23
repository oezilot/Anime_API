# grund-idee: mit get-requests arbeiten
#- wenn man parameter ins form einfüllt verändert das den url der application indem es parameter hinzufügt! (der get-request fügt die parameter hinzu)
#- wenn man nun mit diesen parametern einen api-call machen will müssen diese parameter zuerst aus der applications-url geholt werden um anschliessend der API-url hinzugefügt werden können

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

JIKAN_API_URL = 'https://api.jikan.moe/v4/anime'

@app.route('/')
def index():
    # Get parameters from request
    page = request.args.get('page', 1, type=int)
    anime_type = request.args.get('anime_type', '', type=str) # anime_type is the name of the selection of the form and holds the value for the selected enum

    # Build the query string
    query = {
        'page': page,
        'type': anime_type if anime_type else None  # Filter anime type if selected
    }

    # Fetch data from Jikan API
    response = requests.get(JIKAN_API_URL, params=query)
    data = response.json()

    # Extract anime list and pagination info (seperate dictionaries)
    anime_list = data.get('data', [])
    pagination = data.get('pagination', {})

    return render_template('index.html', anime_list=anime_list, pagination=pagination, anime_type=anime_type)


if __name__ == '__main__':
    app.run(debug=True)
