#to turn Python scripts into interactive web applications 
#without needing to know HTML, CSS, or JavaScript.
import streamlit as st

#to read, write, merge, and manipulate PDF files.
import PyPDF2

#docx is the library used to read and write Microsoft Word (.docx) files in Python.
#Document (capital D) is the class you use to open or create Word documents.
from docx import Document

#CountVectorizer is a text preprocessing tool from scikit-learn
#Its main job is to convert text into numerical features that machine learning models can understand.
from sklearn.feature_extraction.text import CountVectorizer

#Cosine similarity tells us how similar two texts are, regardless of their length.
from sklearn.metrics.pairwise import cosine_similarity

#Resumes and job descriptions can have punctuation, numbers, symbols
#re helps clean the text so CountVectorizer works properly
import re

#Base64 encoding converts binary data (like images, files, or bytes) into a text string
#  using only ASCII characters.
import base64

# ------------------ USER CREDENTIALS ------------------
USER_CREDENTIALS = {"admin": "1234", "test": "abcd"}

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 🔹 Path to your local image (use forward slashes!)
image_path = "D:/AI Analyzer/pexels-boris-pavlikovsky-5498354.jpg"
img_base64 = get_base64_image(image_path)

# 🔹 Inject custom CSS with background
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: 'Trebuchet MS', sans-serif;
    color: #ffffff !important;
}}
.title {{
    color: #ffffff;
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
    margin-bottom: 20px;
}}
</style>
""", unsafe_allow_html=True)

# ------------------ BUTTON STYLING (Login & Analyze) ------------------
st.markdown("""
<style>
.stButton > button, .stFormSubmitButton > button {
    background-color: #996515 !important;
    color: black !important;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background-color: #805000 !important;
    color: black !important;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ------------------ INPUT FIELDS & LABELS ------------------
st.markdown("""
<style>
.stTextInput input, .stTextArea textarea {
    color: #ffffff !important;
    background-color: rgba(0,0,0,0.5) !important;
    border-radius: 8px;
    border: 1px solid #ffffff55;
}
.stTextInput label, .stTextArea label {
    color: #ffffff !important;
}
.stAlert {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ FILE UPLOADER BUTTON ------------------
st.markdown("""
<style>
div.stFileUploader button {
    background-color: #996515 !important;  /* Dark yellow */
    color: black !important;               /* Black text */
    font-weight: bold;
    border-radius: 10px;
    padding: 8px 18px;
    font-size: 16px;
    border: none;
    cursor: pointer;
    transition: 0.3s;
}
div.stFileUploader button:hover {
    background-color: #805000 !important;  /* Darker yellow on hover */
    color: black !important;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ------------------ FUNCTIONS ------------------
def login():
    st.markdown("<h1 class='title'>Login Page</h1>", unsafe_allow_html=True)
    with st.container():
        with st.form("login_form"):
            # Username label in white bold
            st.markdown("<p style='color:white; font-weight:bold;'>Username</p>", unsafe_allow_html=True)
            username = st.text_input("", label_visibility="collapsed")

            # Password label in white bold
            st.markdown("<p style='color:white; font-weight:bold;'>Password</p>", unsafe_allow_html=True)
            password = st.text_input("", type="password", label_visibility="collapsed")

            submit = st.form_submit_button("Login")
            if submit:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state["logged_in"] = True
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Login failed. Try again.")



def read_resume(file):
    text = ""

    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + " "

    elif file.type == "text/plain":
        text = file.getvalue().decode("utf-8")
    return text



def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return " ".join(text.split())



def resume_analyzer():
    st.markdown("<h1 class='title'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)

    # ✅ White label above the uploader
    st.markdown("<p style='color:white; font-weight:bold;'>Upload Resume (PDF, DOCX, TXT)</p>", unsafe_allow_html=True)
    
    # ✅ File uploader with hidden default label
    resume_file = st.file_uploader("", type=["pdf", "docx", "txt"], accept_multiple_files=True, label_visibility="collapsed")

    # White bold label with emoji
    st.markdown("<p style='color:white; font-weight:bold;'>Paste Job Description Here:</p>", unsafe_allow_html=True)

    # Text area without label
    jd_text = st.text_area("", label_visibility="collapsed")


    if st.button("🔍 Analyze"):

        if resume_file and jd_text.strip() != "":
            jd_clean = clean_text(jd_text)

            results=[]

            for file in resume_file:
                resume_text = read_resume(file)
                resume_text = clean_text(resume_text)
                

                vectorizer = CountVectorizer()
                vectors = vectorizer.fit_transform([resume_text, jd_clean])
                score = cosine_similarity(vectors[0], vectors[1])[0][0]

                resume_words = set(resume_text.split())
                jd_words = set(jd_clean.split())
                missing_keywords = jd_words - resume_words
                missing = ", ".join(missing_keywords) if missing_keywords else "None 🎉"

                results.append({
                    "Resume": file.name,
                    "Score": round(score*100, 2),
                    "Missing Keywords": missing
                })

            # Sort by highest score
            results = sorted(results, key=lambda x: x["Score"], reverse=True)

            # Show best resume
            best = results[0]
            st.markdown(f"""
            <div style="background-color:white; color:black; padding:10px; border-radius:8px; font-weight:bold;">
                🏆 Best Resume: {best['Resume']} <br>
                ✅ Match Score: {best['Score']}%
            </div>
            """, unsafe_allow_html=True)

            # Show all resumes in a table
            st.write("📊 Comparison of all resumes:")
            st.dataframe(results)
        else:
            st.warning("⚠️ Please upload a resume and enter a job description.")

# ------------------ SESSION STATE -------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    resume_analyzer()
else:
    login()



#visual diagram showing how a resume and job description are turned into vectors and scored



'''[Resume Text]                     [Job Description Text]
"I am a Python developer ..."      "Looking for Python and ML skills ..."

        |                                  |
        |                                  |
        v                                  v
  CountVectorizer converts             CountVectorizer converts
  each text into numeric              each text into numeric
  vectors (bag-of-words)             vectors (bag-of-words)

Resume Vector:      [1, 2, 0, 1, 0, 3]  
JD Vector:          [1, 1, 1, 0, 1, 2]

        \                                  /
         \                                /
          \                              /
           \                            /
            \                          /
             \                        /
              v                      v
         cosine_similarity(resume_vector, jd_vector)
                     |
                     v
                 Score = 0.82
                     |
                     v
       Convert to percentage → 82%
       Display match score to user
'''