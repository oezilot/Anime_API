
from flask import Flask, render_template, request, url_for, redirect, session
import requests
import os

app = Flask(__name__)
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
# print(urlBuilder(3, params))

def fetchData():
    # params und page in einer session speichern!
    page = session.get('page', 1)
    params = session.get('params', {})

    # daten fetchen mit dem url des api, jetzt setz man hier die werte für die page und params ein!
    response = requests.get(urlBuilder(page, params))

    # daten in einer vaiable speichern 
    if response.status_code == 200:
        data = response.json()
        print(data)  # Print the full response to debug
        return data.get('data', [])  # Use .get() to safely access 'data'
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

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

    # für jeden verschiedenen parameter die ins form gesendeten daten nehmen (type, genre, etc.)
    parameter1 = request.form.get('parameter1')  # "type" steht für den namen des selectors in der form
    parameter2 = request.form.get('parameter2')  
    
    # Get the existing parameters in the session, or initialize an empty dictionary
    params = session.get('params', {})
    
    # Update the session params with the new values
    params['type'] = parameter1  # Add/update the 'type' parameter
    params['genre'] = parameter2  # Add/update the 'status' parameter

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