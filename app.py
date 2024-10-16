from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    
    anime_results = None # liste mit den animes die ausgegeben werden

    anime_name = request.form.get('searchbar')  # Get the name the user searched for in the search bar
    
    # falls etwas in die searchbar submittet wurde...
    if anime_name:
        api_name = f"https://api.jikan.moe/v4/anime?q={anime_name}"
        response_name = requests.get(api_name)

        if response_name.status_code == 200:
            anime_data = response_name.json()  # Parse JSON response
            anime_results = anime_data['data']  # enthält alle animes mit dem namen der searchbar
            print(anime_results[1]['title'])
            return render_template('results.html', anime_results=anime_results)
        else:
            return "Error fetching data from API", 500

    # falls nichts in die searchbar submittt wurde...
    else: 
        anime_all = request.form.get('view_all')
        if anime_all:
            api_all = f"https://api.jikan.moe/v4/anime"
            response_all = requests.get(api_all)

            if response_all.status_code == 200:
                anime_data = response_all.json()  # Parse JSON response
                anime_results = anime_data['data']  # enthält alle anime überhaupt
                print(anime_results[2]['title'])
                return render_template('results.html', anime_results=anime_results)
            else:
                return "Error fetching data from API", 500

    # Default rendering if no form action is performed
    return render_template('results.html', anime_results=anime_results)

            

if __name__ == '__main__':
    app.run(debug=True)
