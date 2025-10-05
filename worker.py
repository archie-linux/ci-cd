import pika, json, os, subprocess

RABBITMQ_HOST = "rabbitmq"
WORKER_ID = os.getenv("WORKER_ID", "worker-unknown")  # Assign worker ID via env variable

def process_job(ch, method, properties, body):
    job_data = json.loads(body)
    job_id = job_data["id"]
    command = job_data["command"]
    
    print(f"[{WORKER_ID}] Processing job {job_id}: {command}")
    
    # Execute command (simulate test execution)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Store job results in a log file
    with open(f"/app/job_results.log", "a") as log_file:
        log_file.write(json.dumps({
            "job_id": job_id,
            "worker_id": WORKER_ID,
            "command": command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": "success" if result.returncode == 0 else "failed"
        }) + "\n")

    print(f"[{WORKER_ID}] Finished job {job_id}")

# RabbitMQ Connection
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='jobs')
channel.basic_consume(queue='jobs', on_message_callback=process_job, auto_ack=True)

print(f"[{WORKER_ID}] Waiting for jobs...")
channel.start_consuming()
