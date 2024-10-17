from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# function for fetching the data with the api for all anime for a specific page
def fetch_all(page_number):
    api_page = f"https://api.jikan.moe/v4/anime?page={page_number}"
    response = requests.get(api_page)

    if response.status_code == 200:
        data_json = response.json()  # Parse JSON response
        data = data_json['data']
        return data
# print(fetch_all(1))



# route to display all anime on the page 1
@app.route('/', methods=['GET', 'POST'])
def all_anime():
    page_number = int(request.args.get('page', 1)) # mit dem 'befehl' kriegt man die page auf der man gerade drauf ist heraus, falls nichts vorhanden ist dann wird es default 1 gesetzt

    # navigation_buttons event
    if request.method == 'POST':
        navigation_action = request.form.get('navigation')  # navigation ist der name der navigationbuttons

        if navigation_action == 'previous':
            page_number = page_number - 1
        elif navigation_action == 'next':
            page_number = page_number + 1

        # Redirect to the new page with updated page_number, wenn man ja den previous button clickt dann redirectet es ja einem zu der page auf der man bereits einmal war!
        return redirect(url_for('all_anime', page=page_number))

    data = fetch_all(page_number)
    
    return render_template('loadmore.html', data=data, page_number=page_number)



if __name__ == '__main__':
    app.run(debug=True)
