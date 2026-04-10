"""
Module to define kafka consumer logic
"""

import datetime
import json

import structlog
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from app.contracts.notification_events import NotificationEvent
from app.core.config import TOPIC
from app.core.redis_client import redis_client
from app.handlers.event_router import EVENT_HANDLER_MAP

IDEMPOTENCY_TTL = 86400  # 1 day


def claim_event(event_id: str) -> bool:
    """
    Idempotency Check for incoming events:
    Returns True if event is new, False if duplicate.
    """
    return redis_client.set(
        f"event: {event_id}",
        json.dumps(
            {"status": "processed", "timestamp": datetime.datetime.utcnow().isoformat()}
        ),
        nx=True,
        ex=IDEMPOTENCY_TTL,
    )


# Configure a logger
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.getLogger("notification_consumer")


def consume_events(topic: str):
    """
    Consumer function to consume and log events from the producer
    """
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="localhost:9092",
        client_id="event_consumer",
        auto_offset_reset="earliest",
        key_deserializer=lambda k: k.decode() if k else None,
        value_deserializer=NotificationEvent.model_validate_json,
    )
    for msg in consumer:
        try:
            event: NotificationEvent = msg.value

            logger.info(
                "Consumed event",
                extra={
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "user_id": event.user_id,
                    "source_service": event.source_service,
                    "schema_version": event.schema_version,
                    "occurred_at": event.occurred_at,
                },
            )

            # Idempotency check before sending notification
            if not claim_event(event_id=event.event_id):
                logger.warning(
                    "Skipping duplicate event", extra={"event id": event.event_id}
                )
                continue

            # Route event to the respective handler
            event_handler = EVENT_HANDLER_MAP.get(str(event.event_type))

            if event_handler:
                event_handler(event)
                logger.info(
                    "Event processed successfully",
                    extra={
                        "event_id": event.event_id,
                        "event_type": event.event_type,
                    },
                )
            else:
                logger.warning(
                    "No handler for the event type",
                    extra={
                        "event_type": event.event_type,
                    },
                )

        except KafkaError as e:
            logger.error("KafkaError", error=str(e))
            print(f"Unexpected Error while processing message: {e}")


def main():
    """
    main function to execute as a standalone service
    """
    consume_events(TOPIC)


if __name__ == "__main__":
    main()
