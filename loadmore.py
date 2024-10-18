from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


# function for fetching the data with the api for all anime for a specific page
def fetch_all(page_number, anime_type=None):

    # this is the default url without using any of the parameters! it displays all anime in pages
    api_page = f"https://api.jikan.moe/v4/anime?page={page_number}"

    # this checks wether a button was clicked
    if anime_type:
        api_page = f"https://api.jikan.moe/v4/anime?page={page_number}&type={anime_type}"

    # here the data gets fetches from the API defined at the top with or without parameters
    response = requests.get(api_page)

    # make data ready to be used in the html (dejasonify and select the data-list)
    if response.status_code == 200:
        data_json = response.json()  # Parse JSON response
        data = data_json['data']
        return data
    else:
        return []
# print(fetch_all(1))



# route to display all anime on the page 1
@app.route('/', methods=['GET', 'POST'])
def all_anime():
    page_number = int(request.args.get('page', 1)) # mit dem 'befehl' kriegt man die page auf der man gerade drauf ist heraus, falls nichts vorhanden ist dann wird es default 1 gesetzt
    anime_type = None # per default the type is none

    # navigation_buttons event
    if request.method == 'POST':
        # get the anime_type from the form
        anime_type = request.form.get('type')

        navigation_action = request.form.get('navigation')  # navigation ist der name der navigationbuttons

        if navigation_action == 'previous':
            page_number = page_number - 1
        elif navigation_action == 'next':
            page_number = page_number + 1

        # Redirect to the new page with updated page_number, wenn man ja den previous button clickt dann redirectet es ja einem zu der page auf der man bereits einmal war!
        return redirect(url_for('all_anime', page=page_number, type=anime_type))

    # If it's a GET request, get the type filter from the URL
    anime_type = request.args.get('type')

    # which data will be displayed, with which paramteers included and which page?
    data = fetch_all(page_number, anime_type)
    
    return render_template('loadmore.html', data=data, page_number=page_number)



if __name__ == '__main__':
    app.run(debug=True)
