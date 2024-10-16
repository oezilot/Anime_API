# api-url für alle animes: https://api.jikan.moe/v4/anime
''' alle verschiedenen urls die ich brauche:
- alle animes: https://api.jikan.moe/v4/anime?sort=asc

- genre: https://api.jikan.moe/v4/anime?genres={id}
- type(dropdown +): https://api.jikan.moe/v4/anime?type={type}
- name(dropdown +): https://api.jikan.moe/v4/anime?q={name}
- rating:
- status:
'''

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# def generate_url():

# display the first page of all all animes url

# allgemeine funktion um eine page mit pagenumber page zu fetchen
def fetch_anime_page(page_number):
    api_url = f"https://api.jikan.moe/v4/anime?page={page_number}"
    response = requests.get(api_url)

    if response.status_code == 200:
        anime_data = response.json()
        anime_data = anime_data['data']

        # Filter out entries that don't have a valid title
        anime_data = [x for x in anime_data if x.get('title')]

        # Normalize titles by stripping whitespace and converting to lowercase for consistent sorting
        anime_data = sorted(anime_data, key=lambda x: x['title'].strip().lower())


        return anime_data  # Returns anime data for the current page
    else:
        return None

# die page mit pagenumber page displayen
@app.route('/', methods=['GET', 'POST'])
def display_anime():
    # Get the page number from the form, default to 1 if not provided
    page_number = int(request.args.get('page', 1))
    
    # Fetch the anime data for the given page number
    anime_data = fetch_anime_page(page_number)

    # Render the results template, passing the anime data and current page
    return render_template('NEW.html', anime_data=anime_data, current_page=page_number)




if __name__ == '__main__':
    app.run(debug=True)