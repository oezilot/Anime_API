'''
Arten von Data:
- sessiondata = page(int), params(dict mit ints und strs), anime_id(variabla mit int), anime_title(variable mit string)
- gefetchte daten(variable)
'''

# jikan API documentation: https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch 

'''
My Plan:

urlBuilder (3 verschiedene arten von urls)

fetchData (3 verschiedene datasets: merere animes in pages, anime: infos zu nur 1 anime mit id, characters: characters zu 1 anime mit id)

pagination (route --> inc, dec)

home-page (route)

anime-page (route)

character-page (route)

resetPage (route, nach jedem submit des forms wird page wieder geresettet)

Form (anpassung der items in der session)

'''

from flask import Flask, render_template
import secrets # für die generiereung eines secret_keys
import requests # für das handlen den API-calls

app2 = Flask(__name__) # mit diser variable wird die app definiert und dass es sich um eine flask app handelt; man könnte alternativ auch einen andere namen verwenden: "app=Flask(__IrgendEinName__)"
app2.secret_key = secrets.token_hex(16) # ein zufälliger key wird jedes mal generiert, das wird benötigt für die session


#nur zum testen:

params = {
    "type": "tv", 
    "q": "kakegurui",
    #"status": "airing"
}
page = 1
error = None # diese variable überbringt dem html immer den error zum darstellen!


#=================== urlBuilder-Functions (3) =====================
# erwartender output = API url mit den richtigen parametern
def url_animes(page, params):
    api_url = f"https://api.jikan.moe/v4/anime?page={page}" # das ist ein query parameter für filtering sachen
    for param in params:
        api_url = api_url + f"&{param}={params[param]}"
    print(f"URL animes:{api_url}")
    return api_url

def url_anime(anime_id):
    api_url = f"https://api.jikan.moe/v4/anime/{anime_id}" # das ist ein path parameter für spezifische informationen
    print(f"URL anime:{api_url}")
    return api_url


def url_characters(anime_id):
    api_url = f"https://api.jikan.moe/v4/anime/{anime_id}/characters"  # path parameter
    print(f"URL characters:{api_url}")
    return api_url


# erwarteter output: daten als liste
def fetch_data(page, params):
    try: # den call probieren zu machen
        # antwort auf den api-call mit dem api-url der url_animes-funktion (fetchen)
        response_animes = requests.get(url_animes(page, params))
        if response_animes.status_code == 200:
            animes_dict = response_animes.json() #JSON-dten in eine variable laden (= Dictionary)
            if "data" in animes_dict and animes_dict["data"]: # überprüüft ob der key namens data im dict vorhanden ist und ob dieser key einen value hat
                animes_data = animes_dict.get('data', []) 
                print(f"ERFOLG FETCHING animes_data: {animes_data}")
                return animes_data # der rückgabewert der funktion sind die daten des calls
            else:
                # wenn keine daten existieren zu den gewählten parametern!
                print("ERROR FETCHING animes_data: es existiern keine Anime-Daten")
                return None
        else: # falls der call nicht erfolgreich war (400: bad request)
            print(f"ERROR FETCHING animes_data:{response_animes.status_code}")
            return None
    except requests.RequestException as e: # falls der call selbst fehlschlägt (das mit dem exception ist so was speziellen für api-calls)
        print(f"ERROR MAING THE API CALL:{e}")
        return None
    
# fetch-funktion aufrufen: (erwarteter output = api-url und die daten)
# fetch_data(page, params)


# TESTS: bsp mit daten enthalten und bp mit keinen daten wenn die parameter kein erfolgreiches resultat ausspucken!
# daten displayen im html, alles was diese funktion returnt wird im html angezeigt!
@app2.route('/', methods=['GET'])
def display_animes_data():
    global page, params
    if fetch_data(page, params) != None: # hier könnte es auch sein dass animes_data none ist deshalb muss man das noch überprüfen
        animes_data = fetch_data(page, params) 
        return render_template('selber2.html', animes_data=animes_data)
    else:
        # diese zeile hier wird im html angezeigt und nicht im terminal!
        return "ERROR in der Display funktion: fetch_data gibt None zurück!"





# das besagt dass dieses file das main file und nicht nur irgendein modul ist (nur da main file wird gerunnt!)
if __name__ == '__main__':
    app2.run(debug=True)


'''
das habe ich gelernt:
- wenn man globale variablem in einer funktion verändern will muss man dise variablen zuerst als global deklarieren in der besagten funktion!
'''