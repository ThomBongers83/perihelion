import sqlite3

MAAN = 384_400

db = sqlite3.connect("neo.db")
db.row_factory = sqlite3.Row


def score(obj):
    punten = 0
    redenen = []

    maan = obj["afstand_km"] / MAAN
    if maan < 30:
        punten += 40
        redenen.append("zeer dichtbij")
    elif maan < 60:
        punten += 25
        redenen.append("relatief dichtbij")
    elif maan < 100:
        punten += 10

    g = obj["grootte_m"]
    if g > 1000:
        punten += 50
        redenen.append("zeer groot (>1 km)")
    elif g > 500:
        punten += 35
        redenen.append("groot object")
    elif g > 200:
        punten += 20
    elif g > 50:
        punten += 8

    if obj["gevaarlijk"]:
        punten += 20
        redenen.append("gemarkeerd als potentieel gevaarlijk")

    if obj["snelheid_kms"] > 25:
        punten += 10
        redenen.append("hoge snelheid")

    return punten, redenen




rijen = db.execute("SELECT * FROM objecten").fetchall()

gescoord = []
for rij in rijen:
    punten, redenen = score(rij)
    gescoord.append((punten, redenen, rij))

gescoord.sort(key=lambda x: x[0], reverse=True)

print(f"{len(rijen)} objecten beoordeeld\n")
print("Top 10:\n")

for punten, redenen, rij in gescoord[:10]:
    maan = rij["afstand_km"] / MAAN
    print(f"{punten:>3} pnt  {rij['naam']:28} {rij['datum']}")
    print(f"          {maan:>6.1f} maanafstanden   {rij['grootte_m']:>6.0f} m")
    if redenen:
        print(f"          → {', '.join(redenen)}")
    print()

mn, mx, gmn, gmx = db.execute("SELECT MIN(afstand_km), MAX(afstand_km), MIN(grootte_m), MAX(grootte_m) FROM objecten").fetchone()
print(f"afstand: {mn:,.0f} - {mx:,.0f} km")
print(f"grootte: {gmn:.0f} - {gmx:.0f} m")

db.close()
