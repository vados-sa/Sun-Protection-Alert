import requests
from collections import defaultdict

# Berlin's coordinates
LATITUDE = 52.52
LONGITUDE = 13.41

# Build the API URL with our parameters
url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    f"&hourly=uv_index"
    f"&forecast_days=1"
    f"&timezone=Europe%2FBerlin"
)

# Make the HTTP GET request and parse the JSON response
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as exc:
    raise SystemExit(f"Failed to fetch UV forecast data: {exc}")
except ValueError as exc:
    raise SystemExit(f"Failed to parse UV forecast response as JSON: {exc}")

# Extract the two parallel lists we care about
hours = data["hourly"]["time"]
uv_values = data["hourly"]["uv_index"]

# Loop through both lists and keep only hours where UV index is above 2
uv_hours = []
for hour, uv in zip(hours, uv_values):
    if uv > 2:
        uv_hours.append((hour, uv))

print("\n--- Sun Protection Alert ---")

if not uv_hours:
    print("UV levels are low all day. No sunscreen needed — enjoy your time outside!")
else:
    # Group risky hours by date (e.g. "2026-04-14T11:00" → key "2026-04-14")
    by_day = defaultdict(list)
    for hour, uv in uv_hours:
        date = hour.split("T")[0]
        by_day[date].append((hour, uv))

    # Print one alert per day
    for date, day_hours in by_day.items():
        peak_uv = max(uv for _, uv in day_hours)

        # Pick a risk label and advice based on the WHO UV index scale
        if peak_uv >= 11:
            risk = "extreme"
            advice = "Avoid going outside if possible. Full coverage clothing, SPF 50+ sunscreen, and a hat are essential."
        elif peak_uv >= 8:
            risk = "very high"
            advice = "Minimise time in the sun between 10am-4pm. Wear SPF 30+ sunscreen, a hat, and sunglasses."
        elif peak_uv >= 6:
            risk = "high"
            advice = "Apply SPF 30+ sunscreen, wear a hat, and seek shade during midday hours."
        else:
            risk = "moderate"
            advice = "Consider SPF 15+ sunscreen if you'll be outside for more than 30 minutes."

        # Extract just the hour part (e.g. "2026-04-14T11:00" → "11:00")
        first_hour = day_hours[0][0].split("T")[1]
        last_hour = day_hours[-1][0].split("T")[1]

        print(f"\n{date}: UV risk is {risk} (peak index: {peak_uv}) between {first_hour} and {last_hour}.")
        print(advice)