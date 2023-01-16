from flask import Flask, request, render_template
import os
from PyPDF2 import PdfReader
import speech_recognition as sr
import pyttsx3
# Python 3.10.9
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf' not in request.files:
        return 'No file selected'
    pdf = request.files['pdf']
    pdf_reader = PdfReader(pdf)
    num_pages = len(pdf_reader.pages)
    engine = pyttsx3.init()
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        engine.save_to_file(text=text,filename=f"page{page_num+1}.wav")
        engine.runAndWait()
        print(f"page{page_num+1}.wav")
    return 'Audio book created!'

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5000, debug = True)


#     <form action="/convert" method="post" enctype="multipart/form-data">
#     <input type="file" name="pdf">
#     <input type="submit" value="Convert">
# </form>

# pip install flask pypdf2 SpeechRecognition PdfReader 
