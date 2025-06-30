# Enhanced HTML themes for resume preview
# pip install streamlit-lottie
import re
import streamlit as st
from google.generativeai import GenerativeModel, configure
from dotenv import load_dotenv
import os
from fpdf import FPDF
import requests

def render_html_resume(text, theme):
    # Replace markdown-style **bold** with HTML <strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    # Build HTML content line-by-line with proper <ul> grouping
    lines = text.split('\n')
    html_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('* '):
            item = stripped[2:]
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'{stripped}<br>')

    if in_list:
        html_lines.append('</ul>')

    content = '\n'.join(html_lines)

    base_css = '''
    <style>
        .resume-box {{
            font-family: 'Helvetica', sans-serif;
            padding: 2rem;
            border-radius: 8px;
            margin-top: 1rem;
            line-height: 1.6;
            white-space: normal;
            background-color: {bg_color};
            color: {text_color};
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}
        .resume-box strong {{
            display: block;
            margin-top: 1rem;
            font-size: 1.1rem;
            color: {header_color};
            border-bottom: 1px solid #ccc;
            padding-bottom: 4px;
        }}
        .resume-box ul {{
            padding-left: 20px;
            margin-top: 0.5rem;
        }}
        .resume-box li {{
            margin-bottom: 0.3rem;
        }}
    </style>
    <div class="resume-box" style="border: 2px dashed #ffd6ea; background-color: #4a0d3d; padding: 2rem; border-radius: 12px; margin-top: 1rem; color: #ffe4f0; box-shadow: 0 4px 10px rgba(255, 182, 193, 0.2);">{content}</div>
    '''

    if theme == "Formal":
        return base_css.format(bg_color="#ffffff", text_color="#000000", header_color="#1a1a1a", content=content)
    elif theme == "Creative":
        return base_css.format(bg_color="#fff0f5", text_color="#4b0082", header_color="#d63384", content=content)
    elif theme == "Technical":
        return base_css.format(bg_color="#f5f7fa", text_color="#1f2937", header_color="#2563eb", content=content)
    else:
        return base_css.format(bg_color="#ffffff", text_color="#000000", header_color="#1a1a1a", content=content)
# app.py


# Function to convert text to PDF
def text_to_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        clean_line = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 10, clean_line)
    pdf.output(filename)

# Load API key
load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))
try:
    model = GenerativeModel("gemini-1.5-flash")
except Exception:
    model = GenerativeModel("gemini-1.5-pro")

# Ensure you are using the latest Gemini SDK:
# Run the following command in your terminal to upgrade:
# pip install -U google-generativeai


st.set_page_config(page_title="Resume & Cover Letter Generator", layout="centered")

# Always apply dark mode styling directly
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

        html, body {
            font-family: 'Quicksand', sans-serif;
        }
        .resume-box,
        .cover-letter-box {
            border: 2px dashed #ffd6ea;
            background-color: #4a0d3d;
            padding: 2rem;
            border-radius: 12px;
            margin-top: 1rem;
            color: #ffe4f0;
            box-shadow: 0 4px 10px rgba(255, 182, 193, 0.2);
        }
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #3b0a34 !important;
            font-family: 'Poppins', 'Segoe UI', sans-serif;
            color: #ffe4f0 !important;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stSelectbox,
        .stFileUploader {
            background-color: #4a0d3d !important;
            border: 1.5px solid #ff9ecb;
            border-radius: 12px;
        }
        .stTextInput input,
        .stTextArea textarea,
        .stTextInput > div > div > input,
        .stTextArea > div > textarea {
            background-color: #4a0d3d !important;
            color: #ffe4f0 !important;
            border-radius: 12px;
            border: 1.5px solid #ff9ecb;
            padding: 0.75rem;
            font-size: 0.95rem;
        }

        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stFileUploader label {
            color: #ffd0df !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #ffc6da !important;
            opacity: 1;
        }
        .stButton button {
            background-color: #ff8ab3;
            color: white;
            border: none;
            padding: 0.75rem 1.75rem;
            font-size: 1rem;
            border-radius: 12px;
            font-weight: 600;
            box-shadow: 0px 2px 6px rgba(255, 133, 179, 0.4);
            transition: background-color 0.3s ease, transform 0.1s ease;
            margin-top: 1rem;
        }
        .stButton button:hover {
            background-color: #ff4c91;
            transform: scale(1.02);
        }
        h1, h2, h3, h4 {
            color: #ffb6c1;
            font-weight: 700;
        }
        .stRadio > div {
            background-color: #531537;
            color: #ffe4f0;
            padding: 1rem;
            border-radius: 16px;
            border: 1.5px solid #ff9ecb;
            box-shadow: 0 5px 12px rgba(255, 182, 193, 0.2);
            margin-bottom: 1.5rem;
        }
        .stSubheader {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #ffb0d4;
        }
        #MainMenu, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

