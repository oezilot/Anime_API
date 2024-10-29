'''
todo's

- keep the values displayed on the filterbuttons when selected a value
- css styling with tailwind
- display image, title, year, studio of each anime  in data
- do tests?
- den ganzen code nochmals neu schreiben?!
- wie genau funkitioniert das mit der message und allgemein das mit den messages?
- ich glaube ich weiss nun was der fehler war: man sollte die daten nie direkt fetchen sondern immer eine alternative bereitsstellen denn sonst gibt es errors
- liste mit erweiterungen schreiben die man noch hinzufügen könnte zur application
- bug-sicher machen und klären ob das mit dem .get ein problem echt ist!
- neue application schreiben als mischung aus dieser und der von gpt
- sort?

'''

from flask import Flask, render_template, request, url_for, redirect, session
import requests

app = Flask(__name__)
app.secret_key = '7ed2323092b13f8347245ecf314617c8a925236bd5c8f56f63c9ca8c479b2204'


################## Search Page --> alles animes aufgelistet zu bestimmten parametern ##########################

# mit dieser API-URL werden dann die Daten gefetched
def urlBuilder(page, params):
    queryUrl = f"https://api.jikan.moe/v4/anime?page={page}"
    for param in params:
        queryUrl += f"&{param}={params[param]}"
    print(f"Main API URL: {queryUrl}")  # Debug print to check the URL
    return queryUrl

# Daten fetchen mit dem URL aus dem urlBuilder
def fetchData():
    # items in die session hineintun! (session wird hier quasi erstellt)
    page = session.get('page', 1)
    params = session.get('params', {})
    
    response = requests.get(urlBuilder(page, params))

    # Print response headers and status code for debugging
    print("Response Headers:", response.headers, flush=True)
    print(f"Status Code: {response.status_code}", flush=True)

    if response.status_code == 200:
        try:
            data = response.json()
            # Check if the data list is empty
            if not data['data']:
                return {"message": "No posts with your filters exist", "data": [], "pagination": {}}
            
            pagination = data.get('pagination', {})  # Corrected to fetch pagination data

            return {"message": "", "data": data.get('data', []), "pagination": pagination}  # Return message, data, and pagination

        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return {"message": "Error fetching data", "data": [], "pagination": {}}
    else:
        print(f"API error: {response.status_code}")
        return {"message": "Error fetching data", "data": [], "pagination": {}}

@app.route('/inc', methods=['POST'])
def inc():
    page = session.get('page', 1)
    session['page'] = page + 1
    return redirect('/')


@app.route('/dec', methods=['POST'])
def dec():
    page = session.get('page', 1)
    if page > 1:
        session['page'] = page - 1
    return redirect('/')


@app.route('/parameters', methods=['POST'])
def parameters():
    # Get the parameters from the form
    parameter1 = request.form.get('parameter1')
    parameter2 = request.form.get('parameter2')
    parameter3 = request.form.get('parameter3')
    parameter_title = request.form.get('parameter_title')
    parameter_genre = request.form.get('parameter_genre')

    # Debugging: Print the values received from the form
    print("Title:", parameter_title)
    print("Genre:", parameter_genre)

    # Get the existing parameters in the session
    params = session.get('params', {})

    # Add/update the parameters in the session
    params['type'] = parameter1
    params['status'] = parameter2
    params['rating'] = parameter3
    params['q'] = parameter_title
    params['genres'] = parameter_genre

    # Save the updated params back into the session
    session['params'] = params
    print("Session params:", session['params'])  # Debug print for session data

    return redirect('/resetPage')


@app.route('/resetPage')
def resetPage():
    session['page'] = 1
    return redirect('/')


@app.route('/')
def display():
    result = fetchData()
    data = result["data"]
    pagination = result["pagination"]
    message = result["message"]

    #session.clear() # falls ich die session leeren möchte (mit dm musste ich genre= gerauslöschen!!!)

    print("Session Data:", session, flush=True)


    page = session.get('page', 1)
    params = session.get('params', {})
    parameter1 = params.get('type', '')
    parameter2 = params.get('status', '')
    parameter3 = params.get('rating', '')
    parameter_title = params.get('q', '')
    parameter_genre = params.get('genres', '')

    return render_template('selber.html', data=data, page=page, params=params, parameter1=parameter1, parameter2=parameter2, parameter3=parameter3, parameter_title=parameter_title, parameter_genre=parameter_genre, message=message, pagination=pagination)



############################ Character Page --> alle characters aus dem anime x #########################

# neue urlbuilder-funtionc für die charaktere
# url: /anime/animeid
def character_url(anime_id):
    api_url = f"https://api.jikan.moe/v4/anime/{anime_id}/characters"
    response2 = requests.get(api_url)
    if response2.status_code == 200:
        print(f"Character API URL: {api_url}")  # Debug print to check the URL
        # print("Response Data:", response2.json(), flush=True)  # Print the entire response data for debugging

        return response2.json()
    else:
        return {"data": []}  # Return an empty structure if the request fails


@app.route('/characters', methods=['GET', 'POST'])
def characters():
    if request.method == 'POST':
        # Get the anime ID and title from the form
        anime_id = request.form.get('anime_id')
        anime_title = request.form.get('anime_title')


        # Debugging: print values to ensure they are received
        print(f"Received anime_id: {anime_id}")
        print(f"Received anime_title: {anime_title}")



        # Store the anime ID and title in the session
        session['anime_id'] = anime_id
        session['anime_title'] = anime_title

    # Retrieve the anime ID and title from the session
    anime_id = session.get('anime_id', 'None')
    anime_title = session.get('anime_title', 'Unknown')

    # API call to get character data
    characters = character_url(anime_id)
    character_data = characters['data']

    print("Session Data:", session, flush=True)

    return render_template('characters.html', anime_id=anime_id, anime_title=anime_title, character_data=character_data)



########################## Anime Page --> informationen zum anime mit id x ##########################
def anime_url(anime_id):
    api_url = f"https://api.jikan.moe/v4/anime/{anime_id}"
    response3 = requests.get(api_url)
    if response3.status_code == 200:
        print(f"Anime API URL: {api_url}")  # Debug print to check the URL
        # print("Response Data:", response2.json(), flush=True)  # Print the entire response data for debugging
        return response3.json()
    else:
        return {"data": []}  # Return an empty structure if the request fails


@app.route('/anime', methods=['GET', 'POST'])
def anime():
    if request.method == 'POST':
        anime_id = request.form.get('anime_id')
        session['anime_id'] = anime_id

    anime_id = session.get('anime_id', 'None')


    anime = anime_url(anime_id)
    anime_data = anime['data']

    print("Session Data:", session, flush=True)

    return render_template('anime.html', anime_data=anime_data)


if __name__ == '__main__':
    app.run(debug=True)
