### KAFKA SETUP

- Make sure you have a Docker daemon running locally
- Inside the root dir Run command `docker compose up -d`
- Docker compose up should create a kafka broker and should listen on port 9092
- Run the python file `python kafka/topics.py`
- Observe that when successful it prints the topics created