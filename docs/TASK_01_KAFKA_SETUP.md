# Task 01: Kafka setup and first producer/consumer

**Goal:** Get Kafka running locally and prove the notification platform can **publish** and **consume** notification trigger events using the event schema from the PRD.

**PRD reference:** Section 10 — Event-Driven Notification Triggers (Kafka). Internal services will eventually publish events to a stream; the platform consumes them and applies preference/type rules before delivery. This task is the first step: infrastructure and a minimal producer/consumer.

---

## Scope (in scope for this task)

- Run Kafka (and Zookeeper, if needed) locally via Docker.
- Define the **Notification Trigger Event** schema from the PRD in code (Pydantic).
- Implement a **producer**: one way to send an event into Kafka (e.g. a REST endpoint or a small script).
- Implement a **consumer**: a process or background task that reads from the topic and logs each event (e.g. to stdout or a log).
- Use a single topic (e.g. `notification-trigger-events`) with retention ≥ 7 days (per PRD Section 11).

**Out of scope for now:** Schema Registry, partitioning strategy, idempotency, retries, DLQ, or real notification delivery. Those can be follow-up tasks.

---

## 1. Run Kafka locally

- Add Kafka (and Zookeeper if you use classic Kafka) to your local setup. Since the project already uses Docker for Redis, use **Docker** (e.g. `docker run` or a `docker-compose.yml`).
- Ensure the app can reach Kafka (e.g. `localhost:9092`).
- Create the topic `notification-trigger-events` with retention of at least 7 days (e.g. `retention.ms=604800000`).

**Acceptance:** Kafka is running and the topic exists; you can describe the topic from the command line or via a Kafka tool.

---

## 2. Event schema (from PRD Section 10)

Events must include at least:

| Field           | Description / notes |
|----------------|----------------------|
| `event_id`     | Unique identifier for the event (for deduplication later). |
| `event_type`   | Notification type (e.g. `PASSWORD_RESET`, `SECURITY_ALERT`, `PAYMENT_CONFIRMED`, `SUBSCRIPTION_RENEWAL`). |
| `user_id`      | Target user. |
| `occurred_at`  | When the event occurred (e.g. ISO 8601). |
| `source_service` | Service that produced the event. |
| `payload`      | Optional extra data (e.g. dict or JSON string). |
| `schema_version` | For future schema evolution (e.g. `"1"`). |

- Define a **Pydantic model** for this event in the codebase (e.g. under `app/` or a dedicated `events` module).
- Serialize to JSON when producing to Kafka and parse from JSON when consuming.

**Acceptance:** One canonical model represents the notification trigger event; producer and consumer use it.

---

## 3. Producer

- Add a Kafka producer (e.g. using `aiokafka` or `confluent-kafka`) and configure it with your local broker(s).
- Expose **one** way to send an event into Kafka:
  - **Option A:** REST endpoint (e.g. `POST /api/v1/events/trigger`) that accepts a body matching the event schema and publishes it to `notification-trigger-events`.
  - **Option B:** A small script that builds one event and produces it to the topic.

For ordering (PRD: “per user per notification type when feasible”), use a **message key** when producing (e.g. `user_id` or `f"{user_id}:{event_type}"`) so that all events for the same key go to the same partition.

**Acceptance:** Sending a request (or running the script) results in a message visible in the topic (e.g. via `kafka-console-consumer` or your consumer).

---

## 4. Consumer

- Implement a **consumer** that subscribes to `notification-trigger-events` and, for each message:
  - Deserializes the value to your Pydantic event model.
  - Logs the event (e.g. `logger.info("Consumed event", extra={"event_id": ..., "event_type": ..., "user_id": ...})`).
- Run the consumer so it stays up (e.g. as a separate process or as a background task started in the FastAPI lifespan). No need to persist to DB or call notification delivery yet.

**Acceptance:** When you produce an event (via REST or script), the consumer logs that event with the correct fields.

---

## 5. Configuration and docs

- Add Kafka-related settings to your config (e.g. bootstrap servers, topic name). Use env vars and your existing config pattern (e.g. `app/core/config.py`).
- Update the README (or this doc) with:
  - How to start Kafka (and Zookeeper if applicable) locally.
  - How to run the consumer (if it’s a separate process).
  - Any new env vars (e.g. `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC_NOTIFICATION_TRIGGERS`).

**Acceptance:** Another developer can start Kafka and the app and see one event flow from producer → topic → consumer.

---

## Summary checklist

- [ ] Kafka (and Zookeeper if needed) runs via Docker; topic `notification-trigger-events` exists with ≥ 7 days retention.
- [ ] Pydantic model for the notification trigger event is defined and used for produce/consume.
- [ ] Producer sends events to the topic with a key (e.g. `user_id` or `user_id:event_type`).
- [ ] Consumer subscribes to the topic and logs each consumed event.
- [ ] Config and README document how to run Kafka and the consumer and which env vars are required.

Once this is done, you’ll have a clear base to add partitioning strategy, idempotency, retries, and real notification delivery in later tasks.
