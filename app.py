from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    
    anime_results = None

    anime_name = request.form.get('searchbar')  # Get the name the user searched for in the search bar
    
    # if search bar has a value
    if anime_name:
        api_name = f"https://api.jikan.moe/v4/anime?q={anime_name}"
        response_name = requests.get(api_name)

        if response_name.status_code == 200:
            anime_data = response_name.json()  # Parse JSON response
            anime_results = anime_data['data']  # Contains all anime results with the name
            print(anime_results[1]['title'])
            return render_template('results.html', anime_results=anime_results)
        else:
            return "Error fetching data from API", 500


    else:  # if search bar is empty, display all anime
        api_all = f"https://api.jikan.moe/v4/anime"
        response_all = requests.get(api_all)

        if response_all.status_code == 200:
            anime_data = response_all.json()  # Parse JSON response
            anime_results = anime_data['data']  # Contains all anime results
            print(anime_results[2]['title'])
            return render_template('results.html', anime_results=anime_results)
        else:
            return "Error fetching data from API", 500
            

if __name__ == '__main__':
    app.run(debug=True)
