# diese FIlter brauche ich für die Anime-Suche:
# type, genre, title(sucheingabe), stauts, rating, (oderby/sort alphabetically)

# erweiterungen: beim reload wird session geleert!
# fragen: muss man den parameter für die suchanfrage zuerst stellen, bevor man andere parameter dazunimmt? --> Antwort = NEIN die reihenfolge kommt nicht darauf an ! (gottseidank omg!)

from flask import Flask, render_template, request, url_for, redirect, session
import requests
import os

app = Flask(__name__)
# falls es errors gibt dann mal den key hier ändern weil es sein kann dass es limite gibt für jeden app-key
app.secret_key = '7ed2323092b13f8347245ecf314617c8a925236bd5c8f56f63c9ca8c479b2204'

# this is for the test to see if it works! ()
# params = {
#     "title":"ranma",
#     "type":"tv"
# }
# page = 3

# url-builder function
def urlBuilder(page, params):
    queryUrl = f"https://api.jikan.moe/v4/anime?page={page}"
    for param in params:
        queryUrl = queryUrl + f"&{param}={params[param]}"
    return queryUrl
    print(queryUrl)
# print(urlBuilder(3, params))

def fetchData():
    page = session.get('page', 1)
    params = session.get('params', {})

    # API Request
    response = requests.get(urlBuilder(page, params))

    # this prints out the response headers to look for issues
    print("Response Headers:", response.headers, flush=True)

    if response.status_code == 200:
        data = response.json()
        data = data.get('data', [])
        return data  # Successful request

    elif response.status_code == 429:
        retry_after = response.headers.get('Retry-After', 'unknown')
        print(f"Rate limit exceeded. Retry after {retry_after} seconds.")
        time.sleep(int(retry_after))  # Wait before retrying

    elif response.status_code == 400:
        print("Bad request. Please check your query.")

    elif response.status_code == 404:
        print("Resource not found. Double-check the URL or resource.")

    elif response.status_code == 500:
        print("Internal Server Error. Try again later or report the issue.")

    elif response.status_code == 503:
        print("Service is down for maintenance. Please try again later.")
    else:
        print(f"Unhandled error: {response.status_code}")


# ??? why a seperate route for that ???
@app.route('/inc', methods=['POST'])
def inc():
    page = session.get('page', 1)
    page = page + 1
    session['page'] = page
    # hätte man das vereinfacht auch so darstellen können?
    # session['page'] = session.get('page') + 1
    # yes! und ob man das kann
    return redirect('/')

@app.route('/dec', methods=['POST'])
def dec():
    page = session.get('page', 1)  # Get the current page or default to 1
    if page > 1:
        session['page'] = page - 1
    return redirect('/')

# change parameters, which filters were clicked?
@app.route('/parameters', methods=['POST'])
def parameters():


    # informationen aus dem form holen die man ausgewählt hat
    parameter1 = request.form.get('parameter1')  # "type" steht für den namen des selectors in der form
    parameter2 = request.form.get('parameter2')  
    parameter3 = request.form.get('parameter3')
    
    # Get the existing parameters in the session, or initialize an empty dictionary
    params = session.get('params', {})
    
    # die neuen parameter aus der form der session hinzufügen
    params['type'] = parameter1  # Add/update the 'type' parameter
    params['status'] = parameter2  # Add/update the 'status' parameter
    params['rating'] = parameter3

    # Save the updated params back into the session
    session['params'] = params

    return redirect('/resetPage')

@app.route('/resetPage')
def resetPage():
    session['page'] = 1
    return redirect('/')

# ??? why is the session information not stored in the session ???
@app.route('/')
def display():
    data = fetchData()

    # egentlich müsste das nicht nötig sein! ich mache es nur bis das problem aufgehoebn ist!
    page = session.get('page', 1)
    params = session.get('params', {})

    return render_template('selber.html', data=data, page=page, params=params)


if __name__ == '__main__':
    app.run(debug=True)