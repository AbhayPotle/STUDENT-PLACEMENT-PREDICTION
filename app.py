from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import joblib
import pandas as pd
import traceback
import sklearn.compose
import re

if not hasattr(sklearn.compose._column_transformer, '_RemainderColsList'):
    class _RemainderColsList(list):
        pass
    sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing for all routes

model = joblib.load("full_ml_pipeline_model.joblib")

def analyze_company_fit(target_job, internships, certs):
    """
    Simulated NLP engine to predict company placement based on text inputs.
    Matches keywords to determine tier and predicted company.
    """
    text_corpus = f"{target_job} {internships} {certs}".lower()
    
    # Tier 1: FAANG / MAANG equivalents
    tier1_keywords = ['machine learning', 'ai', 'artificial intelligence', 'cloud', 'aws', 'azure', 'google', 'microsoft', 'amazon', 'scalable', 'full stack', 'react', 'node', 'system design']
    # Tier 2: Top IT Services / MNCs
    tier2_keywords = ['developer', 'software engineer', 'backend', 'frontend', 'database', 'sql', 'java', 'python', 'c++', 'tcs', 'infosys', 'wipro', 'cognizant']
    
    t1_score = sum(1 for kw in tier1_keywords if kw in text_corpus)
    t2_score = sum(1 for kw in tier2_keywords if kw in text_corpus)
    
    if t1_score >= 3:
        company = "Amazon / Microsoft (Tier 1 Tech)"
        fit_desc = "Your advanced skill set in modern tech stacks (Cloud, AI, Full-Stack) aligns perfectly with Tier-1 product-based companies. Your project portfolio and internships demonstrate a high capability for scalable system design."
    elif t2_score >= 2 or t1_score >= 1:
        company = "TCS / Infosys (Tier 2 MNC)"
        fit_desc = "Your foundational skills in software development and standard programming languages make you an excellent candidate for top-tier IT service multinationals. Continued focus on practical implementation will secure this."
    elif "startup" in text_corpus or "intern" in text_corpus:
        company = "High-Growth Tech Startups"
        fit_desc = "Your profile shows agility and a willingness to learn, which is highly valued in fast-paced startup environments. Focus on end-to-end product development to excel here."
    else:
        company = "General IT Services / Local Tech Firms"
        fit_desc = "Your current skill trajectory aligns with entry-level development roles. To aim for higher-tier companies, consider acquiring specialized certifications (like AWS) and building full-stack projects."

    return company, fit_desc

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        
        # Inject defaults for removed UI fields to keep ML model happy
        data['AptitudeTestScore'] = 75.0
        data['SoftSkillsRating'] = 3.5
        
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
        proba = model.predict_proba(df)[0]
        confidence = float(max(proba) * 100)

        # Generate Actionable Insights based on the inputs (Numeric)
        insights = []
        if data.get('CGPA', 0) < 7.5:
            insights.append("Focus on improving your CGPA to at least 7.5 to pass initial ATS filters.")
        if data.get('Projects', 0) < 3:
            insights.append("Build more hands-on projects (Full-Stack or ML) and push them to GitHub.")
        if data.get('Internships', 0) < 1:
            insights.append("Secure at least one industry internship to gain practical experience.")
        if data.get('PlacementTraining', 'No') == 'No':
            insights.append("Enroll in dedicated placement training programs offered by your college or online platforms.")
            
        if len(insights) == 0:
            insights.append("Your profile looks strong! Keep refining your advanced skills and preparing for technical interviews.")

        # Text-based Company Match Simulation
        target_job = data.get('target_job_description', '')
        internship_details = data.get('internship_details', '')
        cert_details = data.get('certification_details', '')
        
        predicted_company, job_fit_desc = analyze_company_fit(target_job, internship_details, cert_details)

        return jsonify({
            "result": "Placed" if pred == 1 else "Not Placed",
            "confidence": f"{confidence:.2f}%",
            "insights": insights,
            "predicted_company": predicted_company,
            "job_fit_description": job_fit_desc
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