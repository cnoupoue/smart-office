import sys
import requests

def fetch_air_quality(latitude, longitude):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "pm10,pm2_5",
        "timezone": "auto"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Vérifiez si la clé "elevation" existe dans la réponse
        if "elevation" in data:
            return int(data["elevation"])
        else:
            return {"error": "'elevation' key not found in the response"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <latitude> <longitude>")
        sys.exit(1)
    
    latitude = sys.argv[1]
    longitude = sys.argv[2]
    data = fetch_air_quality(latitude, longitude)
    print(data)

