FROM python:3.10.9-slim-buster


# WORKDIR /home/app
# COPY requirements.txt requirements.txt
RUN pip3 install flask pypdf2 SpeechRecognition PdfReader pyttsx3   comtypes

COPY . .
# # Run cd app && python test.py
# # CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# EXPOSE 5000
# # CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD ["python3","app/test.py"]
WORKDIR /app
# RUN pip install -r requirements.txt
EXPOSE 5000
RUN ls
ENTRYPOINT [ "python" ]
CMD [ "/app/test.py" ]