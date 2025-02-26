#docker login -u bhuvanaduraim #run
#dckr_pat_EgGea8wlH4Oel_j9YqAEZ4Kf5Z8    #access token


import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Initialize Flask app
app = Flask(__name__, template_folder="templates")  # Specify the templates folder

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # Serve the frontend

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)

        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)