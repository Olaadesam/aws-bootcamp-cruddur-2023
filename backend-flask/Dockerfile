#base OS for the container

FROM python:3.10-slim-buster 


WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#copy all information into the container /backend-flask
COPY . .

#Creating an environment variable (ENV)
ENV FLASK_ENV=development

EXPOSE ${PORT}

#python3 -m flask run --host=0.0.0.0 --port=4567 // typing directly into the /backend-flask dir
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]