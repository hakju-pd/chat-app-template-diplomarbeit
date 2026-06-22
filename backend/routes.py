# =============================================================================
#  routes.py
# =============================================================================
#  HIER liegen ALLE Routen für unsere Tabellen (profiles, rooms, messages)
#  und die Benutzerverwaltung (register, login).
#
#  Aufbau jeder Route:
#    1. Daten aus der Anfrage lesen
#    2. (Falls nötig) prüfen, ob jemand eingeloggt ist  -> einfaches if
#    3. Mit Supabase reden
#    4. Antwort als JSON zurückgeben
# =============================================================================

from flask import Blueprint, request, jsonify
from supabase_client import (
    supabase,
    create_user,
    login_with_password,
    get_user_id_from_token,
)

# Ein "Blueprint" ist eine Sammlung von Routen.
# In app.py wird dieser Blueprint dann eingebunden.
api = Blueprint("api", __name__)


# -----------------------------------------------------------------------------
#  Hilfsfunktion: Wer ist gerade eingeloggt?
# -----------------------------------------------------------------------------
#  Liest den Token aus dem Header  "Authorization: Bearer <token>"
#  und gibt die user_id zurück (oder None, wenn niemand eingeloggt ist).
#
#  WICHTIG: Das ist KEIN Decorator (kein @-Schutz mit "wraps").
#  Wir schützen Routen ganz einfach mit einem  if  -> siehe unten.
# -----------------------------------------------------------------------------
def aktueller_user(req):
    auth_header = req.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.replace("Bearer ", "")
    return get_user_id_from_token(token)


# =============================================================================
#  BENUTZERVERWALTUNG
# =============================================================================

@api.post("/register")
def register():
    """Neuen Benutzer anlegen.  Body: { email, password, username }"""
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")
    

    if not email or not password or not username:
        return jsonify({"error": "email, password und username sind erforderlich"}), 400

    # 1. Login (E-Mail + Passwort) in Supabase anlegen
    try:
        user = create_user(email, password)
    except Exception as e:
        # echte Fehlermeldung zeigen (z.B. "email already registered")
        return jsonify({"error": f"Registrierung fehlgeschlagen: {e}"}), 400

    # 2. Passendes Profil anlegen (gleiche id wie der Login)
    try:
        supabase.table("profiles").insert({
            "id": user.id,
            "username": username,
        }).execute()
    except Exception as e:
        return jsonify({"error": f"Profil konnte nicht angelegt werden: {e}"}), 400

    return jsonify({"message": "Registrierung erfolgreich", "user_id": user.id}), 201


@api.post("/login")
def login():
    """Einloggen.  Body: { email, password }  ->  gibt access_token zurück."""
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email und password sind erforderlich"}), 400

    session = login_with_password(email, password)
    if session is None:
        return jsonify({"error": "E-Mail oder Passwort ist falsch"}), 401

    # Enthält: { "access_token": "...", "user_id": "..." }
    return jsonify(session)


# =============================================================================
#  RÄUME (Tabelle: rooms)
# =============================================================================

@api.get("/rooms")
def get_rooms():
    """Alle Räume laden (jeder darf das)."""
    result = supabase.table("rooms").select("*").order("created_at").execute()
    return jsonify(result.data)


@api.post("/rooms")
def create_room():
    """Neuen Raum anlegen.  Nur für eingeloggte Benutzer!"""
    # ---- Schutz mit einfachem if (kein Decorator!) ----
    user_id = aktueller_user(request)
    if user_id is None:
        return jsonify({"error": "Bitte zuerst einloggen"}), 401
    # ---------------------------------------------------

    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name ist erforderlich"}), 400

    result = supabase.table("rooms").insert({
        "name": name,
        "created_by": user_id,
    }).execute()
    return jsonify(result.data[0]), 201


# =============================================================================
#  NACHRICHTEN (Tabelle: messages)
# =============================================================================

@api.get("/rooms/<room_id>/messages")
def get_messages(room_id):
    """Alle Nachrichten eines Raums laden (mit Benutzername)."""
    result = (
        supabase.table("messages")
        # profiles(username) holt zusätzlich den Namen des Absenders dazu
        .select("id, content, created_at, user_id, profiles(username)")
        .eq("room_id", room_id)
        .order("created_at")
        .execute()
    )
    return jsonify(result.data)


@api.post("/rooms/<room_id>/messages")
def create_message(room_id):
    """Nachricht in einem Raum schreiben.  Nur für eingeloggte Benutzer!"""
    # ---- Schutz mit einfachem if (kein Decorator!) ----
    user_id = aktueller_user(request)
    if user_id is None:
        return jsonify({"error": "Bitte zuerst einloggen"}), 401
    # ---------------------------------------------------

    data = request.get_json() or {}
    content = data.get("content")
    if not content:
        return jsonify({"error": "content ist erforderlich"}), 400

    result = supabase.table("messages").insert({
        "room_id": room_id,
        "user_id": user_id,
        "content": content,
    }).execute()
    return jsonify(result.data[0]), 201


# =============================================================================
#  PROFILE (Tabelle: profiles)
# =============================================================================

@api.get("/profiles/<user_id>")
def get_profile(user_id):
    """Ein einzelnes Profil laden."""
    result = supabase.table("profiles").select("*").eq("id", user_id).execute()
    if not result.data:
        return jsonify({"error": "Profil nicht gefunden"}), 404
    return jsonify(result.data[0])
