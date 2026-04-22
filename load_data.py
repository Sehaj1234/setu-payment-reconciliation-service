import json
import requests

URL = "https://setu-app-67mr2yfzua-el.a.run.app/"

with open("sample_events.json") as f:
    data = json.load(f)

for i, event in enumerate(data):
    response = requests.post(URL, json=event)

    if i % 100 == 0:
        print(f"Inserted {i} events")

print("Done")
