# Route Fuel Optimization API

## Features
- Convert locations to coordinates
- Calculate route using OpenRouteService
- Find fuel stops using dataset
- Estimate total fuel cost

## Tech Stack
- Django REST Framework
- OpenCage API
- OpenRouteService API
- Pandas + NumPy

## Run Project

pip install -r requirements.txt
python manage.py runserver

## API Endpoint

POST /api/route/

{
  "start": "New York",
  "end": "Los Angeles"
}
