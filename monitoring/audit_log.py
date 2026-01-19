import time, json

def audit(event, payload):
    entry = {
        "time": time.time(),
        "event": event,
        "payload": payload
    }
    with open("audit.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
