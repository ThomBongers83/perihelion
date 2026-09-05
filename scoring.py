MAAN = 384_400

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




