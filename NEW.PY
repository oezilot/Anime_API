# filtern(per page oder gesamt?)
# api im url für die route anzeigen
# bei neuer seite gehen die parameter wieder weg

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# daten einer page x fetchen je nach ihren parameter (=filter)
def fetch_anime_page(page_number, anime_type):

    api_url = f"https://api.jikan.moe/v4/anime?page={page_number}" # url für den api 

    # für jeden angewendeten filter wird eine neue url (Abfrage) generiert

    # falls der button anime_type gedrückt wird (type parameter)
    if anime_type: 
        api_url += f"&type={anime_type}"

    # die daten der abfrage fetchen je für den url der abfrage 
    response = requests.get(api_url)

    # anime daten "vorbereiten"
    if response.status_code == 200:
        anime_data = response.json()
        anime_data = anime_data['data']

        return anime_data  # Returns anime data for the current page
    else:
        return None

# pages darstellen im html
@app.route('/', methods=['GET', 'POST'])
def display_anime():

    # page herausfinden auf der man sich gerade befindet, per default ist es 1
    page_number = int(request.args.get('page', 1)) # 'page' bezieht sich auf den url page={...}
    # per default ist der anime_type nicht spezifiziert
    anime_type = request.args.get('type', None)

    # falls der anime-type-paramter geändert worden ist wird dieser angenommen
    if request.method == "POST":
        anime_type = request.form.get('anime_type')
    
    # Fetch the anime data for the given page number and anime_type
    anime_data = fetch_anime_page(page_number, anime_type)

    # Render the results template, passing the anime data and current page
    return render_template('NEW.html', anime_data=anime_data, current_page=page_number, anime_type=anime_type)


if __name__ == '__main__':
    app.run(debug=True)