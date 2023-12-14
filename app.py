from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

def get_activity(interest):
    types_mapping = {
        "Learn": ["education", "diy", "cooking", "music"],
        "Fun": ["recreational", "social", "music"],
        "Creative": ["diy", "cooking", "music"],
        "Chill": ["relaxation", "music"]
    }
    selected_type = random.choice(types_mapping.get(interest, []))

    response = requests.get(f"https://www.boredapi.com/api/activity?type={selected_type}")
    activity_data = response.json()

    return activity_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    interest = request.form['interest']
    activity_data = get_activity(interest)
    return render_template('index.html', activity=activity_data['activity'], interest=interest,
                           participants=activity_data['participants'])

if __name__ == '__main__':
    app.run(debug=True)