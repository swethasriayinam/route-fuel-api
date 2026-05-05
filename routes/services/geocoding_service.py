import requests

API_KEY = "48938f31052a41ab9adbb22cd618a39c"  # 👈 your OpenCage key

def get_coordinates(place_name):
    url = "https://api.opencagedata.com/geocode/v1/json"
    
    params = {
        "q": place_name,
        "key": API_KEY
    }

    res = requests.get(url, params=params)

    print("GEOCODING STATUS:", res.status_code)
    print("GEOCODING RESPONSE:", res.text)

    data = res.json()

    if data.get("results"):
        lat = data["results"][0]["geometry"]["lat"]
        lng = data["results"][0]["geometry"]["lng"]
        return {"lat": lat, "lng": lng}

    return None