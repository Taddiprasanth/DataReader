from flask import Flask, request, jsonify
import subprocess
import redis
from kafka import KafkaAdminClient

app = Flask(__name__)

# Configure Redis
redis_client = redis.StrictRedis(
    host='redis-18698.c280.us-central1-2.gce.redns.redis-cloud.com',
    port=18698,
    username="default",
    password="BKYiUHXCZv5rL1hI78j5Ph92kog2ZU6g",
    db=0
)

# Configure Kafka
kafka_admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')


@app.route('/start', methods=['POST'])
def start_services():
    try:
        print("Starting services...")
        # Start Microservice 1
        subprocess.Popen(['python', 'C:/Hackthon/MarketDataSimulator/app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        # Start Microservice 2
        subprocess.Popen(['python', 'C:/Hackthon/DataConsumer/app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        # Start Microservice 3
        subprocess.Popen(['python', 'C:/Hackthon/DataConsumer/consumer.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("Microservices started")
        return jsonify({"message": "Microservices started successfully!"}), 200
    except Exception as e:
        print(f"Error starting services: {e}")
        return jsonify({"error": str(e)}), 500



@app.route('/stop', methods=['POST'])
def stop_services():
    try:
        print("Stopping services...")
        subprocess.call(['taskkill', '/IM', 'python.exe', '/F'])
        return "Microservices stopped and cache cleared successfully!"
    except Exception as e:
        print(f"Error stopping services: {e}")  # Debug
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
