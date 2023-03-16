# Build stage
FROM node:14 AS build-frontend
WORKDIR /app/frontend
COPY frontend-react-js/package*.json ./
RUN npm install
COPY frontend-react-js/ .
RUN npm run build

# Production stage
FROM python:3.9-slim AS prod-backend
WORKDIR /app/backend
COPY backend-flask/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend-flask/ .
COPY --from=build-frontend /app/frontend/build ./static
CMD ["python", "app.py"]
