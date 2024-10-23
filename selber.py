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
    page = session.get('page', 1)
    params = session.get('params', {})

    # die antwort des API Request
    response = requests.get(urlBuilder(page, params))

    # Print response headers and status code for debugging
    print("Response Headers:", response.headers, flush=True)
    print(f"Status Code: {response.status_code}", flush=True)

    if response.status_code == 200:
        try:
            data = response.json()
            # print(data)  # Print the full response for debugging

            # Check if the data list is empty
            if not data['data']:
                return {"message": "No posts with your filters exist", "data": []}
            
            return {"message": "", "data": data.get('data', [])}  # Return message and data

        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return {"message": "Error fetching data", "data": []}
    else:
        print(f"API error: {response.status_code}")
        return {"message": "Error fetching data", "data": []}


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
    message = result["message"]

    #session.clear() # falls ich die session leeren möchte (mit dm musste ich genre= gerauslöschen!!!)

    print("Session Data:", session, flush=True)


    page = session.get('page', 1)
    params = session.get('params', {})

    return render_template('selber.html', data=data, page=page, params=params, message=message)


if __name__ == '__main__':
    app.run(debug=True)
