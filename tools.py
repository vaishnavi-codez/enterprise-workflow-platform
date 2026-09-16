import requests
from langchain_core.tools import tool

# -------------------------------------------------------------
# 1. Internal Tool: Calculator
# -------------------------------------------------------------
@tool
def calculator_tool(expression: str) -> str:
    """Useful for evaluating basic mathematical expressions.
    Input should be a valid mathematical string like '2 + 2' or '15 * 3.5'.
    """
    try:
        # Safely evaluate mathematical expressions
        allowed_chars = "0123456789+-*/(). "
        if not all(char in allowed_chars for char in expression):
            return "Error: Invalid characters in mathematical expression."
        result = eval(expression)
        return f"Calculation Result: {result}"
    except Exception as e:
        return f"Error executing calculation: {str(e)}"

# -------------------------------------------------------------
# 2. External Tool: Weather API Connector
# -------------------------------------------------------------
@tool
def weather_tool(city: str) -> str:
    """Useful for retrieving current weather information for a given city name."""
    try:
        # Uses Open-Meteo public geocoding and weather API (no extra API key needed)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url).json()
        
        if not geo_res.get("results"):
            return f"Error: City '{city}' not found."
            
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        city_name = geo_res["results"][0]["name"]
        country = geo_res["results"][0].get("country", "")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(weather_url).json()
        
        curr = w_res.get("current_weather", {})
        temp = curr.get("temperature")
        windspeed = curr.get("windspeed")

        return f"Current weather in {city_name}, {country}: Temperature is {temp}°C with wind speed of {windspeed} km/h."
    except Exception as e:
        return f"Exception handling caught error fetching weather: {str(e)}"

# List of tools to export
agent_tools = [calculator_tool, weather_tool]