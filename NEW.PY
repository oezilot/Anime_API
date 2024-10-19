from flask import Flask, render_template, request, url_for, redirect
import requests

app = Flask(__name__)

# Function to fetch anime data for a specific page and type filter
def fetch_anime_page(page_number, anime_type):
    # Base API URL for fetching anime data
    api_url = f"https://api.jikan.moe/v4/anime?page={page_number}"

    # Append type filter to the URL if one is selected
    if anime_type:
        api_url += f"&type={anime_type}"

    # Fetch the data from the API
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        anime_data = response.json()
        return anime_data['data']  # Return the anime data
    else:
        return None

# Route to display anime list with pagination and filtering (via POST)
@app.route('/', methods=['GET', 'POST'])
def display_anime():
    # Default page number is 1
    page_number = int(request.args.get('page', 1))

    # Default anime type filter
    anime_type = request.args.get('type', None)

    # If the form is submitted (POST), update page number and filter
    if request.method == "POST":
        anime_type = request.form.get('anime_type')  # Get selected anime type
        navigation_action = request.form.get('navigation_buttons')  # Get which button was clicked (Next/Previous)

        # Adjust the page number based on the button clicked
        if navigation_action == 'previous':
            page_number = page_number - 1
        elif navigation_action == 'next':
            page_number = page_number + 1

        # Redirect to the same page with updated page number and type
        return redirect(url_for('display_anime', page=page_number, anime_type=anime_type))  # Fixed the key here

    # Fetch anime data for the current page and filter
    anime_data = fetch_anime_page(page_number, anime_type)

    # Render the template with anime data, current page, and selected filter
    return render_template('NEW.html', anime_data=anime_data, page_number=page_number, anime_type=anime_type)


if __name__ == '__main__':
    app.run(debug=True)
