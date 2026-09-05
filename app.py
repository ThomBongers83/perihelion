import sqlite3
import streamlit as st
from scoring import score, MAAN

st.set_page_config(page_title="Perihelion", layout="wide")
st.title("Perihelion")

db = sqlite3.connect("neo.db", check_same_thread=False)
db.row_factory = sqlite3.Row
rijen = db.execute("SELECT * FROM objecten").fetchall()

gescoord = []
for rij in rijen:
    punten, redenen = score(rij)
    gescoord.append((punten, redenen, rij))

gescoord.sort(key=lambda x: x[0], reverse=True)

laatste = db.execute(
    "SELECT datum, tekst FROM notities ORDER BY datum DESC LIMIT 1"
).fetchone()

if laatste:
    st.info(f"**{laatste['datum']}**\n\n{laatste['tekst']}")



min_score = st.slider("Minimale score", 0, 100, 0)
st.caption(f"{len(gescoord)} objecten in database")

for punten, redenen, rij in gescoord:
    if punten < min_score:
        continue

    maan = rij["afstand_km"] / MAAN
    titel = f"{punten} pnt — {rij['naam']} — {maan:.1f} maanafstanden"

    with st.expander(titel):
        kol1, kol2, kol3 = st.columns(3)
        kol1.metric("Grootte", f"{rij['grootte_m']:.0f} m")
        kol2.metric("Afstand", f"{rij['afstand_km']:,.0f} km")
        kol3.metric("Snelheid", f"{rij['snelheid_kms']:.1f} km/s")

        st.write(f"**Datum nadering:** {rij['datum']}")
        st.write(f"**Potentieel gevaarlijk:** {'ja' if rij['gevaarlijk'] else 'nee'}")

        if redenen:
            st.write("**Waarom interessant:** " + ", ".join(redenen))

        st.link_button(
            "Bekijk bij NASA JPL",
            f"https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr={rij['id']}",
        )

db.close()
