"""
Module to define kafka producer logic
"""

from datetime import datetime
from uuid import uuid4

from kafka import KafkaProducer

from app.contracts.notification_events import NotificationEvent
from app.core.config import TOPIC

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    client_id="event_producer",
    key_serializer=lambda k: k.encode("utf-8"),
    value_serializer=lambda v: v.model_dump_json().encode("utf-8"),
)


def produce_events(topic: str, event: NotificationEvent):
    """
    kafka producer logic to publish events
    """
    future = producer.send(
        topic=topic, key=f"{event.user_id}:{event.event_type}", value=event
    )

    try:
        metadata = future.get(timeout=10)
        print(f"Event sent successfully to topic: {metadata.topic}")
    except Exception as e:
        raise RuntimeError(f'Failed to send event: {e}') from e


def main():
    """
    main function to execute as a standalone service
    """
    event = NotificationEvent(
        event_id=str(uuid4()),
        event_type="SECURITY_ALERT",
        user_id="3",
        occurred_at=datetime.now(),
        source_service="auth_service",
        schema_version="1",
    )
    produce_events(TOPIC, event)


if __name__ == "__main__":
    main()
