from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    anime_name = None
    anime_results = None

    if request.method == 'POST':
        anime_name = request.form['anime_name']  # Get the anime name from the form
        
        # API URL for anime search by name
        api_url_anime = f"https://api.jikan.moe/v4/anime?q={anime_name}"
        
        # Make the GET request to fetch the anime data
        response = requests.get(api_url_anime)

        if response.status_code == 200:
            anime_data = response.json()
            anime_results = anime_data['data'] # enthält alle animes mit dem namen anime_name der in das form eingegeben wurde (z.b. alle verschiedenen Naruto filme/Serien)
            print(anime_results[0]['title']) # der titel für das erste resultat das herausgespuckt wird (bsp.: naruto Shippuden)
        else:
            anime_results = [] # Set to an empty list if the request fails

    return render_template("index_test.html", anime_name=anime_name, anime_results=anime_results)

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


