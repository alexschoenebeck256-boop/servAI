import redis
import sys
import time
import uuid

def check_redis_pubsub(url):
    try:
        r = redis.from_url(url)
        channel = f"healthcheck:{uuid.uuid4()}"
        p = r.pubsub()
        p.subscribe(channel)
        
        # Give it a moment to subscribe
        time.sleep(0.1)
        
        # Publish a message
        r.publish(channel, "healthcheck")
        
        # Try to get the message
        message = p.get_message(timeout=1.0)
        if message and message['type'] == 'message' and message['data'] == b'healthcheck':
            print("Redis Pub/Sub Health Check: SUCCESS")
            return True
        else:
            print(f"Redis Pub/Sub Health Check: FAILED (Received: {message})")
            return False
    except Exception as e:
        print(f"Redis Pub/Sub Health Check: ERROR ({e})")
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "redis://localhost:6379/0"
    if check_redis_pubsub(url):
        sys.exit(0)
    else:
        sys.exit(1)
