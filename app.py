import streamlit as st  #to change code into web apps
import PyPDF2 #read pdf file
from docx import Document  #read word files
from sklearn.feature_extraction.text import CountVectorizer #convert text to numbers
from sklearn.metrics.pairwise import cosine_similarity #calculate similarity
import re #clean text


USER_CREDENTIALS = {
    "admin": "1234",
    "test": "abcd"
}




def login():

    st.title("Login Page")
    username=st.text_input("Username")
    password=st.text_input("Password" , type="password")

    if st.button("login"):

        if username in USER_CREDENTIALS and USER_CREDENTIALS(username)==password:
            st.session_state["loged in"]=True
            st.success("Loged in successfully")

        else:
            st.error("Login failed")

            if "loged in" not in st.session_state:
                st.session_state["loged in"]=False

                if st.set_session["logged in"]:
                    resume_analyzer()
                
                else:
                    login()

                    


def read_resume(file):
    text= ""

    if file.type=="application/pdf":  #check if the file is pdf or not
        reader=PyPDF2.PdfReader(file)   #open pdf file

        for page in reader.pages:
            text += page.extract_text() #extract text from page add each text to text

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document": #check if the file is word or not
        doc = Document(file) #open word file

        for para in doc.paragraphs:
            text += para.text + " "  #add each paragraph with space to text

    elif file.type == "text/plain":
        text = file.getvalue().decode("utf-8")

    return text





#clean text
def clean_text(text):
    text=text.lower() #converts text to lowercase
    text=re.sub(r"[^a-z\s]", "", text)  #removes numbers or punctuations 
    words = text.split() #split each words
    return " ".join(words)  #returns splited words into a string with single space





#analyzer
def resume_analyzer():
    st.title("AI Resume Analyzer")
    resume_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"]) #set it to pdf, docx and txt to upload only this type of files
    jd_text = st.text_area("Paste Job Description Here:") #create a multiline input for job discription


    if st.button("Analyze"):

        if resume_file and jd_text.strip() != "":
            resume_text = read_resume(resume_file)
            resume_text = clean_text(resume_text)
            jd_clean = clean_text(jd_text)


            vectorizer = CountVectorizer() #It converts text into numbers by counting how many times each word appears.
            vectors = vectorizer.fit_transform([resume_text, jd_clean]) 
            
            #Fit → learns the vocabulary of all unique words from both texts.

            #Transform → Converts each text into a vector of numbers.

            score = cosine_similarity(vectors[0], vectors[1])[0][0] 





























