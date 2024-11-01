'''
Arten von Data:
- sessiondata = page(int), params(dict mit ints und strs), anime_id(variabla mit int), anime_title(variable mit string)
- gefetchte daten(variable)
'''

# jikan API documentation: https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch 

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

from flask import Flask
import secrets # für die generiereung eines secret_keys

app = Flask(__name__) # mit diser variable wird die app definiert und dass es sich um eine flask app handelt; man könnte alternativ auch einen andere namen verwenden: "app=Flask(__IrgendEinName__)"
app.secret_key = secrets.token_hex(16) # ein zufälliger key wird jedes mal generiert, das wird benötigt für die session

''' 
nur zum testen:

params = {
    "param1": "type", 
    "param2": 3
}
page = 500

'''

#=================== urlBuilder-Functions (3) =====================
def url_animes(page, params):
    api_url = f"https://api.jikan.moe/v4/anime?page={page}" # das ist ein query parameter für filtering sachen
    for param in params:
        api_url = api_url + f"&{param}={params[param]}"
    print(f"URL animes:{api_url}")
    return api_url

def url_anime(anime_id):
    api_url = f"https://api.jikan.moe/v4/anime/{anime_id}" # das ist ein path parameter für spezifische informationen
    print(f"URL anime:{api_url}")
    return api_url


def url_characters(anime_id):
    api_url = f"https://api.jikan.moe/v4/anime/{anime_id}/characters"  # path parameter
    print(f"URL characters:{api_url}")
    return api_url


# das besagt dass dieses file das main file und nicht nur irgendein modul ist (nur da main file wird gerunnt!)
if __name__ == '__main__':
    app.run(debug=True)
