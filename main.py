from flask import Flask,render_template,request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def extract_all_texts(response):
        texts = []
        for message in response:
            if 'text' in message:
                texts.append(message['text'])
        tex = ' '.join(texts)
        return (tex)


def get_bot_response(user_input):
    
    rasa_endpoint = "http://localhost:5005/webhooks/rest/webhook"  # Replace with your Rasa server URL

    payload = {
        "sender": "user",
        "message": user_input
    }

    try:
        response = requests.post(rasa_endpoint, json=payload)

        if response.status_code == 200:
            return extract_all_texts(response.json())
        else:
            return "Error: Failed to get response from Rasa bot"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

@app.route('/get')
def get_response():
    user_input = request.args.get('msg')
    bot_response = get_bot_response(user_input)
    return bot_response


if __name__ == "__main__":
    app.run()