import requests

api_key = "YOUR_API_KEY"
location = "Emart"

url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={location}&key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for result in data["results"]:
        name = result["name"]
        address = result["formatted_address"]
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]
        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Latitude: {lat}")
        print(f"Longitude: {lng}")
else:
    print("Request failed")
