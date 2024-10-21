'''
Why do i need sessions?
- if i need the same data stored in a variable for multiple requests throughout different routes etc. i can store that information in a session(ex.: login data, ...)
- for global variables i can use g or sessions

mein plan:

ein dictionary definieren mit 2 informationen über den state
- pagenumber
- parameters from the filter
--> based on these infos the url is created!

urlBuilder(page_number, params)
    url = anime_url
    return url


fetchAnimeData():
    fetch data depending on the api_url
    data = ...
    return data


app.route
displayData():
    which data will be displayed?
    renturn render_template(html)


def forward

def backwards
'''

from flask import Flask, render_template, request, url_for, redirect, session, g
import requests
import os

app = Flask(__name__)
app.secret_key = '7ed2323092b13f8347245ecf314617c8a925236bd5c8f56f63c9ca8c479b2204'

# this is for the test to see if it works!
params = {
    "title":"ranma",
    "type":"tv"
}
page = 3

# url-builder function
def urlBuilder(page, params):
    queryUrl = f"https://api.jikan.moe/v4/anime?page={page}"
    for param in params:
        queryUrl = queryUrl + f"&{param}={params[param]}"
    return queryUrl
# print(urlBuilder(3, params))

def fetchData():
    # daten fetchen mit dem url des api
    response = requests.get(urlBuilder(page, params))

    # daten in einer vaiable speichern 
    g.data = response.json()

    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        return None

@app.route('/')
def display():
    data = fetchData()
    return render_template('selber.html', data=data, page=page)





if __name__ == '__main__':
    app.run(debug=True)