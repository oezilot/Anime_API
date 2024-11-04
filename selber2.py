'''
Arten von Data:
- sessiondata = page(int), params(dict mit ints und strs), anime_id(variabla mit int), anime_title(variable mit string)
- gefetchte daten(variable)
'''

# jikan API documentation: https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch 

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

#=================== URL-Builder-Function =====================
# TEST: mit gegebener session aus params und page den richtigen api-url bauen (leere params und gefüllte params testen...per degault müssen params leer sein und page 1) (gefüllte session wird simuliert)
# Output = API url mit den richtigen parametern
def url_animes(page, params):
    api_url = f"https://api.jikan.moe/v4/anime?page={page}" # das ist ein query parameter für filtering sachen
    for param in params:
        api_url = api_url + f"&{param}={params[param]}"
    print(f"URL animes:{api_url}")
    return api_url


#=================== Session updaten =====================
# TEST: wird die session korrekt upgedated? session data vor und nach update vergleichen (form-submission simulieren wenn nichts submitted wird wenn etwas realistisches/unrealistisches submitted wird)
# Output: gefüllte session und reset
@app2.route('/update_session', methods=['POST'])
def update_session():
    # Get parameters from form
    animes_title = request.form.get('param_title', '')
    animes_genre = request.form.get('param_genre', '')

    # Initialize or update session params
    params = session.get('params', {})
    
    # Update session with form data
    params['q'] = animes_title
    params['genres'] = animes_genre
    
    # Save updated params in session
    session['params'] = params
    print(f"SESSION CONTENT: {session}")
    return redirect("/reset")


@app2.route('/reset')
def resetPage():
    session['page'] = 1
    return redirect('/')
    
#=================== FETCH-Data Funktion =====================
# TEST: gefüllte session mit prams und page simulieren und api-call simulieren (simulationen variieren für jedes print-statement)
# Output: daten des requests in einem dictionary gespeichert

# fetching all anime data mithilfe des urls un den informationen aus der session
def fetch_animes():
    # Session data retrieval
    page = session.get('page', 1)
    params = session.get('params', {})
    
    try:
        # Make API call using the generated URL
        response_animes = requests.get(url_animes(page, params))
        
        if response_animes.status_code == 200:
            animes_dict = response_animes.json()  # Load JSON data into a dictionary
            
            # Check if 'data' key exists and has content
            if "data" in animes_dict and animes_dict["data"]:
                animes_data = animes_dict.get('data', [])
                print(f"ERFOLG FETCHING animes_data: {animes_data}")
                return {
                    "message": "Data fetched successfully",
                    "data": animes_data,
                    "status": "success",
                    "pagination": animes_dict.get('pagination', {})  # Include pagination if available
                }
            else:
                # No data available for given filters
                print("ERROR FETCHING animes_data: No Anime Data Found")
                return {
                    "message": "No Anime Data Found",
                    "data": [],
                    "status": "error",
                    "pagination": {}
                }
        
        else:
            # Handle unsuccessful response
            print(f"ERROR FETCHING animes_data: {response_animes.status_code}")
            return {
                "message": f"Error fetching data: {response_animes.status_code}",
                "data": [],
                "status": "error",
                "pagination": {}
            }
    
    except requests.RequestException as e:
        # Handle request failure
        print(f"ERROR MAKING THE Animes-API CALL: {e}")
        return {
            "message": f"Request failed: {e}",
            "data": [],
            "status": "error",
            "pagination": {}
        }


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
# TESTS: gefülltes resultat-dictionary simulieren; wenn das dictionary mit den resultaten nicht leer ist dann sollten die bilder displayed werden und sonst nicht (eine meldung wird angezeigt dass keine daten existieren zu genannten parametern)

@app2.route('/', methods=['GET'])
def display_animes_data():
    # data to display (this data is stored in variables to later give it to the html which will display it!)
    results_dictionary = fetch_animes() # this is the dirctionary created!
    animes_data = results_dictionary['data']
    pagination = results_dictionary['pagination']
    message = results_dictionary['message']

    page = session.get('page', 1) # =current page

    # gespeicherte werte für die parameter damit diese in der form angezeigt werden und nicht immer gelöscht werden sobald man submitted!
    params = session.get('params', {})

    selected_param_title = params.get('q', '')
    selected_param_genre = params.get('genres', '')
    
    return render_template(
        'selber2.html', 
        page=page, 
        animes_data=animes_data, 
        pagination=pagination, 
        message=message, 
        selected_param_title=selected_param_title,  # Tippfehler korrigiert
        selected_param_genre=selected_param_genre  # Tippfehler korrigiert
    )


# TESTS: überprüfen ob die page korrekt in der session abgespeichert/abgedated wurde und überprüfen ob die buttons richtig dargestellt sind je nach der aktuellen page
@app2.route('/inc', methods=['POST'])
def inc(): 
    page = session.get('page', 1)
    page = page + 1
    # upgedatete page wieder in der session speichern
    session['page'] = page
    print(f"SESSION DATA:{session}")
    return redirect('/')

@app2.route('/dec', methods=['POST'])
def dec():
    page = session.get('page', 1)
    page = page - 1
    session['page'] = page
    print(f"SESSION DATA:{session}")
    return redirect('/')


# das besagt dass dieses file das main file und nicht nur irgendein modul ist (nur da main file wird gerunnt!)
if __name__ == '__main__':
    app2.run(debug=True)


'''
das habe ich gelernt:
- wenn man globale variablem in einer funktion verändern will muss man dise variablen zuerst als global deklarieren in der besagten funktion!
'''