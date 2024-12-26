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
        print("Starting services...")  # Debug
        # Start Microservice 1
        subprocess.Popen(['python', 'C:/Hackthon/MarketDataSimulator/app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        # Start Microservice 2
        subprocess.Popen(['python', 'C:/Hackthon/DataConsumer/app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        # Start Microservice 3
        subprocess.Popen(['python', 'C:/Hackthon/DataConsumer/consumer.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("Microservices started")  # Debug
        return jsonify({"message": "Microservices started successfully!"}), 200
    except Exception as e:
        print(f"Error starting services: {e}")  # Debug
        return jsonify({"error": str(e)}), 500



@app.route('/stop', methods=['POST'])
def stop_services():
    try:
        print("Stopping services...")  # Debug
        # Stop all running microservices using taskkill for Windows
        subprocess.call(['taskkill', '/IM', 'python.exe', '/F'])

        try:
            # Set and get a test key
            redis_client.set('test_key', 'test_value')
            value = redis_client.get('test_key')
            print(f"Value of test_key: {value.decode('utf-8')}")

            # Clear Redis cache
            redis_client.flushdb()
            print("Redis cache cleared successfully!")
        except redis.RedisError as e:
            print(f"Error performing Redis operations: {e}")

        try:
            # Delete Kafka topics
            topic_list = ['market_data']
            kafka_admin_client.delete_topics(topics=topic_list)
            print("Kafka topics deleted")  # Debug
        except Exception as kafka_error:
            print(f"Error deleting Kafka topics: {kafka_error}")  # Debug

        return jsonify({"message": "Microservices stopped and cache cleared successfully!"}), 200
    except Exception as e:
        print(f"Error stopping services: {e}")  # Debug
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
