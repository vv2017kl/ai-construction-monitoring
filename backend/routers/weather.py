"""
Weather API Router
==================

Real weather data integration for construction sites using OpenWeatherMap API
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import os
import httpx
import asyncio
from datetime import datetime

router = APIRouter(prefix="/api/weather", tags=["Weather"])

# Get OpenWeatherMap API key from environment
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@router.get("/", summary="Get current weather")
async def get_current_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get current weather conditions for construction site coordinates"""
    
    # Check if API key is available
    if not OPENWEATHER_API_KEY:
        # Return fallback data if no API key
        return generate_fallback_weather(lat, lon)
    
    try:
        async with httpx.AsyncClient() as client:
            # Call OpenWeatherMap Current Weather API
            response = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "imperial"  # Fahrenheit, mph
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "temp": round(data["main"]["temp"]),
                "conditions": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "wind_speed": data.get("wind", {}).get("speed", 0),
                "humidity": data["main"]["humidity"],
                "visibility": data.get("visibility", 10000),
                "pressure": data["main"]["pressure"],
                "feels_like": round(data["main"]["feels_like"]),
                "temp_min": round(data["main"]["temp_min"]),
                "temp_max": round(data["main"]["temp_max"]),
                "clouds": data.get("clouds", {}).get("all", 0),
                "location": {
                    "name": data.get("name", "Unknown"),
                    "country": data.get("sys", {}).get("country", ""),
                    "lat": lat,
                    "lon": lon
                },
                "timestamp": datetime.now().isoformat(),
                "source": "openweathermap"
            }
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid OpenWeatherMap API key")
        elif e.response.status_code == 429:
            raise HTTPException(status_code=429, detail="Weather API rate limit exceeded")
        else:
            # Return fallback data for other HTTP errors
            return generate_fallback_weather(lat, lon)
    except Exception as e:
        print(f"Weather API error: {e}")
        # Return fallback data for network or other errors
        return generate_fallback_weather(lat, lon)

@router.get("/forecast", summary="Get weather forecast")
async def get_weather_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    days: int = Query(5, description="Number of days to forecast", ge=1, le=7)
):
    """Get weather forecast for construction planning"""
    
    if not OPENWEATHER_API_KEY:
        return {"forecast": generate_fallback_forecast(days)}
    
    try:
        async with httpx.AsyncClient() as client:
            # Call OpenWeatherMap 5-Day Forecast API
            response = await client.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "imperial"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Process forecast data
            forecast = []
            processed_dates = set()
            
            for item in data["list"][:days * 8]:  # 8 forecasts per day (3-hour intervals)
                forecast_date = datetime.fromtimestamp(item["dt"]).date()
                
                if forecast_date not in processed_dates:
                    forecast.append({
                        "date": forecast_date.isoformat(),
                        "temperature": {
                            "high": round(item["main"]["temp_max"]),
                            "low": round(item["main"]["temp_min"])
                        },
                        "condition": item["weather"][0]["main"],
                        "description": item["weather"][0]["description"],
                        "precipitation": item.get("rain", {}).get("3h", 0) + item.get("snow", {}).get("3h", 0),
                        "wind_speed": item.get("wind", {}).get("speed", 0),
                        "humidity": item["main"]["humidity"],
                        "clouds": item.get("clouds", {}).get("all", 0)
                    })
                    processed_dates.add(forecast_date)
                    
                if len(forecast) >= days:
                    break
            
            return {
                "forecast": forecast,
                "location": {
                    "name": data.get("city", {}).get("name", "Unknown"),
                    "country": data.get("city", {}).get("country", ""),
                    "lat": lat,
                    "lon": lon
                },
                "source": "openweathermap"
            }
            
    except Exception as e:
        print(f"Weather forecast error: {e}")
        return {"forecast": generate_fallback_forecast(days)}

@router.get("/alerts", summary="Get weather alerts")
async def get_weather_alerts(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get weather alerts affecting construction work"""
    
    if not OPENWEATHER_API_KEY:
        return {"alerts": []}
    
    try:
        async with httpx.AsyncClient() as client:
            # Call OpenWeatherMap One Call API for alerts
            response = await client.get(
                "https://api.openweathermap.org/data/3.0/onecall",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": OPENWEATHER_API_KEY,
                    "exclude": "minutely,hourly,daily"  # Only get current and alerts
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            alerts = []
            if "alerts" in data:
                for alert in data["alerts"]:
                    alerts.append({
                        "title": alert.get("event", "Weather Alert"),
                        "description": alert.get("description", ""),
                        "severity": alert.get("severity", "moderate"),
                        "start": datetime.fromtimestamp(alert.get("start", 0)).isoformat(),
                        "end": datetime.fromtimestamp(alert.get("end", 0)).isoformat(),
                        "sender": alert.get("sender_name", "Weather Service")
                    })
            
            return {"alerts": alerts}
            
    except Exception as e:
        print(f"Weather alerts error: {e}")
        return {"alerts": []}

def generate_fallback_weather(lat: float, lon: float) -> dict:
    """Generate realistic fallback weather data when API is unavailable"""
    import random
    from datetime import datetime
    
    # Seasonal temperature adjustment
    month = datetime.now().month
    base_temp = 60
    
    if month in [12, 1, 2]:  # Winter
        base_temp = 35
    elif month in [6, 7, 8]:  # Summer
        base_temp = 75
    elif month in [3, 4, 5]:  # Spring
        base_temp = 55
    else:  # Fall
        base_temp = 50
    
    # Latitude adjustment (colder in north)
    if lat > 45:
        base_temp -= 10
    elif lat < 35:
        base_temp += 15
    
    temp = base_temp + random.randint(-15, 15)
    
    conditions = ["Clear", "Partly Cloudy", "Cloudy", "Overcast"]
    if month in [12, 1, 2] and lat > 40:
        conditions.extend(["Snow", "Light Snow"])
    if month in [4, 5, 9, 10]:
        conditions.extend(["Light Rain", "Rain"])
    
    condition = random.choice(conditions)
    
    return {
        "temp": temp,
        "conditions": condition,
        "description": condition.lower(),
        "wind_speed": random.randint(3, 20),
        "humidity": random.randint(30, 80),
        "visibility": 10000,
        "pressure": random.randint(1000, 1030),
        "feels_like": temp + random.randint(-5, 5),
        "temp_min": temp - random.randint(3, 8),
        "temp_max": temp + random.randint(3, 8),
        "clouds": random.randint(0, 100),
        "location": {
            "name": "Construction Site",
            "country": "US",
            "lat": lat,
            "lon": lon
        },
        "timestamp": datetime.now().isoformat(),
        "source": "fallback",
        "note": "Weather API unavailable - using estimated conditions based on location and season"
    }

def generate_fallback_forecast(days: int) -> list:
    """Generate fallback forecast data"""
    import random
    from datetime import datetime, timedelta
    
    forecast = []
    base_temp = 60
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        temp = base_temp + random.randint(-10, 10)
        
        forecast.append({
            "date": date.date().isoformat(),
            "temperature": {
                "high": temp + random.randint(5, 15),
                "low": temp - random.randint(5, 15)
            },
            "condition": random.choice(["Clear", "Partly Cloudy", "Cloudy", "Light Rain"]),
            "description": "Estimated conditions",
            "precipitation": random.randint(0, 30),
            "wind_speed": random.randint(5, 25),
            "humidity": random.randint(40, 80),
            "clouds": random.randint(0, 100)
        })
    
    return forecast