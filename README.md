## 📂 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/sroowo/resume-coverletter-generator.git
cd resume-coverletter-generator
pip install -r requirements.txt
```

### 2. Add your Gemini API key

Create a file named `.streamlit/secrets.toml` and paste the following:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

### 3. Run the app

```bash
streamlit run app.py
```
