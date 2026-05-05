from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.geocoding_service import get_coordinates
from .services.routing_service import get_route
from .services.fuel_service import calculate_fuel_stops, calculate_total_cost


@api_view(["POST"])
def route_api(request):
    start = request.data.get("start")
    end = request.data.get("end")

    if not start or not end:
        return Response({"error": "Start and End required"}, status=400)

    print("INPUT START:", start)
    print("INPUT END:", end)

    # ✅ Step 1: Geocoding
    start_coords = get_coordinates(start)
    end_coords = get_coordinates(end)

    print("START COORDS:", start_coords)
    print("END COORDS:", end_coords)

    if not start_coords or not end_coords:
        return Response({"error": "Geocoding failed"}, status=400)

    # ✅ Step 2: Routing
    route_data = get_route(start_coords, end_coords)

    print("ROUTE DATA:", route_data)

    # ✅ FIX HERE
    routes = route_data.get("routes")
    if not routes:
        return Response({
            "error": "Routing failed",
            "details": route_data
        }, status=400)

    try:
        route = routes[0]

        # distance in miles
        distance = route["summary"]["distance"] / 1609

        # ⚠️ geometry is encoded string
        geometry = route.get("geometry")

        import polyline
        decoded_points = polyline.decode(geometry)

        # convert to dict format
        points = [{"lat": lat, "lng": lng} for lat, lng in decoded_points]

    except Exception as e:
        return Response({
            "error": "Invalid route response",
            "details": str(e),
            "data": route_data
        }, status=500)

    # ✅ Step 3: Fuel stops
    stops = calculate_fuel_stops(points)

    # ✅ Step 4: Cost
    avg_price = sum([s["price"] for s in stops]) / len(stops) if stops else 3
    total_cost = calculate_total_cost(distance, avg_price)

    return Response({
        "distance_miles": distance,
        "fuel_stops": stops,
        "total_cost": total_cost
    })