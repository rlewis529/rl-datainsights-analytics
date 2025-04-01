from flask import Flask, jsonify, send_file
from flask_cors import CORS  
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the Flask app

# Sample data
data = [
    {"id": "1", "description": "Underdog Win", "probability": 0.25},
    {"id": "2", "description": "Narrow Win", "probability": 0.55},
    {"id": "3", "description": "Blowout", "probability": 0.85},
    {"id": "4", "description": "Upset", "probability": 0.40}
]

@app.route('/predictions')
def get_predictions():
    return jsonify(data)

@app.route('/chart')
def get_chart():
    labels = [item["description"] for item in data]
    values = [item["probability"] for item in data]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color='skyblue')
    plt.ylim(0, 1)
    plt.ylabel("Probability")
    plt.title("Prediction Probabilities")

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')
