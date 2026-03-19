### KAFKA SETUP

- Make sure you have a Docker daemon running locally
- cd inside the root dir Run command `docker compose up -d`
- Docker compose should create a kafka broker and should listen on port 9092
- Run the python file `python kafka/topics.py`
- Observe that when successful it prints the topics created
- Now that we have the topic created we should run the producer
- Run `app/kafka/producer.py` file using your IDE runner or as an executable file with `python -m (path to)filename`
- Similarly, by following the same process and run the consumer file `app/kafka/consumer.py`
- You should now see the console log with the consumed event and its details
- This shows one complete `producer -> topic -> consumer` flow