'''
Types of Data:
- session data = page (int), params (dict with ints and strings), anime_id (int variable), anime_title (string variable)
- fetched data (variable)
'''

# Jikan API documentation: https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch

from flask import Flask, render_template, session, redirect, request
import secrets  # for generating a secret_key
import requests  # for handling API calls

app2 = Flask(__name__)  # defining this app as a Flask application
app2.secret_key = secrets.token_hex(16)  # generating a random key needed for session handling

# TESTING ONLY:
# TEST: Set up sample values in the session to simulate various API requests. Instead of filling these variables each time, use the session with defined params and page values
# TESTS: Simulate session rather than individual variables

'''
params = {
    #"type": "tv", 
    "q": ""
    #"status": "airing"
}
page = 1
'''

# =================== URL-Builder Function =====================
# TEST: Create the correct API URL based on session values from params and page (test both empty and filled params; default should be empty params and page 1)
# Output: API URL with the correct parameters
def url_animes(page, params):
    api_url = f"https://api.jikan.moe/v4/anime?page={page}"  # Adding query parameters for filtering options
    for param in params:
        api_url = api_url + f"&{param}={params[param]}"
    print(f"URL animes: {api_url}")
    return api_url


# =================== Updating Session Data =====================
# TEST: Check if session updates correctly; compare session data before and after updating (simulate form submission with valid and invalid inputs)
# Output: Updated session and reset confirmation
@app2.route('/update_session', methods=['POST'])
def update_session():
    # Get parameters from form submission
    animes_title = request.form.get('param_title', '')
    animes_genre = request.form.get('param_genre', '')

    # Initialize or update session params
    params = session.get('params', {})
    
    # Update session with form data
    params['q'] = animes_title
    params['genres'] = animes_genre
    
    # Save updated params in session
    session['params'] = params
    print(f"SESSION CONTENT: {session}")
    return redirect("/reset")


@app2.route('/reset')
def resetPage():
    session['page'] = 1
    return redirect('/')
    
# =================== Data Fetch Function =====================
# TEST: Simulate a filled session with params and page and execute an API call (test print statements with various simulation scenarios)
# Output: Data from the request stored in a dictionary

# Fetch all anime data using the URL and session data
def fetch_animes():
    # Retrieve session data
    page = session.get('page', 1)
    params = session.get('params', {})
    
    try:
        # Make API call using the generated URL
        response_animes = requests.get(url_animes(page, params))
        
        if response_animes.status_code == 200:
            animes_dict = response_animes.json()  # Load JSON data into a dictionary
            
            # Check if 'data' key exists and has content
            if "data" in animes_dict and animes_dict["data"]:
                animes_data = animes_dict.get('data', [])
                print(f"SUCCESS FETCHING animes_data: {animes_data}")
                return {
                    "message": "Data fetched successfully",
                    "data": animes_data,
                    "status": "success",
                    "pagination": animes_dict.get('pagination', {})  # Include pagination if available
                }
            else:
                # No data available for given filters
                print("ERROR FETCHING animes_data: No Anime Data Found")
                return {
                    "message": "No Anime Data Found",
                    "data": [],
                    "status": "error",
                    "pagination": {}
                }
        
        else:
            # Handle unsuccessful response
            print(f"ERROR FETCHING animes_data: {response_animes.status_code}")
            return {
                "message": f"Error fetching data: {response_animes.status_code}",
                "data": [],
                "status": "error",
                "pagination": {}
            }
    
    except requests.RequestException as e:
        # Handle request failure
        print(f"ERROR MAKING THE Animes-API CALL: {e}")
        return {
            "message": f"Request failed: {e}",
            "data": [],
            "status": "error",
            "pagination": {}
        }


# =================== Page Routes (3) =====================
# TEST: Simulate a filled results dictionary; if the dictionary with results is not empty, images should be displayed, otherwise a message should appear indicating that no data exists for the given parameters

@app2.route('/', methods=['GET'])
def display_animes_data():
    # Data for display (stored in variables for passing to HTML for rendering)
    results_dictionary = fetch_animes()  # The dictionary created from fetch_animes function
    animes_data = results_dictionary['data']
    pagination = results_dictionary['pagination']
    message = results_dictionary['message']

    page = session.get('page', 1)  # Current page

    # Retrieve stored filter parameters to maintain them in the form after submission
    params = session.get('params', {})

    selected_param_title = params.get('q', '')
    selected_param_genre = params.get('genres', '')
    
    return render_template(
        'selber2.html', 
        page=page, 
        animes_data=animes_data, 
        pagination=pagination, 
        message=message, 
        selected_param_title=selected_param_title,
        selected_param_genre=selected_param_genre
    )


# TEST: Check if the page number is correctly saved and updated in the session; ensure the buttons display correctly based on the current page
@app2.route('/inc', methods=['POST'])
def inc(): 
    page = session.get('page', 1)
    page = page + 1
    # Save updated page number back to session
    session['page'] = page
    print(f"SESSION DATA: {session}")
    return redirect('/')

@app2.route('/dec', methods=['POST'])
def dec():
    page = session.get('page', 1)
    page = page - 1
    session['page'] = page
    print(f"SESSION DATA: {session}")
    return redirect('/')


# Specify that this file is the main file and not just a module (only the main file runs!)
if __name__ == '__main__':
    app2.run(debug=True)


'''
What I learned:
- To modify global variables within a function, you must declare them as global within that function!
'''
