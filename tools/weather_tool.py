from langchain.tools import tool
import os
import re
import requests

from dotenv import load_dotenv
from monitoring.logger import logger

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


@tool
def get_weather(city: str):
    """
    Get current weather information for any city.
    """

    logger.info(f"Weather tool invoked | city={city}")

    if city is None:
        return {
            "success": False,
            "message": "City name is required."
        }

    city = city.strip()

    if not city:
        return {
            "success": False,
            "message": "City name cannot be empty."
        }

    if not re.fullmatch(r"[A-Za-z .'-]+", city):
        return {
            "success": False,
            "message": "Invalid city name."
        }

    if len(city) < 2:
        return {
            "success": False,
            "message": "City name is too short."
        }

    if not API_KEY:
        logger.error("Weather API key not found.")

        return {
            "success": False,
            "message": "Weather API key not found."
        }

    url = "https://api.weatherapi.com/v1/current.json"

    params = {
        "key": API_KEY,
        "q": city
    }

    try:

        logger.info(
            f"Weather API request started | city={city}"
        )

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        logger.info(
            f"Weather API response received | city={city}"
        )

        if "error" in data:

            logger.error(
                f"Weather API error | city={city} | "
                f"message={data['error']['message']}"
            )

            return {
                "success": False,
                "message": data["error"]["message"]
            }

        result = {
            "success": True,
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_kph"]
        }

        logger.info(
            f"Weather tool completed | city={city} | "
            f"condition={result['condition']} | "
            f"temperature={result['temperature']}C"
        )

        return result

    except requests.exceptions.Timeout:

        logger.error(
            f"Weather API timeout | city={city}"
        )

        return {
            "success": False,
            "message": "Weather API request timed out."
        }

    except requests.exceptions.ConnectionError:

        logger.error(
            f"Weather API connection error | city={city}"
        )

        return {
            "success": False,
            "message": "Unable to connect to Weather API."
        }

    except requests.exceptions.RequestException as e:

        logger.error(
            f"Weather API request failed | city={city} | error={str(e)}"
        )

        return {
            "success": False,
            "message": f"Weather API request failed: {str(e)}"
        }

    except Exception as e:

        logger.exception(
            f"Unexpected weather tool error | city={city} | error={str(e)}"
        )

        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}"
        }