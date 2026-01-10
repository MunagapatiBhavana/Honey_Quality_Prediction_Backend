from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import joblib

app = Flask(__name__)

# -----------------------------
# Load Model
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "honey_pipeline.pkl")

pipeline = joblib.load(MODEL_PATH)

# -----------------------------
# Default values
# -----------------------------
DEFAULTS = {
    "CS": 5.500259,
    "Density": 1.535523,
    "EC": 0.799974,
    "Pollen_analysis": "Avacado",
    "Viscosity": 5752.893888
}

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        input_data = pd.DataFrame([{
            "CS": DEFAULTS["CS"],
            "Density": DEFAULTS["Density"],
            "WC": float(data["WC"]),
            "pH": float(data["pH"]),
            "EC": DEFAULTS["EC"],
            "F": float(data["Fructose"]),
            "G": float(data["Glucose"]),
            "Pollen_analysis": DEFAULTS["Pollen_analysis"],
            "Viscosity": DEFAULTS["Viscosity"]
        }])

        result = pipeline.predict(input_data)[0]

        return jsonify({
            "prediction": int(result),
            "message": "Pure Honey" if result == 1 else "Adulterated Honey"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -----------------------------
# Run App (Render compatible)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
