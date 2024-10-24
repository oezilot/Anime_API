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

# mit dieser API-URL werden dann die Daten gefetched
def urlBuilder(page, params):
    queryUrl = f"https://api.jikan.moe/v4/anime?page={page}"
    for param in params:
        queryUrl += f"&{param}={params[param]}"
    print(f"Final API URL: {queryUrl}")  # Debug print to check the URL
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

    return render_template('selber.html', data=data, page=page, params=params, message=message, pagination=pagination)


@app.route('/characters', methods=['GET', 'POST'])
def characters():
    if request.method == 'POST':
        # Get the anime ID from the form
        anime_id = request.form.get('anime_id')

        # Store the anime ID in the session
        session['anime_id'] = anime_id

    # Retrieve the anime ID from the session
    anime_id = session.get('anime_id', 'None')

    return render_template('characters.html', anime_id=anime_id)


@app.route('/anime', methods=['GET', 'POST'])
def anime():
    return render_template('anime.html')


if __name__ == '__main__':
    app.run(debug=True)
