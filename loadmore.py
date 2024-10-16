from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Function to fetch a specific page of anime data
def fetch_anime_page(page):
    api_url = f"https://api.jikan.moe/v4/anime?page={page}"
    response = requests.get(api_url)

    if response.status_code == 200:
        anime_data = response.json()
        return anime_data['data']  # Returns anime data for the current page
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def search():
    page = int(request.form.get('page', 1))  # Get the current page number, default to 1
    anime_results = []  # To store the anime results
    
    # Fetch the current page of anime data
    anime_data = fetch_anime_page(page)
    
    if anime_data:
        anime_results.extend(anime_data)  # Add current page data to the results

    return render_template('results.html', anime_results=anime_results, next_page=page+1)

if __name__ == '__main__':
    app.run(debug=True)
