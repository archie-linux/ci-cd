from fastapi import FastAPI
from pydantic import BaseModel
import pika, json, uuid, os

app = FastAPI()
RABBITMQ_HOST = "rabbitmq"
LOG_FILE = "/app/job_results.log"

class JobRequest(BaseModel):
    command: str  

def send_to_queue(job_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='jobs')
    channel.basic_publish(exchange='', routing_key='jobs', body=json.dumps(job_data))
    connection.close()

@app.post("/job")
def create_job(job: JobRequest):
    job_id = str(uuid.uuid4())
    job_data = {"id": job_id, "command": job.command}
    send_to_queue(job_data)
    return {"job_id": job_id, "status": "queued"}
