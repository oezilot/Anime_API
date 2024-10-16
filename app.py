# how to fetch a single request? (the API is a link to the database)
# example: i want information to the series naruto
# 


# app.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Serve the homepage
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

