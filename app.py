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

    wikipedia_response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{selected_type}")
    wikipedia_data = wikipedia_response.json()

    wikipedia_summary = wikipedia_data.get('extract', '')
    wikipedia_link = wikipedia_data.get('content_urls', {}).get('desktop', {}).get('page', '')

    return activity_data, wikipedia_summary, wikipedia_link

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    interest = request.form['interest']
    activity_data, wikipedia_summary, wikipedia_link = get_activity(interest)
    return render_template('index.html', activity=activity_data, interest=interest,
                           participants=activity_data['participants'],
                           wikipedia_summary=wikipedia_summary, wikipedia_link=wikipedia_link)

if __name__ == '__main__':
    app.run(debug=True)
