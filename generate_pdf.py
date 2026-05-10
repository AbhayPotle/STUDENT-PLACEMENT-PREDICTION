from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Logo or Title Header
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(41, 128, 185) # Blue
        self.cell(0, 10, 'NexGen AI Placement Insights', new_x="LMARGIN", new_y="NEXT", align='R')
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def create_placement_guide(user_data=None, output_path="Placement_Success_Blueprint.pdf"):
    pdf = PDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", 'B', 24)
    pdf.set_text_color(44, 62, 80) # Dark Blue/Grey
    pdf.cell(0, 20, "Your Personalized Placement Blueprint", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font("helvetica", 'I', 12)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(0, 10, "Data-Driven Approaches to Maximize Your Placement Probability", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)

    if user_data:
        # Personalized Section Header
        pdf.set_fill_color(41, 128, 185) # Blue background
        pdf.set_text_color(255, 255, 255) # White text
        pdf.set_font("helvetica", 'B', 16)
        pdf.cell(0, 12, " Your Personalized Profile Analysis", border=0, new_x="LMARGIN", new_y="NEXT", fill=True, align="C")
        pdf.ln(5)
        
        # Placement Probability Score
        pdf.set_font("helvetica", 'B', 14)
        pdf.set_text_color(44, 62, 80)
        prob = user_data.get('confidence', 'N/A')
        pdf.cell(0, 8, f"Calculated Placement Probability: {prob}", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(5)

        # Target & Fit
        pdf.set_font("helvetica", 'B', 12)
        pdf.set_text_color(44, 62, 80)
        target_co = user_data.get('target_company', 'Top Tech Firms')
        target_co = target_co if target_co.strip() != '' else 'Top Tech Firms'
        pdf.cell(0, 8, f"Target Company: {target_co}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"AI Predicted Fit: {user_data.get('predicted_company', 'N/A')}", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("helvetica", 'I', 11)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 6, user_data.get('job_fit_desc', ''))
        pdf.ln(8)
        
        # Actionable Insights Header
        pdf.set_fill_color(231, 76, 60) # Red background
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", 'B', 14)
        pdf.cell(0, 10, " Critical Actionable Insights to Improve Your Score ", border=0, new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.ln(5)

        pdf.set_font("helvetica", '', 11)
        pdf.set_text_color(0, 0, 0)
        for insight in user_data.get('insights', []):
            # Split the insight to make the first part bold (if it has a colon)
            if ":" in insight:
                title, desc = insight.split(":", 1)
                pdf.set_font("helvetica", 'B', 11)
                pdf.write(6, f"• {title}: ")
                pdf.set_font("helvetica", '', 11)
                pdf.write(6, f"{desc}\n\n")
            else:
                pdf.multi_cell(0, 6, f"• {insight}\n")
        
        pdf.ln(5)
        pdf.add_page()

    # Section 1: How the AI Prediction Model Evaluates You
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 10, "1. How the AI Prediction Model Evaluates You", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, (
        "Our NexGen ML pipeline evaluates your profile using a Logistic Regression model trained on real-world placement data. "
        "It looks at specific metrics to calculate your probability of getting placed. Understanding these metrics is the key "
        "to hacking your placement chances:\n\n"
        "- Academic Consistency (CGPA, SSC, HSC): Your CGPA acts as an initial filter for recruiters (Applicant Tracking Systems). "
        "A consistent score indicates reliability and ability to learn.\n"
        "- Practical Experience (Internships & Projects): These are the highest-impact features. They prove you can apply theoretical "
        "knowledge to solve real-world business problems.\n"
        "- Skill Metrics (Aptitude & Soft Skills): Aptitude clears the first round of assessments; soft skills clear the HR and managerial rounds.\n"
        "- Initiative (Extracurriculars & Training): Shows leadership, teamwork, and a proactive mindset."
    ))
    pdf.ln(8)

    # Section 2: Concrete Approaches to Maximize Probability
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 10, "2. Concrete Approaches to Maximize Probability", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 8, "A. Hacking the 'Projects' Metric (Aim for 3+)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, (
        "Do not just list academic projects. Build 'Proof of Work':\n"
        "- Build Full-Stack Apps: Ensure your projects are hosted live (e.g., Vercel, Netlify) so recruiters can click and interact.\n"
        "- Solve Real Problems: Build an inventory manager, an AI-powered resume analyzer, or a placement tracker.\n"
        "- GitHub Excellence: Ensure every repository has a detailed README.md containing screenshots, architecture diagrams, and installation steps."
    ))
    pdf.ln(4)

    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 8, "B. The 'Internship' Advantage (Aim for 1-2)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, (
        "- Cold Emailing: Reach out directly to startup founders on LinkedIn or Twitter/X. Offer to work for free for 1 month to prove your value.\n"
        "- Open Source: If you can't get a corporate internship, successfully contributing to major Open Source projects (like Mozilla or React) holds equal or more weight in interviews."
    ))
    pdf.ln(4)

    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 8, "C. Elevating 'Aptitude' & 'Soft Skills'", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, (
        "- Aptitude: Dedicate 1 hour daily to Data Interpretation, Logical Reasoning, and Quantitative skills on IndiaBix or HackerRank.\n"
        "- Soft Skills: The 'STAR' Method. Whenever asked a behavioral question, structure your answer using:\n"
        "   S - Situation (What was the context?)\n"
        "   T - Task (What was your specific responsibility?)\n"
        "   A - Action (What exactly did YOU do to solve it?)\n"
        "   R - Result (What was the quantifiable outcome? e.g., 'Improved efficiency by 20%')"
    ))
    pdf.ln(8)

    pdf.add_page()

    # Section 3: High-ROI Technical Skills Timeline
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 10, "3. High-ROI Technical Skills Timeline", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, (
        "If you are short on time, prioritize these specific technologies which currently have the highest market demand:\n\n"
        "Tier 1 (Must Have): Git/GitHub, Linux Basics, SQL, Data Structures & Algorithms (in Python/Java/C++).\n"
        "Tier 2 (Web/Software Dev): React.js (Frontend), Node.js/Express or Python/Django (Backend), RESTful APIs.\n"
        "Tier 3 (Cloud & DevOps): Docker (Containerization), AWS Cloud Practitioner (Certification is a huge bonus), CI/CD pipelines.\n"
        "Tier 4 (AI/Data): Familiarity with LLM APIs (OpenAI/Gemini), Pandas, and basic Machine Learning pipelines."
    ))
    pdf.ln(8)

    # Section 4: Resume & ATS Optimization
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 10, "4. Resume & ATS Optimization Strategy", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, (
        "If your resume gets rejected by the ATS (Applicant Tracking System), an HR person will never even see it.\n\n"
        "- Format: Use a simple, single-column text format (like Jake's Resume template on Overleaf). Avoid graphics, photos, or complex tables.\n"
        "- Keywords: Tailor your resume for every job. If the job description asks for 'Python' and 'REST APIs', ensure those exact words are in your skills section.\n"
        "- Impact Bullet Points: Do not write 'Developed a website'. Write 'Architected a scalable e-commerce frontend using React.js, improving page load speeds by 40% and increasing user retention.'\n"
        "- Metrics: Always use numbers. Quantify your achievements."
    ))

    # Save the PDF
    pdf.output(output_path)
    return output_path

if __name__ == "__main__":
    create_placement_guide()
