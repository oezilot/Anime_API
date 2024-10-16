from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    
    anime_results = None  # List to hold anime results
    anime_name = request.form.get('searchbar')  # Get the name the user searched for in the search bar
    view_all_clicked = request.form.get('view_all')  # Check if 'View All' button was clicked

    # If the search bar has a value, fetch anime based on the search query
    if anime_name:
        api_name = f"https://api.jikan.moe/v4/anime?q={anime_name}"
        response_name = requests.get(api_name)

        if response_name.status_code == 200:
            anime_data = response_name.json()  # Parse JSON response
            anime_results = anime_data['data']  # Contains anime results based on search
            return render_template('results.html', anime_results=anime_results)
        else:
            return "Error fetching data from API", 500

    # If the 'View All' button was clicked, fetch all anime data via pagination
    elif view_all_clicked:
        anime_results = []
        page = 1  # Start from the first page
        has_more_data = True  # Flag to keep track of more pages
        
        while has_more_data:
            api_all = f"https://api.jikan.moe/v4/anime?page={page}"  # Fetch data by page
            response_all = requests.get(api_all)

            if response_all.status_code == 200:
                anime_data = response_all.json()  # Parse JSON response
                page_data = anime_data['data']  # Get anime data for this page
                
                if not page_data:
                    has_more_data = False  # Stop if no more data is found
                else:
                    anime_results.extend(page_data)  # Add current page data to results
                    page += 1  # Move to the next page
            else:
                return "Error fetching data from API", 500
        
        # Return all the results from all pages
        return render_template('results.html', anime_results=anime_results)

    # Default rendering if no form action is performed
    return render_template('results.html', anime_results=anime_results)

if __name__ == '__main__':
    app.run(debug=True)
