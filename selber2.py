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

session updaten

character-page (route)

resetPage (route, nach jedem submit des forms wird page wieder geresettet)

Form (anpassung der items in der session)

'''

from flask import Flask, render_template, session, redirect, request
import secrets # für die generiereung eines secret_keys
import requests # für das handlen den API-calls

app2 = Flask(__name__) # mit diser variable wird die app definiert und dass es sich um eine flask app handelt; man könnte alternativ auch einen andere namen verwenden: "app=Flask(__IrgendEinName__)"
app2.secret_key = secrets.token_hex(16) # ein zufälliger key wird jedes mal generiert, das wird benötigt für die session


#nur zum testen:
# TEST: testwerte um requests etc zu simulieren, statt bei den tests diese variblen füllen füle ich einfach die session mit gewissen werten für die params und page etc
# TESTS: session simulieren statt einzelnenvariablen simulieren!

'''
params = {
    #"type": "tv", 
    "q": ""
    #"status": "airing"
}
page = 1
'''

anime_id = 20 # irgendein naruto-dings (achtung nicht alle zahlen sind eine anime_id...3 z.b. gibt einen error weil es keine id mit 3 gibt!)
error = None # diese variable überbringt dem html immer den error zum darstellen!


#=================== Sessions (params, page, anime_id, anime_title) updaten =====================
# überall wo vorhin die werte der globalen variablen genommen wurden wird nun der wert aus der session geholt!!!
app2.route('/session', methods=['POST'])
def session():
    # parameters 
    animes_type = request.form.get('param_type')


    # pagenumber/currentpage speichern...pagination-dictionary (default-wert ist eins wenn noch keine pagenumber in der session existiert!)
    page = session.get('page', 1)

    # data speicher wie anime_id, anime_title

    # alles in der session speichern
    params = session.get('params', {}) # get the existing session: das dictionary initialisieren
    
    params['type'] = animes_type # das dictionary mit den daten aufüllen aus dem form
    
    params = session.get('params', {}) # das upgedatete dictionary mit den parametern drin

    print(session)
    return redirect("/reset")

@app2.route('/reset')
def resetPage():
    session['page'] = 1
    return redirect('/')
    


#=================== URL-Builder-Functions (3) =====================
# TEST: werden die urls richtig gebildet?
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

#=================== FETCH-Data Funktionen (3) =====================
# TEST: fetch-funktion für die 3 api-urls tsten mit allen spezialfällen
# erwarteter output: daten als liste
# fetching all anime data
def fetch_animes(page, params):
    # sessiondaten herausholen:
    page = session.get('page', 1)
    params = session.get('params', {})

    try: # den call probieren zu machen
        # antwort auf den api-call mit dem api-url der url_animes-funktion (fetchen)
        response_animes = requests.get(url_animes(page, params))
        if response_animes.status_code == 200:
            animes_dict = response_animes.json() #JSON-daten in eine variable laden (= Dictionary)
            if "data" in animes_dict and animes_dict["data"]: # überprüüft ob der key namens data im dict vorhanden ist und ob dieser key einen value hat
                animes_data = animes_dict.get('data', []) 
                print(f"ERFOLG FETCHING animes_data: {animes_data}")
                return animes_data # der rückgabewert der funktion sind die daten des calls
            else:
                # wenn keine daten existieren zu den gewählten parametern!
                print("ERROR FETCHING animes_data: es existiern keine Animes-Daten")
                return None
        else: # falls der call nicht erfolgreich war (400: bad request)
            print(f"ERROR FETCHING animes_data:{response_animes.status_code}")
            return None
    except requests.RequestException as e: # falls der call selbst fehlschlägt (das mit dem exception ist so was speziellen für api-calls)
        print(f"ERROR MAKING THE Animes-API CALL:{e}")
        return None
    
# fetching a certain anime
def fetch_anime(anime_id):
    try:
        response_anime = requests.get(url_anime(anime_id))
        if response_anime.status_code == 200:
            anime_dict = response_anime.json() #JSON-daten in eine variable laden (= Dictionary)
            if "data" in anime_dict and anime_dict["data"]: # überprüüft ob der key namens data im dict vorhanden ist und ob dieser key einen value hat (hier ist data ein dictionary!)
                anime_data = anime_dict.get('data', {}) 
                print(f"ERFOLG FETCHING anime_data: {anime_data}")
                return anime_data # der rückgabewert der funktion sind die daten des calls
            else:
                # wenn keine daten existieren zu den gewählten parametern!
                print("ERROR FETCHING anime_data: es existiern keine Anime-Daten")
                return None
        else: # falls der call nicht erfolgreich war (wenn man parameter hinschreibt die nicht existieren wie anime_id=None) (400: bad request)
            print(f"ERROR FETCHING anime_data:{response_anime.status_code}")
            return None
    except requests.RequestException as e: # falls der call selbst fehlschlägt (das mit dem exception ist so was speziellen für api-calls)
        print(f"ERROR MAKING THE Anime-API CALL:{e}")
        return None

# fetching anime characters from a cerstain anime
def fetch_characters(anime_id):
    try:
        response_characters = requests.get(url_characters(anime_id))
        if response_characters.status_code == 200:
            characters_dict = response_characters.json() #JSON-daten in eine variable laden (= Dictionary)
            if "data" in characters_dict and characters_dict["data"]: # überprüüft ob der key namens data im dict vorhanden ist und ob dieser key einen value hat (hier ist data eine liste!)
                characters_data = characters_dict.get('data', []) 
                print(f"ERFOLG FETCHING characters_data: {characters_data}")
                return characters_data # der rückgabewert der funktion sind die daten des calls
            else:
                # wenn keine daten existieren zu den gewählten parametern!
                print("ERROR FETCHING character_data: es existiern keine Anime-Daten")
                return None
        else: # falls der call nicht erfolgreich war (400: bad request), zum bsp wenn dieanime_id nicht existiert!
            print(f"ERROR FETCHING characters_data:{response_characters.status_code}")
            return None
    except requests.RequestException as e: # falls der call selbst fehlschlägt (das mit dem exception ist so was speziellen für api-calls)
        print(f"ERROR MAKING THE Characters-API CALL:{e}")
        return None
    
#=================== Fetch-Funktionen testen mit vorgegebenen dictionary, page, anime_id (3) =====================
# fetch_animes(page, params) # (erwarteter output = api-url und die daten aller animes)
# fetch_anime(anime_id) # url and daten zu einem bestimmten anime
'''
anime_data = fetch_anime(anime_id)  # Anime-Daten abrufen
if anime_data is not None:
    print("image_url:", anime_data['images']['webp']['image_url'])  # mal_id ausgeben
