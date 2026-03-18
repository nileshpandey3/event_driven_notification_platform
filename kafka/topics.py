from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092", client_id="topic_creator"
)

topic = NewTopic(
    name="notification-trigger-events",
    num_partitions=3,
    replication_factor=1,
    topic_configs={"retention.ms": "604800000"},
)

# Create Topic
try:
    admin_client.create_topics(new_topics=[topic], validate_only=False)
    print(f"Topic {topic.name} created successfully")

except TopicAlreadyExistsError:
    print(f"Topic already exists, skipping creation")

except Exception as e:
    print(f"Error creating Topic: {e}")

# List created topics
try:
    topics = admin_client.list_topics()
    for t in topics:
        print(f'Topic name: "{t}" exists in the cluster')

except Exception as e:
    print(f"Error listing topics: {e}")

admin_client.close()
