import os
import sqlite3
import requests
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NASA_API_KEY")

start = date.today()
eind = start + timedelta(days=6)

# database openen (maakt neo.db aan als die nog niet bestaat)
db = sqlite3.connect("neo.db")
db.execute("""
    CREATE TABLE IF NOT EXISTS objecten (
        id TEXT,
        naam TEXT,
        datum TEXT,
        afstand_km REAL,
        grootte_m REAL,
        snelheid_kms REAL,
        gevaarlijk INTEGER,
        PRIMARY KEY (id, datum)
    )
""")

r = requests.get(
    "https://api.nasa.gov/neo/rest/v1/feed",
    params={
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": eind.strftime("%Y-%m-%d"),
        "api_key": API_KEY,
    },
)
data = r.json()

nieuw = 0
for datum, objecten in data["near_earth_objects"].items():
    for obj in objecten:
        nadering = obj["close_approach_data"][0]
        rij = (
            obj["id"],
            obj["name"],
            datum,
            float(nadering["miss_distance"]["kilometers"]),
            obj["estimated_diameter"]["meters"]["estimated_diameter_max"],
            float(nadering["relative_velocity"]["kilometers_per_second"]),
            1 if obj["is_potentially_hazardous_asteroid"] else 0,
        )
        cur = db.execute(
            "INSERT OR IGNORE INTO objecten VALUES (?, ?, ?, ?, ?, ?, ?)", rij
        )
        nieuw += cur.rowcount

db.commit()

totaal = db.execute("SELECT COUNT(*) FROM objecten").fetchone()[0]
print(f"{nieuw} nieuwe objecten opgeslagen, {totaal} in totaal")

print("\nDichtste passages in de database:")
for naam, datum, afstand in db.execute(
    "SELECT naam, datum, afstand_km FROM objecten ORDER BY afstand_km LIMIT 5"
):
    print(f"{naam:30} {datum}   {afstand:>15,.0f} km")

db.close()
