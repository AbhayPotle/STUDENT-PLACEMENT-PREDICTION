from fpdf import FPDF

def create_placement_guide(output_path="Placement_Success_Blueprint.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 20, "The Ultimate Blueprint for Placement Success", 0, 1, 'C')
    pdf.ln(10)

    # Section 1: How the AI Prediction Model Works
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "1. Understanding the AI Prediction Model", 0, 1)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, (
        "Our machine learning pipeline uses a Logistic Regression model trained on high-dimensional data, "
        "optimized using Principal Component Analysis (PCA). The key factors it evaluates are:\n"
        "- Academic Consistency: Steady CGPA combined with SSC and HSC marks.\n"
        "- Practical Experience: Projects and Internships hold significant weight.\n"
        "- Skill Metrics: A balance between Aptitude Test Scores and Soft Skills Rating.\n"
    ))
    pdf.ln(5)

    # Section 2: High-ROI Technical Skills
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "2. High-ROI Technical Skills to Master", 0, 1)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, (
        "To increase your placement prediction score, focus on acquiring highly sought-after skills:\n"
        "- Cloud Computing (AWS/Azure): Gain basic certifications (e.g., AWS Cloud Practitioner).\n"
        "- Full-Stack Development: Master React.js for frontend and Node.js or Python (Flask/Django) for backend.\n"
        "- Data & AI: Familiarity with Pandas, Scikit-Learn, and LLM prompting is increasingly valuable.\n"
        "- DevOps Basics: Learn Docker and Git for CI/CD workflows."
    ))
    pdf.ln(5)

    # Section 3: Soft Skills & Interview Preparation
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "3. Soft Skills & Interview Preparation", 0, 1)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, (
        "Technical skills get you the interview, but soft skills get you the job:\n"
        "- Communication: Practice explaining complex technical concepts simply (The Feynman Technique).\n"
        "- Behavioral Interviews: Use the STAR method (Situation, Task, Action, Result) for HR rounds.\n"
        "- Mock Interviews: Participate in peer-to-peer or AI-driven mock interviews to reduce anxiety."
    ))
    pdf.ln(5)

    # Section 4: Resume & Portfolio Optimization
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "4. Resume & Portfolio Optimization", 0, 1)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, (
        "- ATS Formatting: Ensure your resume is readable by Applicant Tracking Systems (no complex tables or graphics).\n"
        "- Impact-Driven Bullet Points: Don't just list what you did. Use the format: 'Accomplished [X] as measured by [Y], by doing [Z]'.\n"
        "- GitHub Portfolio: Ensure you have 2-3 high-quality, pinned repositories with excellent README files."
    ))
    
    # Save the PDF
    pdf.output(output_path)
    return output_path

if __name__ == "__main__":
    create_placement_guide()
