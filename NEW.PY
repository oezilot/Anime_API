from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        if request.form['filters'] == 'filter1':
            # Get the value from the input field
            anime_name = request.form.get('anime_search', '')
            return f"You searched for: {anime_name}"
        elif request.form['filters'] == 'filter2':
            return "Button 2 was clicked!"
        elif request.form['filters'] == 'filter3':
            return "Button 3 was clicked!"
        else:
            return "Unknown button"
    
    # If it's a GET request, render the form
    return render_template('NEW.html')

if __name__ == "__main__":
    app.run(debug=True)
