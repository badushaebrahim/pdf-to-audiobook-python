from flask import Flask, Response, request, render_template
import os
from PyPDF2 import PdfReader
import speech_recognition as sr
import pyttsx3
import random
from zipfile import ZipFile
import shutil
import time
# Python 3.10.9
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf' not in request.files:
        return 'No file selected'
    start_time = time.time()
    pdf = request.files['pdf']
    pdf_reader = PdfReader(pdf)
    num_pages = len(pdf_reader.pages)
    path = os.getcwd() 
    mode = 0o666
    ran = random.random()
    gen =  str(ran)
    os.mkdir(path=path+"/"+gen,mode=mode)
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 125)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        engine.save_to_file(text=text,filename=path+"/"+gen+"/"+f"page{page_num+1}.mp3")
        engine.runAndWait()
        print(f"page{page_num+1}.wav")
    names_of_zip = f'ffo{gen}.zip'
    with ZipFile(names_of_zip, 'w') as zipObj:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk(path+"/"+gen):
          for filename in filenames:
              #create complete filepath of file in directory
              filePath = os.path.join(folderName, filename)
              # Add file to zip
              zipObj.write(filePath)
    # return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)
    
    with open(names_of_zip, 'rb') as f:
        data = f.read()
    # os.rmdir(path+"/"+gen)
    shutil.rmtree(path=path+"/"+gen)
    print("folder deleted")
    os.remove(names_of_zip)
    print(f"zip deleted {names_of_zip}")
    
    # return the zip file as a response
    end_time = time.time()
    TOTAL =  end_time - start_time
    print(f"total time:{TOTAL}")
    response = Response(data,
                        mimetype="application/zip",
                        headers={"Content-disposition":
                                 "attachment; filename="+names_of_zip})
    return response

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5000, debug = True)


#     <form action="/convert" method="post" enctype="multipart/form-data">
#     <input type="file" name="pdf">
#     <input type="submit" value="Convert">
# </form>

# pip install flask pypdf2 SpeechRecognition PdfReader pyttsx3 zipfile
