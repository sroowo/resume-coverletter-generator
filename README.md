# 📄 Resume & Cover Letter Generator + AI Career Roadmap

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-ff4b4b?logo=streamlit&style=flat-square)](https://sroowo-resume-coverletter-generator.streamlit.app)
[![Made with Gemini](https://img.shields.io/badge/Made_with-Gemini_AI-blueviolet?logo=google&style=flat-square)](https://ai.google.dev)
[![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)](LICENSE)

> ✨ A Gemini-powered Streamlit app to help users generate polished resumes, tailored cover letters, and personalized career roadmaps — all in one pastel-themed UI.

## 🚀 Live Demo

🔗 [Try it here](https://sroowo-resume-coverletter-generator.streamlit.app)

## ✨ Features

- 🎨 Generate beautiful resumes in **Formal**, **Creative**, or **Technical** styles  
- 💌 Write cover letters in **Professional**, **Confident**, **Friendly**, or **Witty** tones  
- 📥 Upload an existing resume (PDF, DOCX, TXT) and enhance it with AI  
- 🗺️ Build a **personalized skill roadmap** based on your current skills and a target job  
- 📚 Get **recommended learning resources** and project ideas  
- 📄 Download final resume, cover letter, and roadmap as **PDFs**  
- 🎉 Pastel dark-mode interface with positive quotes and confetti  

## 🛠️ Tech Stack

	•	Streamlit – UI framework
	•	Gemini API – by Google Generative AI
	•	fpdf – for PDF creation
	•	Pillow – image processing
	•	PyPDF2, python-docx – file handling
	•	.streamlit/secrets.toml – secret key management


## 📸 App Preview

### 🏠 Resume & Cover Letter Generator (Home)
![First Page](firstpage.png)

### 📄 Improve Existing Resume
![Second Page](firstpage2.png)

### 🗺️ Build My Portfolio / Career Roadmap
![Third Page](secondpage.png)

### 🔍 Additional View (Portfolio continued)
![Additional View](thirdpage.png)


## 📂 How to Run Locally

```bash
git clone https://github.com/sroowo/resume-coverletter-generator.git
cd resume-coverletter-generator
pip install -r requirements.txt

## Then create a file:

.streamlit/secrets.toml

## Inside it, paste your Gemini API key:

GEMINI_API_KEY = "your-api-key-here"

## Then run the app:

streamlit run app.py



Built With Love By

Hemal Sri V
🎓 Final-year BTech (CSE - Data Science)
🌐 GitHub: @sroowo
