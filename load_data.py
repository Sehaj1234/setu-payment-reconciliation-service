import json
import requests

URL = "http://127.0.0.1:8000/events"

with open("sample_events.json") as f:
    data = json.load(f)

for i, event in enumerate(data):
    response = requests.post(URL, json=event)

    if i % 100 == 0:
        print(f"Inserted {i} events")

print("Done")
