# Week 1 — App Containerization

I initially encounter an error while trying to run the command without an environmental variable. That was fixed by 


```
cd backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
python3 -m flask run --host=0.0.0.0 --port=4567
cd...

```

###Containerize the backend

Port for 4567 was opened for in your browser
append to the url to /api/activities/home

##Add Dockerfile

backend-flask/Dockerfile

```
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```

the target for the front end is ".../api/activities/home" append it to the url

![Installing AWS CLI](image of open web/CLI.png)
##Build container

```
docker build -t backend-flask ./backend-flask 

```

##Run container

```
docker run --rm -p 4567:4567 -it backend-flask
FRONTEND_URL="*" BACKEND_URL="*" docker run --rm -p 4567:4567 -it backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
docker run --rm -p 4567:4567 -it  -e FRONTEND_URL -e BACKEND_URL backend-flask
```
To remove environment variable
```
unset FRONTEND_URL="*"
unset BACKEND_URL="*"
```
Alternatively run this command:
```
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
```


##Check docker images and running container ids

```
docker images
```

```
check running container
docker container ls
docker ps
```

##Send Curl to Test Server
```
curl -X GET http://localhost:4567/api/activities/home -H "Accept: application/json" -H "Content-Type: application/json"
```

##Check Container Logs

```
docker logs CONTAINER_ID -f
docker logs backend-flask -f
docker logs $CONTAINER_ID -f
```
##Delete an Image

```
docker image rm backend-flask --force
```

##Overriding Ports

```FLASK_ENV=production PORT=8080 docker run -p 4567:4567 -it backend-flask```

###Containerize Frontend


cd frontend-react-js
run
```
npm install
```

##Create Docker File

Create a file here: frontend-react-js/Dockerfile

```
FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```

##Build Container
```
docker build -t frontend-react-js ./frontend-react-js
```

#Run Container
```
docker run -p 3000:3000 -d frontend-react-js
```

###Multiple Containers

##Create a docker-compose file

#Create docker-compose.yml at the root of your project.
```
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js

# the name flag is a hack to change the default prepend folder
# name when outputting the image names
networks: 
  internal-network:
    driver: bridge
    name: cruddur
    ```

#Adding DynamoDB Local and Postgres

Adding Postgres and DynamoDB locally for future labs and bring them in as containers and reference them externally

Integrate the following into the existing docker compose file:

##Postgres
```
services:
  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data
volumes:
  db:
    driver: local
    ```
To install the postgres client into Gitpod
```
  - name: postgres
    init: |
      curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
      echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
      sudo apt update
      sudo apt install -y postgresql-client-13 libpq-dev
      ```
##DynamoDB Local
```
services:
  dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
```

###Homework Challenge

##Run the dockerfile CMD as an external script
Created a new file as .sh under each of frontend and backend
```
#!/bin/bash

docker build -t backend-flask -f Dockefile .

docker run -it backend-flask

```
##Push and tag a image to DockerHub 
Image was pushed to dockerhub created

**Image of the docker images

##Use multi-stage building for a Dockerfile build
Created a new Dockerfile using multistaging method

**image of the docker-mult-stage

##Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes
Created an EC2 instance and installed docker on it
```
sudo yum install -y docker
```
Start docker
```
sudo service docker start
```
Confirm if docker is running
```
sudo docker info
```
##Pull docker image from dockerhub

```
sudo docker pull octaconnect/frontend-react-js

sudo docker pull octaconnect/backend-flask
```








