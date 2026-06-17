from datetime import date, datetime
import requests, re

LAT, LON = 32.45, -6.78
today = date.today().isoformat()
biofix = "2026-03-01"

url = (
    f"https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={LAT}&longitude={LON}"
    f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    f"&start_date={biofix}&end_date={today}"
    f"&timezone=Africa/Casablanca"
)

r = requests.get(url)
data = r.json()

tmaxs = data["daily"]["temperature_2m_max"]
tmins = data["daily"]["temperature_2m_min"]

dd_cumul = sum(max(0, (tmax + tmin) / 2 - 10) for tmax, tmin in zip(tmaxs, tmins))

# Met à jour la date dans index.html
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

new_date = f'value="{today}"'
content = re.sub(r'value="\d{4}-\d{2}-\d{2}"', new_date, content, count=1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ Mis à jour : {today} | DD cumulés : {dd_cumul:.1f}")
