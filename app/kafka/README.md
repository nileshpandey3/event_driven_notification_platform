### KAFKA SETUP

- Make sure you have a Docker daemon running locally
- cd inside the root dir Run command `docker compose up -d`
- Docker compose should create a kafka broker and should listen on port 9092
- Run the python file `python kafka/topics.py`
- Observe that when successful it prints the topics created
- Now that we have the topic created we should run the producer
- Run `app/kafka/producer.py` file using your IDE runner or as an executable file with `python -m (path to)filename`
- Similarly, by following the same process and run the consumer file `app/kafka/consumer.py`
- You should now see the console log with the consumed event and its details e.g.
    ```azure
    {"extra": {"event_id": "bd708259-f29d-4605-bcb2-1c6e8b83dfd4", "event_type": "SECURITY_ALERT", "user_id": "3", "source_service": "auth_service", "schema_version": "1", "occurred_at": "datetime.datetime(2026, 3, 19, 16, 29, 55, 965929)"}, "event": "Consumed event", "timestamp": "2026-03-19T23:30:01.059567Z"}
    ```

- This shows one complete `producer -> topic -> consumer` flow