else:
    print("Fehler: fetch_anime() hat None zurückgegeben.")
'''
# fetch_characters(anime_id) # url and daten zu allen charaktere eines bestimmten animes


#=================== Pages/Routen (3) =====================
# TESTS: bsp mit daten enthalten und bp mit keinen daten wenn die parameter kein erfolgreiches resultat ausspucken!, alle sachen die man displayed haben will teste wie image, title etc
# daten displayen im html, alles was diese funktion returnt wird im html angezeigt!

@app2.route('/', methods=['GET'])
def display_animes_data():
    page = session.get('page', 1)
    params = session.get('params', {})

    if fetch_animes(page, params) != None: # hier könnte es auch sein dass animes_data none ist deshalb muss man das noch überprüfen
        animes_data = fetch_animes(page, params) 
        return render_template('selber2.html', animes_data=animes_data)
    else:
        # diese zeile hier wird im html angezeigt und nicht im terminal!
        return "ERROR in der Display funktion: fetch_animes gibt None zurück!"
    
@app2.route('/anime')
def display_anime_data():
    global anime_id
    if fetch_anime(anime_id) != None: # hier könnte es auch sein dass animes_data none ist deshalb muss man das noch überprüfen
        anime_data = fetch_anime(anime_id) 
        return render_template('anime2.html', anime_data=anime_data)
    else:
        # diese zeile hier wird im html angezeigt und nicht im terminal!
        return "ERROR in der Display funktion: fetch_anime gibt None zurück!"

@app2.route('/characters')
def display_characters_data():
    global anime_id
    if fetch_anime(anime_id) != None: # hier könnte es auch sein dass animes_data none ist deshalb muss man das noch überprüfen
        characters_data = fetch_characters(anime_id) 
        return render_template('characters2.html', characters_data=characters_data)
    else:
        # diese zeile hier wird im html angezeigt und nicht im terminal!
        return "ERROR in der Display funktion: fetch_characters gibt None zurück!"

# TESTS: wenn aktuelle page kleiner als 1 ist, gleich der max seitenzahl ist oder eine zahl dazwischen ist
@app2.route('/inc')
def inc(): 
    page = session.get('page', 1)
    page = page + 1
    return redirect('/')

@app2.route('/dec')
def dec():
    page = session.get('page', 1)
    if page > 1:
        page = page - 1
    else: 
        return "There are no pages lower than 1!"
    return redirect('/')





# das besagt dass dieses file das main file und nicht nur irgendein modul ist (nur da main file wird gerunnt!)
if __name__ == '__main__':
    app2.run(debug=True)


'''
das habe ich gelernt:
- wenn man globale variablem in einer funktion verändern will muss man dise variablen zuerst als global deklarieren in der besagten funktion!
'''