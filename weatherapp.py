import requests
import json

WEATHER_API_KEY = "33431d6a4984c6c1a4e3e9fb82b0ef93"
CITY_NAME = input("Enter city name: ")
COUNTRY_CODE = input("Enter country code (e.g., US for United States): ")
STATE_CODE = input("Enter state code (e.g., CA for California, leave blank if not applicable): ")


geocoding_url =  f"https://api.openweathermap.org/geo/1.0/direct?q={CITY_NAME},{STATE_CODE},{COUNTRY_CODE}&limit=1&appid={WEATHER_API_KEY}"

#   Fetch geocoding data
geo_response = requests.get(geocoding_url)
geo_data = geo_response.json()

#   Extract latitude and longitude from user input
#   The [0] is because the API returns a list of locations, and we want the first one
latitude = geo_data[0]["lat"]
longitude = geo_data[0]["lon"]

weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=imperial"

#   Fetch weather data
weather_response = requests.get(weather_url)
weather_data = weather_response.json()

#   Extract current data
#   The use of main is because the original API 3.0 was a paid version and the free version uses main instead of current
current_weather = weather_data["main"]
current_temperature = current_weather["temp"]
current_feels_like = current_weather["feels_like"]
current_humidity = current_weather["humidity"]

print("\n--- Current Weather Data ---")
print(f"Current Temperature: {current_temperature:.0f}°f")
print(f"Feels Like: {current_feels_like:.0f}°f")
print(f"Humidity: {current_humidity:.0f}%")


max_min_temp = input("Would you like to check out the maximum and minimum temperatures for today? (yes/no): ")
if max_min_temp == "yes":
    max_temperature = current_weather["temp_max"]
    min_temperature = current_weather["temp_min"]
    print("\n--- Max and Min Temperatures for Today ---")
    print(f"Maximum Temperature: {max_temperature:.1f}°f")
    print(f"Minimum Temperature: {min_temperature:.1f}°f")
else:
    print("Okay, skipping today's maximum and minimum temperatures.")

user_moon_phase = input("Would you like to check out the current moon phase? (yes/no): ")
if user_moon_phase == "yes":
    # Using the astral library we can determine the current moon phase by checking the phase number and returning the corresponding phase name
    from astral import moon
    from datetime import date
    phase_number = moon.phase(date.today())
    if phase_number < 1 or phase_number > 27:
        moon_phase = "New Moon"
    elif 1 <= phase_number < 7:
        moon_phase = "Waxing Crescent"
    elif 7 <= phase_number < 8:
        moon_phase = "First Quarter"
    elif 8 <= phase_number < 14:
        moon_phase = "Waxing Gibbous"
    elif 14 <= phase_number < 15:
        moon_phase = "Full Moon"
    elif 15 <= phase_number < 21:
        moon_phase = "Waning Gibbous"
    elif 21 <= phase_number < 22:
        moon_phase = "Last Quarter"
    elif 22 <= phase_number < 27:
        moon_phase = "Waning Crescent"
    print(f"\n--- Current Moon Phase: {moon_phase} ---")

#   Surf Report Section
check_surf = input("\nDo you want to check the surf report for this location? (yes/no): ")
if check_surf == "yes":
    STORMGLASS_API_KEY = "bde3b092-8acb-11f0-a246-0242ac130006-bde3b0f6-8acb-11f0-a246-0242ac130006"
    try:
    # Prepare the API request to Stormglass
        stormglass_url = "https://api.stormglass.io/v2/weather/point"
        params = {
            "lat": latitude,
            "lng": longitude,
            "params": ",".join(["waveHeight"]), # Ask for wave height data
        }
        headers = {
            "Authorization": STORMGLASS_API_KEY
        }
        # Fetch the surf data
        surf_response = requests.get(stormglass_url, params=params, headers=headers)
        surf_data = surf_response.json()
    
        # Extract the wave height (Stormglass returns it in meters)
        # First access "hours", get the first hour [0], and then "waveHeight"
        # >> The "sg" stands for the Stormglass data source <<
        wave_height_meters = surf_data["hours"][0]["waveHeight"]["sg"]
     
        # Convert meters to feet
        wave_height_feet = wave_height_meters * 3.28084

        # Extract wind speed
        wind_data = weather_data["wind"]
        wind_speed = wind_data["speed"]
        wind_gust = wind_data.get("gust", 0) # Some locations may not have gust data and therefore you can call for a safe access

        print("\n--- SURF REPORT ---")
        # The :.2f formats the number to two decimal places
        print("Note: Wave heights can vary throughout the day. Check back often for updates!")
        print(f"Current Wave Height: {wave_height_feet:.2f} ft")
        print(f"Current Wind Speed: {wind_speed:.2f} mph")
        print(f"Current Wind Gusts: {wind_gust:.2f} mph")

    except Exception as e:
        print("\nCould not retrieve surf data for this location.")
        print("Unfortunately this feature is only available for coastal areas.")
        print("If you have used a city that has a coast and still get this message, the Stormglass API has reached its limit of free requests for the day. Sorry!")