from pathlib import Path
from io import StringIO
import base64
from PIL import Image

col1, col2 = st.columns([1, 8])
with col1:
    image = Image.open("_ (1).jpeg")
    st.image(image, width=160)
with col2:
    st.markdown(
        "<div style='display: flex; align-items: center; height: 100%;'><h2 style='margin: 0;'> Resume and Cover Letter Generator</h2></div>",
        unsafe_allow_html=True
    )


import random
quotes = [
    "You got this! 💪💖",
    "Believe in yourself — you’re resume-ready! ✨",
    "Every great journey starts with a single click 🚀",
    "Shine bright, you're doing amazing! 🌟",
    "One step closer to your dream job! 📝"
]
st.markdown(f"#### 💬 {random.choice(quotes)}")


page = st.radio("Choose what you want to do:", ["Generate New Resume", "Improve Existing Resume", "Build My Portfolio"])

if page == "Improve Existing Resume":
    st.header("📤 Upload Your Resume for AI Enhancement")
    uploaded_file = st.file_uploader("Upload your resume (.txt, .pdf, or .docx)", type=["txt", "pdf", "docx"])
    job_title = st.text_input("Job Role You're Targeting")
    if uploaded_file and job_title:
        uploaded_text = ""
        if uploaded_file.name.endswith(".txt"):
            uploaded_text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        elif uploaded_file.name.endswith(".pdf"):
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                uploaded_text += page.extract_text() or ""
        elif uploaded_file.name.endswith(".docx"):
            import docx
            doc = docx.Document(uploaded_file)
            uploaded_text = "\n".join([para.text for para in doc.paragraphs])
        improve_prompt = f"""Improve and rewrite the following resume to match a {job_title} position. Make it professional and ATS-friendly:\n\n{uploaded_text}"""
        with st.spinner("Improving your resume..."):
            improved = model.generate_content(improve_prompt)
            st.subheader("✨ Improved Resume")
            st.session_state.resume_text = improved.text
            st.markdown(f'<div style="border: 2px dashed #ffd6ea; background-color: #4a0d3d; padding: 2rem; border-radius: 12px; margin-top: 1rem; color: #ffe4f0; box-shadow: 0 4px 10px rgba(255, 182, 193, 0.2);">{st.session_state.resume_text}</div>', unsafe_allow_html=True)
            edited_resume = st.text_area("✏️ Edit Improved Resume Before Download", improved.text, height=300)
            text_to_pdf(edited_resume, "resume.pdf")
            with open("resume.pdf", "rb") as file:
                st.download_button("📥 Download Enhanced Resume as PDF", file.read(), file_name="resume.pdf", mime="application/pdf")
    st.stop()

