# Week 1 — App Containerization

I initially encounter an error while trying to run the command without an environmental variable. That was fixed by 


```
cd backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
python3 -m flask run --host=0.0.0.0 --port=4567
cd...

```

the target for the front end is ".../api/activities/home" append it to the url

Add DOCKERFILE to the backend-flask and build docker image

```
docker build -t backend-flask ./backend-flask 

```

Run container

```
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
```
Check docker images

```
docker images
```

```
check running container
docker container ls
docker ps
```

cd frontend-react-js
run
```
npm install
```



