import os
import pika
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'marks_queue'

def publish_message(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
    connection.close()

@app.post("/upload-marks/")
async def upload_marks(file: UploadFile = File(...)):
    try:
        folder = "./uploaded_files"
        os.makedirs(folder, exist_ok=True)

        file_location = os.path.join(folder, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        # Publish the path of saved file to RabbitMQ queue
        publish_message(file_location)

        return {"message": f"File '{file.filename}' uploaded and queued for processing."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
