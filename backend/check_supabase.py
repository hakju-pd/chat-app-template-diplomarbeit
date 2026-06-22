# =============================================================================
#  check_supabase.py  –  Diagnose: Stimmen Verbindung, Key und Tabellen?
# =============================================================================
#  Ausführen (im Ordner backend, venv aktiv):   python check_supabase.py
#  Zeigt: ob die .env passt, welcher Key-Typ benutzt wird, ob die Tabellen
#  da sind und was beim Anlegen eines Test-Users WIRKLICH schiefgeht.
# =============================================================================

import os
import json
import base64
import uuid
import traceback
from pathlib import Path


# .env selbst einlesen (ohne python-dotenv, damit es überall läuft)
def load_env(path):
    if not path.exists():
        print("[FEHLER] .env nicht gefunden unter:", path)
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


load_env(Path(__file__).parent / ".env")

URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_SERVICE_KEY")

print("=" * 60)
print("SUPABASE_URL gesetzt:", bool(URL), "->", URL)
print("SUPABASE_SERVICE_KEY gesetzt:", bool(KEY), "| Länge:", len(KEY) if KEY else 0)


def key_typ(key):
    if not key:
        return "KEIN Key"
    if key.startswith("sb_secret_"):
        return "neues Format: SECRET  (= Admin, OK)"
    if key.startswith("sb_publishable_"):
        return "neues Format: PUBLISHABLE  (= NICHT Admin! falsch)"
    teile = key.split(".")
    if len(teile) == 3:  # sieht aus wie ein JWT
        try:
            pad = teile[1] + "=" * (-len(teile[1]) % 4)
            payload = json.loads(base64.urlsafe_b64decode(pad))
            return f"JWT mit role = {payload.get('role')!r}   (gebraucht wird 'service_role')"
        except Exception as e:
            return f"JWT, payload nicht lesbar: {e}"
    return "unbekanntes Format"


print("Key-Typ:", key_typ(KEY))
print("=" * 60)

try:
    import supabase as sb
    from supabase import create_client
    print("supabase-py Version:", getattr(sb, "__version__", "?"))

    client = create_client(URL, KEY)

    # --- Lese-Test: gibt es die Tabelle rooms? ---
    try:
        r = client.table("rooms").select("*").execute()
        print(f"[OK]  Tabelle 'rooms' lesbar – {len(r.data)} Raum/Räume gefunden.")
    except Exception as e:
        print("[FEHLER] 'rooms' lesen:", repr(e))

    # --- Auth-Test: Test-User anlegen (und gleich wieder löschen) ---
    test_email = f"diag_{uuid.uuid4().hex[:8]}@example.com"
    print(f"\nLege Test-User an: {test_email}")
    try:
        res = client.auth.admin.create_user({
            "email": test_email,
            "password": "test123456",
            "email_confirm": True,
        })
        print("[OK]  auth.admin.create_user funktioniert ->", res.user.id)
        try:
            client.auth.admin.delete_user(res.user.id)
            print("[OK]  Test-User wieder gelöscht.")
        except Exception as e:
            print("[Hinweis] Test-User nicht gelöscht:", repr(e))
    except Exception:
        print("[FEHLER] auth.admin.create_user – ECHTER Fehler:")
        traceback.print_exc()
except Exception:
    print("[FEHLER] Verbindung/Import:")
    traceback.print_exc()

print("=" * 60)
