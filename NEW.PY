'''
Arten von Data:
- sessiondata = page(int), params(dict mit ints und strs), anime_id(variabla mit int), anime_title(variable mit string)
- gefetchte daten(variable)
'''

from flask import Flask
import secrets # für die generiereung eines secret_keys

app = Flask(__name__) # mit diser variable wird die app definiert und dass es sich um eine flask app handelt; man könnte alternativ auch einen andere namen verwenden: "app=Flask(__IrgendEinName__)"
app.secret_key = secrets.token_hex(16) # ein zufälliger key wird jedes mal generiert, das wird benötigt für die session

'''
My Plan:

urlBuilder (3 verschiedene arten von urls)

fetchData (3 verschiedene datasets: merere animes in pages, anime: infos zu nur 1 anime mit id, characters: characters zu 1 anime mit id)

pagination (route --> inc, dec)

home-page (route)

anime-page (route)

character-page (route)

resetPage (route, nach jedem submit des forms wird page wieder geresettet)

Form (anpassung der items in der session)

'''

#=================== urlBuilder-Functions =====================
def url_animes(page, params):
    api_url = f"https://api.jikan.moe/v4/anime/{page}"

def url_anime(anime_id):
          api_url = f"https://api.jikan.moe/v4/anime/{anime_id}"

def url_characters(anime_id):
        api_url = f"https://api.jikan.moe/v4/anime/{page}"
