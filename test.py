from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# define seperate variables for the sorting?!
# options_for_genres =
# options_for_type =


# page to search for specific anime by their name and filter within this search
@app.route('/', methods=['GET', 'POST'])
def index():
    anime_name = None
    anime_results = None
    sort_by = 'all'  # Default value if no sorting is applied

    if request.method == 'POST':
        anime_name = request.form['anime_name']  # Get the anime name from the form
        sort_by = request.form.get('sort_by', 'all')  # Get the sorting option, default to 'all'

        # API URL for anime search by name
        api_url_anime = f"https://api.jikan.moe/v4/anime?q={anime_name}"
        # mit diesem command kann man schauen was es alles für kathegorien gibt für den anime x: https://api.jikan.moe/v4/anime?q=naruto
        
        # Make the GET request to fetch the anime data
        response = requests.get(api_url_anime)

        if response.status_code == 200:
            anime_data = response.json()
            anime_results = anime_data['data']  # Contains all anime results

            # Apply sorting based on 'sort_by'
            if sort_by == 'series':
                anime_results = [anime for anime in anime_results if anime['type'] == 'TV']
            elif sort_by == 'movies':
                anime_results = [anime for anime in anime_results if anime['type'] == 'Movie']
        else:
            anime_results = []  # Set to an empty list if the request fails

    return render_template("index_test.html", anime_name=anime_name, anime_results=anime_results)


# page to search for all anime using filters
@app.route('/all', methods=['GET', 'POST'])
def all():
    allanime_results = []  # Initialize an empty list to hold anime data


    # API URL for all anime
    api_url_allanime = f"https://api.jikan.moe/v4/anime"
    
    # Make the GET request to fetch the anime data
    response = requests.get(api_url_allanime)
    if response.status_code == 200:
        allanime_data = response.json()
        allanime_results = allanime_data['data']  # Contains all anime results
        print(allanime_data)


    # Pass the results to the template
    return render_template("all.html", allanime_results=allanime_results)



# with each individual anime you hae the possibility to click 2 different buttons:
# - view anime details
# - view character list

# page route for each individual anime
# functions: anime auf watchliste hinzufügen/entfernen, steckbrief

# page route for characters of each individual anime
# actions: view all characters and their steckbrief


if __name__ == '__main__':
    app.run(debug=True)


'''

2 verchiedene Funktionen fürs ausprinten der Daten

def fetch_anime_by_id(anime_id):
    # Construct the URL with the given anime ID
    api_url_anime = f"https://api.jikan.moe/v4/anime/{anime_id}"

    # make the get-request to the API
    response = requests.get(api_url_anime)

    # check if the request was successful
    if response.status_code == 200:
        anime_data = response.json()
        # extract certain data from the set
        print("Anime Title:", anime_data['data']['title'])

        # display all data from the set
        print("Full Dataset:", anime_data)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# fetch_anime_by_id(1)


def fetch_anime_by_name(anime_name):

    # API url for anime by searched by name
    api_url_anime = f"https://api.jikan.moe/v4/anime?q={anime_name}"
    # do the request with the predefined api-url (here you fetch the data from the external website)
    response = requests.get(api_url_anime)

    if response.status_code == 200:
        # converts the json structure of the data into python language
        anime_data = response.json()

        # an alternative way to loop:
        # for anime in anime_data['data']:
        #     print(anime['title'])

        for i in range(len(anime_data['data'])):
            # because there are multiple anime with the same title you need a loop which displays all of them
            print(anime_data['data'][i]['title'])
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")

fetch_anime_by_name("naruto")


so sehen die daten der externen applikation aus:
- anime_data is die antwort der appliation auf ein anfrage zu einem bestimmten animenamen und enthält alle animes zu dem namen
- anime_data['data] enthält alle ainmes zu dem namen anime_name
- anime_data['data'][x] das ist der x-te anime mit dem namen anime_anime
- ainme_data['data'][x]['title'] das printet den animetitel aus des bestimmten animes

'''


