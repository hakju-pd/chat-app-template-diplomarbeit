# =============================================================================
#  app.py  –  Der Startpunkt des Flask-Servers
# =============================================================================
#  Diese Datei macht drei Dinge:
#    1. Flask-App erstellen
#    2. CORS erlauben (damit das Expo-Frontend zugreifen darf)
#    3. Alle Routen aus routes.py einbinden
#
#  STARTEN:   python app.py
# =============================================================================

from flask import Flask
from flask_cors import CORS
from routes import api

app = Flask(__name__)

# CORS = erlaubt, dass die App von einer anderen Adresse (dem Frontend)
# aus auf den Server zugreift.
CORS(app)

# Alle Routen aus routes.py hinzufügen.
app.register_blueprint(api)


@app.get("/")
def index():
    """Kleiner Test: Läuft der Server?"""
    return {"status": "ok", "message": "ChatApp Backend läuft 🎉"}


if __name__ == "__main__":
    # host="0.0.0.0"  ->  der Server ist auch vom Handy im selben WLAN erreichbar.
    # port=5000       ->  die Adresse ist dann  http://<deine-ip>:5000
    # debug=True      ->  der Server startet bei Code-Änderungen automatisch neu.
    app.run(host="0.0.0.0", port=5001, debug=True)
