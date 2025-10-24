import pika
import json
import time

# 1. Connect to RabbitMQ (localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# 2. Ensure the queue exists (creates if not present)
channel.queue_declare(queue="student_tasks")

# 3. Define the message handling function (callback)
def callback(ch, method, properties, body):
    task = json.loads(body)  # Convert JSON string to Python dict
    print("Received:", task)

    # Simulate some work (e.g., processing a task)
    time.sleep(2)
    print("Task processed for student:", task["student_id"])

# 4. Tell RabbitMQ to start sending messages to the callback
channel.basic_consume(
    queue="student_tasks",
    on_message_callback=callback,
    auto_ack=True  # Acknowledge message right after it's received
)

print("Waiting for messages. Press CTRL+C to exit.")
channel.start_consuming()
