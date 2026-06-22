# Schritt 2 – Backend (Flask-Server) starten

Der Flask-Server ist **schon fertig programmiert**. Du musst ihn nur noch
einrichten und starten.

> Alle Befehle führst du im Ordner `backend` aus.

## 2.1 Python-Umgebung vorbereiten

Öffne ein Terminal und gehe in den Backend-Ordner:

```bash
cd backend
```

Erstelle eine virtuelle Umgebung (ein eigener Python-Bereich nur für dieses Projekt):

```bash
python3 -m venv .venv
```

Aktiviere sie:

```bash
# macOS / Linux:
source .venv/bin/activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

Wenn es geklappt hat, steht jetzt `(.venv)` vorne in der Zeile.

## 2.2 Pakete installieren

```bash
pip install -r requirements.txt
```

## 2.3 Schlüssel eintragen (.env Datei)

1. Kopiere die Vorlage:

   ```bash
   # macOS / Linux:
   cp .env.example .env

   # Windows (PowerShell):
   copy .env.example .env
   ```

2. Öffne die neue Datei `.env` und trage deine beiden Werte aus
   [Schritt 1.3](1_supabase.md) ein:

   ```env
   SUPABASE_URL=https://deinprojekt.supabase.co
   SUPABASE_SERVICE_KEY=eyJhbGciOi....(dein service_role key)
   ```

## 2.4 Server starten

```bash
python app.py
```

Du solltest etwa so etwas sehen:

```
 * Running on http://0.0.0.0:5001
```

## 2.5 Funktioniert es?

Öffne im Browser: [http://localhost:5001](http://localhost:5001)

Du solltest sehen:

```json
{ "status": "ok", "message": "ChatApp Backend läuft 🎉" }
```

✅ Glückwunsch, dein Backend läuft! Lass das Terminal **offen**
(der Server muss laufen, solange du die App benutzt).

➡️ Weiter mit **[Schritt 3 – Backend testen](3_backend_testen.md)**
