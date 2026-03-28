### KAFKA SETUP

- Make sure you have a Docker daemon running locally
- cd inside the root dir Run command `docker compose build`
- Run `docker compose up`
- Docker compose should start the fast api app along with all the required services like postgresdb, redis etc. and create a kafka broker listening on port 9092
- To create a topic run the python file `python kafka/topics.py`
- Now that we have the topic created we should run the producer
- Run `app/kafka/producer.py` file using your IDE runner or as an executable file with `python -m (path to)filename`
- Similarly, follow the same process and run the consumer file `app/kafka/consumer.py`
- You should now see the console log with the consumed event and its details e.g.
    ```bash
    {"extra": {"event_id": "bd708259-f29d-4605-bcb2-1c6e8b83dfd4", "event_type": "SECURITY_ALERT", 
      "user_id": "3", "source_service": "auth_service", "schema_version": "1", 
      "occurred_at": "datetime.datetime(2026, 3, 19, 16, 29, 55, 965929)"},
      "event": "Consumed event", "timestamp": "2026-03-19T23:30:01.059567Z"}
    ```

- This shows one complete `producer -> topic -> consumer` flow