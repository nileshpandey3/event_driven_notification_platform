"""
Module to create kafka topics
"""

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, KafkaError

from app.core.config import TOPIC

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092", client_id="topic_creator"
)

topic = NewTopic(
    name=TOPIC,
    num_partitions=3,
    replication_factor=1,
    topic_configs={"retention.ms": "604800000"},
)

# Create Topic
try:
    admin_client.create_topics(new_topics=[topic], validate_only=False)
    print(f"Topic {topic.name} created successfully")

except TopicAlreadyExistsError:
    print("Topic already exists, skipping creation")

# List created topics
try:
    topics = admin_client.list_topics()
    for t in topics:
        print(f'Topic name: "{t}" exists in the cluster')

except KafkaError as e:
    print(f"Encountered kafka error: {e}")

# Describe topics
try:
    topics = admin_client.describe_topics(topics=[topic])
    print(f"Topic description: {topics}")

except KafkaError as e:
    print(f"Encountered kafka error: {e}")

admin_client.close()
