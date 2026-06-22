# =============================================================================
#  test_api.py  –  Tests für ALLE Routen des Backends
# =============================================================================
#  Diese Tests sprechen den LAUFENDEN Server an und prüfen jede Route:
#  richtige Eingaben, falsche Eingaben und der Login-Schutz.
#
#  SO TESTEST DU:
#    1. Terminal 1:   python app.py            (Server starten und laufen lassen)
#    2. Terminal 2:   pytest -v                 (aus dem Ordner "backend")
#
#  Wenn alles grün ist (PASSED), funktioniert dein Backend + Supabase. 🎉
# =============================================================================

import os
import uuid
import pytest
import requests

# Adresse des laufenden Servers.
# Standard: Port 5001 (siehe app.py). Falls du einen anderen Port nutzt,
# kannst du ihn hier ändern ODER beim Start setzen:  BASE_URL=... pytest
BASE_URL = os.environ.get("BASE_URL", "http://localhost:5001")

# Zufällige Test-Daten, damit man die Tests beliebig oft laufen lassen kann.
TEST_EMAIL = f"test_{uuid.uuid4().hex[:8]}@example.com"
TEST_PASSWORD = "geheim123"
TEST_USERNAME = f"tester_{uuid.uuid4().hex[:6]}"

# Diese Werte füllen sich während der Tests und werden danach weiterverwendet.
token = None        # Login-Token (nach dem Login)
user_id = None      # ID des Test-Benutzers
room_id = None      # ID eines selbst angelegten Raums


# -----------------------------------------------------------------------------
#  Vorab-Check: Läuft der Server überhaupt? (sonst klare Meldung statt Chaos)
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def server_muss_laufen():
    try:
        requests.get(f"{BASE_URL}/", timeout=3)
    except requests.exceptions.RequestException:
        pytest.skip(
            f"Server nicht erreichbar unter {BASE_URL}. "
            "Läuft 'python app.py' im anderen Terminal?"
        )


# =============================================================================
#  Allgemein
# =============================================================================

def test_server_laeuft():
    """GET /  ->  200 und status ok."""
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# =============================================================================
#  Registrierung  (POST /register)
# =============================================================================

def test_register_ohne_daten_400():
    """Fehlende Felder  ->  400."""
    r = requests.post(f"{BASE_URL}/register", json={})
    assert r.status_code == 400


def test_register_klappt_201():
    """Gültige Registrierung  ->  201 und user_id."""
    r = requests.post(f"{BASE_URL}/register", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "username": TEST_USERNAME,
    })
    assert r.status_code == 201, r.text
    assert "user_id" in r.json()


def test_register_doppelte_email_400():
    """Gleiche E-Mail nochmal  ->  400 (schon vergeben)."""
    r = requests.post(f"{BASE_URL}/register", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "username": TEST_USERNAME + "x",
    })
    assert r.status_code == 400


# =============================================================================
#  Login  (POST /login)
# =============================================================================

def test_login_ohne_daten_400():
    """Fehlende Felder  ->  400."""
    r = requests.post(f"{BASE_URL}/login", json={})
    assert r.status_code == 400


def test_login_falsches_passwort_401():
    """Falsches Passwort  ->  401."""
    r = requests.post(f"{BASE_URL}/login", json={
        "email": TEST_EMAIL,
        "password": "falsch",
    })
    assert r.status_code == 401


def test_login_klappt_200():
    """Richtige Daten  ->  200, access_token und user_id."""
    global token, user_id
    r = requests.post(f"{BASE_URL}/login", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
    })
    assert r.status_code == 200, r.text
    daten = r.json()
    token = daten["access_token"]
    user_id = daten["user_id"]
    assert token        # darf nicht leer sein
    assert user_id


# =============================================================================
#  Räume  (GET /rooms, POST /rooms)
# =============================================================================

def test_rooms_laden_200():
    """GET /rooms  ->  200 und eine Liste (mit den Beispiel-Räumen)."""
    r = requests.get(f"{BASE_URL}/rooms")
    assert r.status_code == 200
    rooms = r.json()
    assert isinstance(rooms, list)
    assert len(rooms) >= 1  # aus schema.sql gibt es Beispiel-Räume


def test_raum_anlegen_ohne_login_401():
    """POST /rooms ohne Token  ->  401 (Schutz greift)."""
    r = requests.post(f"{BASE_URL}/rooms", json={"name": "Geheim"})
    assert r.status_code == 401


def test_raum_anlegen_ohne_name_400():
    """POST /rooms mit Login aber ohne name  ->  400."""
    r = requests.post(
        f"{BASE_URL}/rooms",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 400


def test_raum_anlegen_mit_login_201():
    """POST /rooms mit Login  ->  201, Raum wird angelegt."""
    global room_id
    r = requests.post(
        f"{BASE_URL}/rooms",
        json={"name": f"Testraum {uuid.uuid4().hex[:5]}"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201, r.text
    room_id = r.json()["id"]
    assert room_id


# =============================================================================
#  Nachrichten  (GET / POST /rooms/<id>/messages)
# =============================================================================

def test_nachricht_ohne_login_401():
    """POST Nachricht ohne Token  ->  401."""
    r = requests.post(f"{BASE_URL}/rooms/{room_id}/messages", json={"content": "Hi"})
    assert r.status_code == 401


def test_nachricht_falscher_token_401():
    """POST Nachricht mit kaputtem Token  ->  401."""
    r = requests.post(
        f"{BASE_URL}/rooms/{room_id}/messages",
        json={"content": "Hi"},
        headers={"Authorization": "Bearer total-falscher-token"},
    )
    assert r.status_code == 401


def test_nachricht_ohne_inhalt_400():
    """POST Nachricht mit Login aber ohne content  ->  400."""
    r = requests.post(
        f"{BASE_URL}/rooms/{room_id}/messages",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 400


def test_nachricht_senden_201():
    """POST Nachricht mit Login  ->  201."""
    r = requests.post(
        f"{BASE_URL}/rooms/{room_id}/messages",
        json={"content": "Hallo aus dem Test!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201, r.text
    assert r.json()["content"] == "Hallo aus dem Test!"


def test_nachrichten_laden_200():
    """GET Nachrichten  ->  200, enthält unsere Nachricht inkl. Benutzername."""
    r = requests.get(f"{BASE_URL}/rooms/{room_id}/messages")
    assert r.status_code == 200
    messages = r.json()
    assert isinstance(messages, list)
    assert len(messages) >= 1
    # Die zuletzt gesendete Nachricht sollte dabei sein:
    inhalte = [m["content"] for m in messages]
    assert "Hallo aus dem Test!" in inhalte
    # Der Benutzername wird mitgeliefert (Join auf profiles):
    assert messages[-1]["profiles"]["username"] == TEST_USERNAME


# =============================================================================
#  Profile  (GET /profiles/<id>)
# =============================================================================

def test_profil_laden_200():
    """GET /profiles/<user_id>  ->  200, richtiger Benutzername."""
    r = requests.get(f"{BASE_URL}/profiles/{user_id}")
    assert r.status_code == 200
    assert r.json()["username"] == TEST_USERNAME


def test_profil_nicht_gefunden_404():
    """GET /profiles/<unbekannte id>  ->  404."""
    zufalls_id = str(uuid.uuid4())
    r = requests.get(f"{BASE_URL}/profiles/{zufalls_id}")
    assert r.status_code == 404
