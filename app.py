from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import joblib
import pandas as pd
import traceback
import sklearn.compose
if not hasattr(sklearn.compose._column_transformer, '_RemainderColsList'):
    class _RemainderColsList(list):
        pass
    sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing for all routes

model = joblib.load("full_ml_pipeline_model.joblib")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])

        # Preprocessing matching the notebook and predict_placement script
        df['ExtracurricularActivities'] = df['ExtracurricularActivities'].map({'Yes': 1, 'No': 0})
        df['PlacementTraining'] = df['PlacementTraining'].map({'Yes': 1, 'No': 0})

        # Feature Engineering
        df['AcademicPerformanceIndex'] = (df['CGPA'] + df['HSC_Marks'] + df['SSC_Marks']) / 3
        df['OverallSkillScore'] = (df['AptitudeTestScore'] + df['SoftSkillsRating']) / 2

        # Ensure correct column order expected by the pipeline before its internal ColumnTransformer
        final_columns = [
            'CGPA', 'Internships', 'Projects', 'Workshops/Certifications', 'AptitudeTestScore',
            'SoftSkillsRating', 'ExtracurricularActivities', 'PlacementTraining', 'SSC_Marks', 'HSC_Marks',
            'AcademicPerformanceIndex', 'OverallSkillScore'
        ]
        
        df = df[final_columns]

        pred = model.predict(df)[0]
        # Return probability as well if possible to show confidence level (adds a nice touch)
        proba = model.predict_proba(df)[0]
        confidence = float(max(proba) * 100)

        # Generate Actionable Insights based on the inputs
        insights = []
        if data.get('CGPA', 0) < 7.5:
            insights.append("Focus on improving your CGPA to at least 7.5 to pass initial ATS filters.")
        if data.get('Projects', 0) < 3:
            insights.append("Build more hands-on projects (Full-Stack or ML) and push them to GitHub.")
        if data.get('Internships', 0) < 1:
            insights.append("Secure at least one industry internship to gain practical experience.")
        if data.get('AptitudeTestScore', 0) < 70:
            insights.append("Practice aptitude tests (quantitative, logical reasoning) regularly on platforms like IndiaBix.")
        if data.get('SoftSkillsRating', 0) < 4.0:
            insights.append("Enhance soft skills via mock interviews and communication workshops.")
        if data.get('PlacementTraining', 'No') == 'No':
            insights.append("Enroll in dedicated placement training programs offered by your college or online platforms.")
            
        if len(insights) == 0:
            insights.append("Your profile looks strong! Keep refining your advanced skills and preparing for technical interviews.")

        return jsonify({
            "result": "Placed" if pred == 1 else "Not Placed",
            "confidence": f"{confidence:.2f}%",
            "insights": insights
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 400

@app.route("/download-guide", methods=["GET"])
def download_guide():
    try:
        return send_file("Placement_Success_Blueprint.pdf", as_attachment=True)
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)