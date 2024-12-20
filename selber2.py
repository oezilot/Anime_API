'''
Types of Data:
- session data = page (int), params (dict with ints and strings), anime_id (int variable), anime_title (string variable)
- fetched data (variable)
'''

# Jikan API documentation: https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch

from flask import Flask, render_template, session, redirect, request
import secrets  # for generating a secret_key
import requests  # for handling API calls
from urllib.parse import urlencode # for an endcoded api-url (query-parameters)


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
''' ursprüngliche funktion
def url_animes(page, params):
    api_url = f"https://api.jikan.moe/v4/anime?page={page}"  # Adding query parameters for filtering options
    for param in params:
        api_url = api_url + f"&{param}={params[param]}"
    print(f"URL animes: {api_url}")
    return api_url
'''
# neue verbesserte funktion mit query-endcoding 
def url_animes(page, params):
    base_url = f"https://api.jikan.moe/v4/anime?page={page}"  # Adding page parameter directly to the base URL
    encoded_params = urlencode(params)  # Encode all parameters in params dictionary
    
    # Construct the final URL by appending encoded query parameters
    api_url = f"{base_url}&{encoded_params}"
    
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
    # Retrieve session data or create this data if not deklared already
    page = session.get('page', 1)
    params = session.get('params', {})
    
    try:
        # Make API call using the generated URL
        response_animes = requests.get(url_animes(page, params))
        
        if response_animes.status_code == 200:
            animes_dict = response_animes.json()  # Load JSON data into a dictionary
            #print(animes_dict)
            
            # Check if 'data' key exists and has content
            if "data" in animes_dict and animes_dict["data"]:
                animes_data = animes_dict.get('data', [])
                # print(f"SUCCESS FETCHING animes_data: {animes_data}")
                return {
                    "message": "Data fetched successfully",
                    "data": animes_data,
                    "status": "success",
                    "pagination": animes_dict.get('pagination', {})  # Include pagination if available
                }
            else:
                # No data available for given filters (wenn zu gesuchten parameter nichts vorhanden ist dann ist die datenliste einfach leer!!!)
                print("ERROR FETCHING animes_data: No Anime Data Found")
                return {
                    "message": "No Anime Data Found",
                    "data": [],
                    "status": "error",
                    "pagination": {"has_next_page": False, "last_visible_page": 1}  # Default pagination
                }
        
        else:
            # Handle unsuccessful response, client/server problem (als rückgabe wir dann einfach eine leere liste zurückgegeben)...z.b. wenn zu viele anfragen gemacht wurden
            print(f"ERROR FETCHING animes_data: {response_animes.status_code}")
            return {
                "message": f"Error fetching data: {response_animes.status_code}",
                "data": [],
                "status": "error",
                "pagination": {"has_next_page": False, "last_visible_page": 1}  # Default pagination
            }
    
    except requests.RequestException as e:
        # Handle request failure, der request konnte gar nicht gemacht werden!
        print(f"ERROR MAKING THE Animes-API CALL: {e}")
        return {
            "message": f"Request failed: {e}",
            "data": [],
            "status": "error",
            "pagination": {"has_next_page": False, "last_visible_page": 1}  # Default pagination
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
    # Get the current page from the session
    page = session.get('page', 1)

    # Fetch pagination information to get the last visible page
    result = fetch_animes()
    last_visible_page = result['pagination'].get('last_visible_page', 1)

    # Increment only if the current page is less than the last_visible_page
    if page < last_visible_page:
        page += 1

    # Update the session with the new page value
    session['page'] = page
    print(f"SESSION DATA after increment: {session}")
    return redirect('/')


@app2.route('/dec', methods=['POST'])
def dec():
    # Get the current page from the session
    page = session.get('page', 1)

    # Decrement only if the page is greater than 1
    if page > 1:
        page -= 1

    # Update the session with the new page value
    session['page'] = page
    print(f"SESSION DATA after decrement: {session}")
    return redirect('/')



# Specify that this file is the main file and not just a module (only the main file runs!)
if __name__ == '__main__':
    app2.run(debug=True)


'''
What I learned:
- To modify global variables within a function, you must declare them as global within that function!
'''
