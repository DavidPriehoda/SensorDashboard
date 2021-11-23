import sys
import requests
import json
import time

def read_data():
    with open("prop_1_kitchen.json") as file:
        return json.load(file)

def main():
    while True:
        for entry in data:
            s = json.dumps(entry)
            res = requests.post("http://127.0.0.1:5555/api/new_sensor_data/", json=s).json()
            print(res)
            time.sleep(10)


if __name__ == "__main__":
    data = read_data()
    main()