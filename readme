Perihelion

An autonomous monitoring agent for near-Earth objects. It fetches NASA data daily, scores each object against a custom model, and uses a language model to write a short analyst note on what actually stands out.

Why

NASA's NEO API tells you what is passing by. It does not tell you what matters. Perihelion adds two layers on top: a deterministic scoring model that ranks objects by distance, size, velocity and hazard classification, and a reasoning layer that judges whether anything is genuinely unusual, and says so plainly when nothing is.

How it works

Ingest. fetch.py pulls a seven-day window from NASA's NeoWs API and stores it in SQLite. The API keeps no history of its own, so this builds one.

Score. scoring.py assigns points across four factors. The thresholds were calibrated against the actual distribution in the dataset rather than theoretical values.

Reason. analyse.py sends the top twenty to Gemini along with the scoring context, and stores the resulting note.

Serve. app.py renders everything in a Streamlit interface.

The language model never filters raw data. Deterministic code narrows thousands of records down to twenty; the model only judges what code cannot.

Automation

A GitHub Actions workflow runs the pipeline every morning at 06:00 UTC and commits the updated database back to the repository. No server, no cost.

Stack

Python, SQLite, Streamlit, NASA NeoWs API, Gemini API, GitHub Actions.

Running locally

Install the dependencies with pip install -r requirements.txt. Create a .env file containing your NASA_API_KEY and GEMINI_API_KEY. Then run fetch.py, analyse.py, and streamlit run app.py in that order.

A note on scoring

The scoring weights are a design choice, not a scientific standard. They reflect what I consider worth surfacing, and they are meant to be adjusted.
