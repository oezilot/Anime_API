from flask import Flask, render_template, request, url_for, redirect, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_fallback_key')  # Ensure you set SECRET_KEY in your environment variables


def queryUrlBuilder(pageNumber, params_):
    queryUrl = f"https://api.jikan.moe/v4/anime?page={pageNumber}"
    for key in params_:
        queryUrl += f"&{key}={params_[key]}"
    return queryUrl

def fetchData():
    page_number = session.get('page_number', 1)
    params = session.get('params', {})
    # TODO Validate parameters before using them
    print("************************************")
    print("************************************")
    print(queryUrlBuilder(page_number, params))
    print("************************************")
    print("************************************")

    response = requests.get(queryUrlBuilder(page_number, params))
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        return None

@app.route('/inc', methods=['POST'])
def pageInc():
    page_number = session.get('page_number', 1)
    page_number += 1
    session['page_number'] = page_number
    return redirect('/')

@app.route('/dec', methods=['POST'])
def pageDec():
    page_number = session.get('page_number', 1)
    if page_number > 1:
        page_number -= 1
    session['page_number'] = page_number
    return redirect('/')

@app.route('/addParam', methods=['POST'])
def addParam():
    key = "type" ##request.form.get('key')
    value = request.form.get('key')
    params = session.get('params', {})
    params[key] = value
    session['params'] = params
    return redirect('/resetPage')

@app.route('/resetPage')
def resetPage():
    session['page_number'] = 1
    return redirect('/')

@app.route('/')
def display():
    data = fetchData()
    return render_template('NEW.html', data=data, page_number=session['page_number'], params = session['params'])

if __name__ == '__main__':
    app.run(debug=True)
