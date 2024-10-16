# how to fetch a single request? (the API is a link to the database)
# example: i want information to the series naruto
# 


# app.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Serve the homepage
@app.route('/')
def index():
    return render_template('index.html')


# this handles the API call with the info from javascript
# Route to search for anime using the Jikan API
@app.route('/search_anime', methods=['GET'])
def search_anime():
    anime_name = request.args.get('anime')  # Get anime name from the query string
    api_url = f"https://api.jikan.moe/v4/anime?q={anime_name}"

    # Make the API request
    response = requests.get(api_url)
    anime_data = response.json()  # Parse the JSON response

    return jsonify(anime_data)  # Return the data as JSON to the frontend, converts python data into jason format which javascript will receive


if __name__ == '__main__':
    app.run(debug=True)

