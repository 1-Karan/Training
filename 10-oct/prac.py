import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue = 'student_tasks')

task = {
    'studentID': 120,
    'action': 'graduation certificate',
    'email': 'arspmissesyou@gmail.com'

}

channel.basic_publish(
    exhange ="",
    routing_key= 'students_tasks',
    body=json.dumps(task)
)

print("your message has been sent: ", task)
connection.close()