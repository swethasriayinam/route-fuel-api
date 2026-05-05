import pandas as pd
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_PATH = os.path.join(BASE_DIR, "data", "fuel_prices.csv")

stations = pd.read_csv(FILE_PATH)


# 🌍 Haversine distance (accurate geo distance)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def find_cheapest_station(lat, lng):
    stations["distance"] = haversine(
        lat,
        lng,
        stations["latitude"].values,
        stations["longitude"].values
    )

    # Nearby within 100 km
    nearby = stations[stations["distance"] < 100]

    if nearby.empty:
        nearby = stations.nsmallest(5, "distance")

    cheapest = nearby.nsmallest(1, "price").iloc[0]

    return {
        "lat": float(cheapest["latitude"]),
        "lng": float(cheapest["longitude"]),
        "price": float(cheapest["price"])
    }


def calculate_fuel_stops(route_points):
    stops = []
    distance_since_last_stop = 0
    MAX_RANGE_KM = 500

    for i in range(0, len(route_points), 50):
        point = route_points[i]

        distance_since_last_stop += 50

        if distance_since_last_stop >= MAX_RANGE_KM:
            stop = find_cheapest_station(point["lat"], point["lng"])

            if not any(
                abs(s["lat"] - stop["lat"]) < 0.01 and
                abs(s["lng"] - stop["lng"]) < 0.01
                for s in stops
            ):
                stops.append(stop)

            distance_since_last_stop = 0

        if len(stops) >= 8:
            break

    return stops


def calculate_total_cost(total_distance, avg_price):
    mileage = 10  # miles per gallon
    gallons = total_distance / mileage
    return gallons * avg_price