# Schritt 3 – Backend testen

Bevor wir das Frontend verbinden, prüfen wir: **Funktioniert das Backend
wirklich?** Dafür gibt es zwei Möglichkeiten.

---

## Möglichkeit A: Automatische Tests (empfohlen)

Im Ordner `backend/tests` liegt die Datei `test_api.py` mit fertigen Tests.
Sie registrieren einen Benutzer, loggen ein, laden Räume und senden eine
Nachricht – und prüfen, ob alles richtig antwortet.

So führst du sie aus:

1. **Terminal 1:** Server läuft bereits (`python app.py` aus Schritt 2).
2. **Terminal 2** öffnen, in den Backend-Ordner gehen und die Umgebung aktivieren:

   ```bash
   cd backend
   source .venv/bin/activate     # Windows: .venv\Scripts\Activate.ps1
   ```

3. Tests starten:

   ```bash
   pytest -v
   ```

✅ Wenn alles grün ist (`PASSED`), funktioniert dein Backend + Supabase!

Beispiel-Ausgabe:

```
tests/test_api.py::test_server_laeuft PASSED
tests/test_api.py::test_register PASSED
tests/test_api.py::test_login PASSED
tests/test_api.py::test_falsches_passwort_wird_abgelehnt PASSED
tests/test_api.py::test_rooms_laden PASSED
tests/test_api.py::test_nachricht_ohne_login_ist_verboten PASSED
tests/test_api.py::test_nachricht_mit_login_klappt PASSED
tests/test_api.py::test_nachrichten_laden PASSED
```

---

## Möglichkeit B: Von Hand mit `curl` ausprobieren

Du kannst die Routen auch einzeln im Terminal ausprobieren.

**Läuft der Server?**

```bash
curl http://localhost:5001/
```

**Benutzer registrieren:**

```bash
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{"email":"max@example.com","password":"geheim123","username":"max"}'
```

**Einloggen** (gibt dir einen `access_token` zurück):

```bash
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"email":"max@example.com","password":"geheim123"}'
```

**Räume laden:**

```bash
curl http://localhost:5001/rooms
```

**Nachricht senden** (Token aus dem Login einsetzen, ebenso eine `room_id`
aus der Raum-Liste):

```bash
curl -X POST http://localhost:5001/rooms/DEINE-ROOM-ID/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer DEIN-ACCESS-TOKEN" \
  -d '{"content":"Hallo Welt!"}'
```

> 💡 Tipp: Statt `curl` kannst du auch ein Tool wie **Thunder Client**
> (VS Code), **Postman** oder **Insomnia** verwenden.

---

## Welche Routen gibt es?

| Methode | Route | Geschützt? | Was macht sie? |
|---------|-------|-----------|----------------|
| GET  | `/` | nein | Test: läuft der Server? |
| POST | `/register` | nein | Neuen Benutzer anlegen |
| POST | `/login` | nein | Einloggen, gibt `access_token` |
| GET  | `/rooms` | nein | Alle Räume laden |
| POST | `/rooms` | **ja** | Neuen Raum anlegen |
| GET  | `/rooms/<id>/messages` | nein | Nachrichten eines Raums |
| POST | `/rooms/<id>/messages` | **ja** | Nachricht senden |
| GET  | `/profiles/<id>` | nein | Ein Profil laden |

„Geschützt" heißt: man muss eingeloggt sein und den `access_token` im Header
`Authorization: Bearer <token>` mitschicken.

➡️ Weiter mit **[Schritt 4 – Frontend verbinden](4_frontend_verbinden.md)**
