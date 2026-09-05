import os
import sqlite3
import requests
from datetime import date
from dotenv import load_dotenv
from scoring import score, MAAN

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

db = sqlite3.connect("neo.db")
db.row_factory = sqlite3.Row
rijen = db.execute("SELECT * FROM objecten").fetchall()

gescoord = []
for rij in rijen:
    punten, redenen = score(rij)
    gescoord.append((punten, rij))

gescoord.sort(key=lambda x: x[0], reverse=True)
top = gescoord[:20]

# de data in leesbare regels zetten voor het model
regels = []
for punten, rij in top:
    maan = rij["afstand_km"] / MAAN
    regels.append(
        f"{rij['naam']} | {rij['datum']} | {maan:.1f} maanafstanden | "
        f"{rij['grootte_m']:.0f} m | {rij['snelheid_kms']:.1f} km/s | "
        f"gevaarlijk: {'ja' if rij['gevaarlijk'] else 'nee'} | score {punten}"
    )

prompt = f"""Je bent een astronomie-analist. Hieronder staan de {len(top)} hoogst
scorende near-Earth objects uit een database, gesorteerd op een eigen scoringsmodel.

{chr(10).join(regels)}

Ter referentie: 1 maanafstand = 384.400 km. De meeste objecten die langskomen zijn
kleiner dan 100 meter en passeren op meer dan 20 maanafstanden.

Schrijf een korte dagnotitie van maximaal 150 woorden. Benoem wat hier werkelijk
opvalt en waarom, en zeg het eerlijk als er niets bijzonders tussen zit. Geen
alarmerende toon, geen opsomming van alle objecten. Schrijf in het Engels."""

r = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent",
    headers={"x-goog-api-key": GEMINI_KEY, "Content-Type": "application/json"},
    json={"contents": [{"parts": [{"text": prompt}]}]},
)

antwoord = r.json()["candidates"][0]["content"]["parts"][0]["text"]
print(antwoord)


db.execute("""
    CREATE TABLE IF NOT EXISTS notities (
        datum TEXT PRIMARY KEY,
        tekst TEXT
    )
""")
db.execute(
    "INSERT OR REPLACE INTO notities VALUES (?, ?)",
    (date.today().strftime("%Y-%m-%d"), antwoord),
)
db.commit()

db.close()
