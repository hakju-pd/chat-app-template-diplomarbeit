# =============================================================================
#  supabase_client.py
# =============================================================================
#  Hier wird die Verbindung zu Supabase aufgebaut.
#  Außerdem stehen hier ein paar kleine Hilfsfunktionen für die
#  Benutzerverwaltung (Registrieren, Login, Token prüfen).
#
#  WICHTIG:
#  Wir verbinden uns mit dem "service_role"-Schlüssel. Das ist ein
#  Admin-Schlüssel. Damit darf der Server alles und umgeht die
#  Sicherheits-Regeln (RLS). Dieser Schlüssel darf NIEMALS ins Frontend!
# =============================================================================

import os
from pathlib import Path
from supabase import create_client, Client


# .env selbst einlesen – ganz ohne Zusatz-Paket (python-dotenv wird nicht gebraucht).
# Pfad relativ zu dieser Datei, damit es unabhängig vom Arbeitsverzeichnis funktioniert.
def _load_env(path: Path):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        # vorhandene Umgebungsvariablen nicht überschreiben
        os.environ.setdefault(key.strip(), value.strip())


_load_env(Path(__file__).parent / ".env")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

# Freundliche Fehlermeldung, falls die .env Datei vergessen wurde.
if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise RuntimeError(
        "SUPABASE_URL oder SUPABASE_SERVICE_KEY fehlt!\n"
        "Lege eine Datei  .env  an (Vorlage: .env.example) und trage deine Werte ein."
    )

# Der Admin-Client. Den benutzen wir für ALLE Tabellen-Zugriffe.
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


# -----------------------------------------------------------------------------
#  Benutzerverwaltung – kleine Hilfsfunktionen
# -----------------------------------------------------------------------------

def create_user(email: str, password: str):
    """Legt einen neuen Benutzer in Supabase an (E-Mail sofort bestätigt)."""
    result = supabase.auth.admin.create_user({
        "email": email,
        "password": password,
        "email_confirm": True,  # keine Bestätigungs-Mail nötig -> einfacher im Unterricht
    })
    return result.user  # enthält u.a. .id


def login_with_password(email: str, password: str):
    """
    Prüft E-Mail + Passwort und gibt access_token + user_id zurück.
    Gibt None zurück, wenn die Daten falsch sind.

    Hinweis: Wir benutzen hier einen EIGENEN, frischen Client nur für den
    Login. So vermischt sich die Login-Sitzung nicht mit dem Admin-Client.
    """
    client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    try:
        result = client.auth.sign_in_with_password({"email": email, "password": password})
    except Exception:
        return None

    if result.session is None:
        return None

    return {
        "access_token": result.session.access_token,
        "user_id": result.user.id,
    }


def get_user_id_from_token(token: str):
    """
    Prüft einen Login-Token und gibt die user_id zurück.
    Gibt None zurück, wenn der Token ungültig ist.
    """
    try:
        result = supabase.auth.get_user(token)
    except Exception:
        return None

    if result is None or result.user is None:
        return None

    return result.user.id
