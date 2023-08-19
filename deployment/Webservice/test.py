import requests

ride = {
    "pickup_community_area": '6',
    "dropoff_community_area": '32',
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=ride)
print(response.json())