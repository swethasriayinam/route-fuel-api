import requests

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjEyNWNjMTZhMThkMjRjZjg5YjVmZjhjZDU2NDQ3ZWVhIiwiaCI6Im11cm11cjY0In0="  

def get_route(start, end):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [start["lng"], start["lat"]],
            [end["lng"], end["lat"]]
        ]
    }

    res = requests.post(url, json=body, headers=headers)

    # ✅ Debug logs
    print("ROUTE STATUS:", res.status_code)
    print("ROUTE RESPONSE:", res.text)

    try:
        data = res.json()
    except:
        return None

    return data