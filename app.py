from flask import Flask, request, jsonify
import subprocess
import redis
from kafka import KafkaAdminClient

app = Flask(__name__)

# Configure Redis
redis_client = redis.StrictRedis(
    host='redis.finvedic.in',
    port=6379,
    db=0
)

# Configure Kafka
kafka_admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')


@app.route('/start', methods=['POST'])
def start_services():
    try:
        print("Starting services...")
        # List of microservices to start
        services = [
            'C:\\Users\\fnvedicuser\\Downloads\\MarketDataSimulator\\app.py',
            'C:\\Users\\fnvedicuser\\Downloads\\DataConsumer\\app.py',
            'C:\\Users\\fnvedicuser\\Downloads\\DataConsumer\\consumer.py'
        ]

        # Start each service
        for service in services:
            subprocess.Popen(['python', service], creationflags=subprocess.CREATE_NEW_CONSOLE)

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
        return jsonify({"message": "Microservices stopped successfully!"}), 200
    except Exception as e:
        print(f"Error stopping services: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
