"""
Module to define kafka consumer logic
"""

import structlog
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from app.contracts.notification_events import NotificationEvent
from app.core.config import TOPIC
from app.handlers.event_router import EVENT_HANDLER_MAP

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.getLogger("notification_consumer")


def consume_events(topic: str):
    """
    Consume and log events from the producer for a topic
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
