from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

pipeline = joblib.load("C:\\Users\\munag\\OneDrive\\Desktop\\Final_Website\\honey_pipeline.pkl")

# Default mean values for non-user features
DEFAULTS = {
    "CS": 5.500259,
    "Density": 1.535523,
    "EC": 0.799974,
    "Pollen_analysis": "Avacado",
    "Viscosity": 5752.893888
}

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        
        # Create input dataframe with all required features
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

        # Make prediction
        result = pipeline.predict(input_data)[0]
        
        return jsonify({
            "prediction": int(result),
            "message": "Pure Honey" if result == 1 else "Adulterated Honey"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)