if page == "Generate New Resume":
    st.write("Fill in your details below:")

    # User Input Form
    with st.form("resume_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")

        education = st.text_area("Education (e.g., BTech in CSE with Data Science)")
        experience = st.text_area("Work Experience (e.g., Intern at XYZ, used React, etc.)")
        skills = st.text_input("Skills (comma-separated)")
        job_role = st.text_input("Job Role You’re Applying For")
        
        cover_tone = st.radio(
            "Choose Cover Letter Tone",
            ["Professional", "Confident", "Friendly", "Witty"],
            horizontal=True
        )

        template = st.radio(
            "Choose Resume Template Style",
            ["Formal", "Creative", "Technical"],
            horizontal=True
        )

        submitted = st.form_submit_button("Generate")
        if "resume_text" not in st.session_state:
            st.session_state.resume_text = ""
        if "cover_letter_text" not in st.session_state:
            st.session_state.cover_letter_text = ""

    if submitted and not all([name, email, phone, education, experience, skills, job_role]):
        st.error("Please fill in all fields before generating.")
        st.stop()

    if submitted:
        if template == "Formal":
            style_note = "Use a professional and concise tone suitable for corporate jobs."
        elif template == "Creative":
            style_note = "Use a friendly and creative tone, ideal for design, writing, or marketing roles."
        elif template == "Technical":
            style_note = "Use a precise and skill-focused tone suitable for tech roles like software engineering."


        with st.spinner("Generating resume and cover letter..."):
            prompt_resume = f"""Generate a {template.lower()}-style professional resume. {style_note}

Include:
- A strong summary section
- Bullet-pointed key skills
- Experience in a readable format

Candidate Info:
Name: {name}
Email: {email}
Phone: {phone}
Education: {education}
Experience: {experience}
Skills: {skills}
"""

            prompt_cover_letter = f"""Write a {cover_tone.lower()} cover letter tailored for the role: {job_role}.
Candidate Information:
Name: {name}
Education: {education}
Experience: {experience}
Skills: {skills}
"""

            # Generate Resume
            response_resume = model.generate_content(prompt_resume)
            st.session_state.resume_text = response_resume.text

            # Generate Cover Letter
            response_cover = model.generate_content(prompt_cover_letter)
            st.session_state.cover_letter_text = response_cover.text

    if st.session_state.resume_text:
        st.subheader("📄 Generated Resume")
        st.markdown(f'<div style="border: 2px dashed #ffd6ea; background-color: #4a0d3d; padding: 2rem; border-radius: 12px; margin-top: 1rem; color: #ffe4f0; box-shadow: 0 4px 10px rgba(255, 182, 193, 0.2); margin-bottom: 2rem;">{st.session_state.resume_text}</div>', unsafe_allow_html=True)
        mao_heart = Image.open("mao_heart.jpeg")
        st.image(mao_heart, width=130, caption="All done! 💖")
        st.subheader("✏️ Edit Resume Before Download")
        edited_resume = st.text_area("Modify your resume below:", st.session_state.resume_text, height=300)
        text_to_pdf(edited_resume, "resume.pdf")
        with open("resume.pdf", "rb") as file:
            st.download_button("📥 Download Edited Resume as PDF", file.read(), file_name="resume.pdf", mime="application/pdf")
        st.components.v1.html("""
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<script>
confetti({
  particleCount: 50,
  spread: 60,
  origin: { y: 0.6 },
  colors: ['#ffb6c1', '#ffd6ea', '#fff0f5'],
  scalar: 0.6,
  ticks: 200
});
</script>
""", height=0)

    if st.session_state.cover_letter_text:
        st.subheader("✉️ Generated Cover Letter")
        st.markdown(f'<div style="border: 2px dashed #ffd6ea; background-color: #4a0d3d; padding: 2rem; border-radius: 12px; margin-top: 1rem; color: #ffe4f0; box-shadow: 0 4px 10px rgba(255, 182, 193, 0.2); margin-bottom: 2rem;">{st.session_state.cover_letter_text}</div>', unsafe_allow_html=True)
        cover_cat = Image.open("cover_cat.jpeg")
        st.image(cover_cat, width=130, caption="Here’s your cover letter 💌")
        # text_to_pdf(st.session_state.cover_letter_text, "cover_letter.pdf")
        # with open("cover_letter.pdf", "rb") as file:
        #     st.download_button("📥 Download Cover Letter as PDF", file.read(), file_name="cover_letter.pdf", mime="application/pdf")
        st.subheader("✏️ Edit Cover Letter Before Download")
        edited_cover = st.text_area("Modify your cover letter below:", st.session_state.cover_letter_text, height=300)
        text_to_pdf(edited_cover, "cover_letter.pdf")
        with open("cover_letter.pdf", "rb") as file:
            st.download_button("📥 Download Edited Cover Letter as PDF", file.read(), file_name="cover_letter.pdf", mime="application/pdf")

