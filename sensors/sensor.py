import requests
import json
import time


API_Key = input("API Key: ")
Sensor_ID = input("Sensor ID: ")
File = input("File: ")

def read_data():
    with open(File) as file:
        return json.load(file)

def main():
    for entry in data:
        entry['SENSOR_EUI'] = Sensor_ID
        s = json.dumps([API_Key, entry])
        print(requests.post("http://127.0.0.1:5555/api/new_sensor_data/", json=s))
        time.sleep(60)


if __name__ == "__main__":
    data = read_data()
    main()