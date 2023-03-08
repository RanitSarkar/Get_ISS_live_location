from flask import Flask,render_template,request
import requests
from requests.structures import CaseInsensitiveDict

app = Flask(__name__,template_folder='template')

longitude=0
latitude=0

data={'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {'result_type': 'postcode', 'city': 'Hawtat Bani Tamim', 'state': 'Riyadh Region', 'postcode': '16521', 'country': 'Saudi Arabia', 'country_code': 'sa', 'datasource': {'sourcename': 'openstreetmap', 'attribution': '© OpenStreetMap contributors', 'license': 'Open Database License', 'url': 'https://www.openstreetmap.org/copyright'}, 'lon': 46.7901066, 'lat': 23.5072157, 'distance': 276478.48943468026, 'formatted': 'Hawtat Bani Tamim 16521, Saudi Arabia', 'address_line1': 'Hawtat Bani Tamim 16521', 'address_line2': 'Saudi Arabia', 'timezone': {'name': 'Asia/Riyadh', 'offset_STD': '+03:00', 'offset_STD_seconds': 10800, 'offset_DST': '+03:00', 'offset_DST_seconds': 10800}, 'rank': {'popularity': 0.6675503045960379}, 'place_id': '5148ad8b3622654740598b845be3d8813740f00101f901f591bd0000000000'}, 'geometry': {'type': 'Point', 'coordinates': [46.7901066, 23.5072157]}}]}


@app.route("/",methods=['GET', 'POST'])
def home():
    global latitude
    global longitude
    global data
    if request.method == "GET":
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()

        data_lat = response.json()
        longitude = data_lat["iss_position"]["longitude"]
        latitude = data_lat["iss_position"]["latitude"]

        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&type=postcode&apiKey=enter-the-API-key-from-geoapify"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        resp = requests.get(url, headers=headers)
        data = resp.json()

    else:
        pass

    return render_template("index.html",state=data["features"][0]["properties"]['state'],
                           country=data["features"][0]["properties"]["country"],
                           postcode=data["features"][0]["properties"]["postcode"],
                           longitude=longitude,latitude=latitude)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)
