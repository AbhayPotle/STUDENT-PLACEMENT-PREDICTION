# NexGen Placement AI Dashboard 🚀

A highly professional, 4K-revolutionized 3D Enterprise Web Application that predicts student placement probabilities and provides hyper-personalized career insights.

## Overview
This project evolves a standard student placement prediction script into a stunning, interactive 3D portfolio piece. Built for realism and enterprise appeal, it utilizes a custom NLP (Natural Language Processing) simulation engine alongside a robust Logistic Regression Machine Learning pipeline to analyze a student's entire profile—from academic rigor to highly specific technical skills—and outputs an actionable career fit summary.

### Key Features 🌟
- **Immersive 3D Parallax UI**: The entire dashboard is built on extreme glassmorphism aesthetics and features a full-site 3D parallax tilt effect driven by mouse position.
- **Holographic Data Core**: Integrated with `Three.js`, featuring an interactive rotating icosahedron and a dynamic particle system that reacts to prediction results.
- **Enterprise NLP Engine**: Analyzes textual inputs like 'Target Job', 'Key Skills' (e.g., Python, Kubernetes, AWS), and 'Work Experience' to predict exact company tiers (e.g., FAANG vs Tier-2 MNCs) rather than just a generic numeric score.
- **Dynamic Education Pathways**: Intelligently handles diverse backgrounds. Whether a student comes from a rigorous CBSE board, holds a Diploma, or is pursuing a B.Com instead of an Engineering degree, the AI adapts its advice accordingly.
- **Dynamic PDF Blueprint Generation**: Utilizing `fpdf2`, the platform instantly generates and downloads an uncorrupted, 4-page 'Placement Success Blueprint' detailing actionable steps to secure high-end tech roles.

## Tech Stack 🛠️
* **Frontend**: Vanilla JavaScript (ES Modules), HTML5, CSS3 (Advanced Glassmorphism & 3D CSS Transforms)
* **3D Rendering**: Three.js (r160)
* **Backend**: Python, Flask, Flask-CORS
* **Machine Learning**: Scikit-Learn (`LogisticRegression`, `ColumnTransformer`, `PCA`), Pandas, Joblib
* **PDF Generation**: `fpdf2`

## How to Run Locally 💻

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AbhayPotle/STUDENT-PLACEMENT-PREDICTION.git
   cd STUDENT-PLACEMENT-PREDICTION
   ```

2. **Install Backend Dependencies:**
   Ensure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask Backend:**
   This runs the ML Model and NLP prediction server.
   ```bash
   python app.py
   ```
   *The backend will run on `http://127.0.0.1:5000`*

4. **Serve the Frontend:**
   Open a new terminal window in the project root and start a simple HTTP server:
   ```bash
   python -m http.server 8000
   ```
   *Navigate your browser to `http://localhost:8000/` to view the application.*

## Project Architecture & ML Pipeline 🧠
The underlying ML Pipeline processes numerical data (CGPA, Projects, SSC/HSC marks) through `MinMaxScaler` and Dimensionality Reduction (`PCA`). Features like 'Placement Training' and 'Extracurricular Activities' are binary encoded. 

To bridge the gap between human-readable inputs and the strict numerical requirements of the ML model, the Flask backend injects mathematical defaults where necessary, while extracting the true value via the text-based NLP simulation, ensuring the model never breaks while the user experiences a modern, text-based profiling system.

---
*Built to capture the attention of technical recruiters and showcase end-to-end full-stack AI integration.*