# --- Portfolio & Skill Gap Planner ---
if page == "Build My Portfolio":
    st.header("🧭 Portfolio & Skill Gap Planner")
    current_skills = st.text_area("🧠 Enter your current skills (comma-separated)", placeholder="e.g., Python, HTML, SQL")
    job_description = st.text_area("📋 Paste the job description of your desired role", height=250)

    # Maintain roadmap_text in session state
    if "roadmap_text" not in st.session_state:
        st.session_state.roadmap_text = ""

    if st.button("🔮 Generate Skill Roadmap"):
        if not current_skills or not job_description:
            st.error("Please fill out both fields.")
            st.stop()

        roadmap_prompt = f"""
You are an AI career coach.

The user has the following current skills:
{current_skills}

They are aiming for a job with this description:
{job_description}

1. Identify which additional skills/tools the user should learn (in order of priority).
2. For each skill, explain briefly why it is important.
3. Suggest a learning path (beginner → intermediate → advanced).
4. Recommend at least one project idea for each skill to showcase it in a portfolio.

Respond in a clear, motivational, roadmap-style format.
"""

        with st.spinner("Crafting your personalized roadmap..."):
            roadmap_response = model.generate_content(roadmap_prompt)
            st.session_state.roadmap_text = roadmap_response.text

    # Show the roadmap if present in session state
    if st.session_state.roadmap_text:
        st.markdown("### 📚 Recommended Resources")
        skills = [line.strip("•-– ") for line in st.session_state.roadmap_text.split("\n") if any(keyword in line.lower() for keyword in ["learn", "skill", "tool", "language", "technology"])][:8]
        resource_prompt = f"""
For each of these skills: {', '.join(skills[:3])}, suggest one high-quality online resource (like Udemy, Coursera, YouTube, or official documentation).
Present them as a bullet list with clickable hyperlinks.
"""
        resource_response = model.generate_content(resource_prompt)
        st.markdown(resource_response.text, unsafe_allow_html=True)

        st.markdown("### 🗺️ Your Personalized Career Roadmap")
        st.markdown(f'<div style="border: 2px dashed #ffd6ea; background-color: #4a0d3d; padding: 2rem; border-radius: 12px; margin-top: 1rem; color: #ffe4f0; box-shadow: 0 4px 10px rgba(255, 182, 193, 0.2); margin-bottom: 2rem;">{st.session_state.roadmap_text}</div>', unsafe_allow_html=True)

        # ✅ Generate PDF from session state text
        import io
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in st.session_state.roadmap_text.split('\n'):
            clean_line = line.encode("latin-1", "replace").decode("latin-1")
            clean_line = clean_line.replace("*", "").strip()
            clean_line = clean_line.replace("#", "").strip()
            if clean_line.strip().startswith(("1.", "2.", "3.", "4.", "-", "*")):
                pdf.set_font("Arial", style="B", size=12)
            else:
                pdf.set_font("Arial", style="", size=12)
            pdf.multi_cell(0, 10, clean_line)

        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_buffer = io.BytesIO(pdf_bytes)

        st.download_button("⬇️ Download Career Roadmap PDF", pdf_buffer, file_name="roadmap.pdf", mime="application/pdf", use_container_width=True)