# fastapi-mongo-crud

docker build -t fastapi-mongo-crud .
docker run -p 8080:8080 -d --name fastapi-mongo-crud-container fastapi-mongo-crud

docker-compose up --build -d
docker-compose stop
