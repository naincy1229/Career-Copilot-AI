# utils/report_generator.py

from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Career Copilot AI - Full Report", ln=True, align="C")
        self.ln(10)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def section_body(self, body):
        self.set_font("Arial", "", 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, body)
        self.ln()

def generate_full_report(resume_score=None, jd_match=None, ats_score=None, interview_score=None, suggestions=None):
    pdf = PDFReport()
    pdf.add_page()

    if resume_score:
        score, feedback = resume_score
        pdf.section_title("📄 Resume Score")
        pdf.section_body(f"Score: {score}/100\n\nFeedback:\n{feedback}")

    if jd_match:
        percent, insights = jd_match
        pdf.section_title("📌 JD Match")
        pdf.section_body(f"Match Percentage: {percent}%\n\nInsights:\n{insights}")

    if ats_score:
        pdf.section_title("📊 ATS Score")
        pdf.section_body(
            f"Score: {ats_score['ats_score']} / 100\n"
            f"Matched Keywords: {', '.join(ats_score['matched_keywords']) or 'None'}\n"
            f"Missing Keywords: {', '.join(ats_score['missing_keywords']) or 'None'}\n"
            f"Suggestions: {'; '.join(ats_score['suggestions'])}"
        )

    if interview_score:
        score, tips = interview_score
        pdf.section_title("🎤 Interview Readiness Score")
        pdf.section_body(
            f"Score: {score}/100\n"
            f"Suggestions: {'; '.join(tips)}"
        )

    file_path = "career_report.pdf"
    pdf.output(file_path)
    return file_path
