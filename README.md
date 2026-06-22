# ChatApp – Expo + Flask + Supabase

Ein einfaches Lern-Projekt: eine **Chat-App** (Expo / React Native), die über
einen **Flask-Server** mit einer **Supabase-Datenbank** spricht.

> 🎯 **Deine Aufgabe:** Backend und Datenbank sind fertig. Du musst nur die
> **Verbindung vom Frontend zum Backend** herstellen. Die Stellen sind im Code
> mit `TODO` markiert. Die Anleitung dazu ist
> [`docs/4_frontend_verbinden.md`](docs/4_frontend_verbinden.md).

---

## Wie hängt alles zusammen?

```
┌─────────────────┐   fetch / HTTP   ┌──────────────────┐   supabase-py   ┌──────────────┐
│   Expo-App      │ ───────────────► │   Flask-Server   │ ──────────────► │   Supabase   │
│  (Frontend)     │ ◄─────────────── │   (Backend)      │ ◄────────────── │  (Datenbank) │
│  frontend/      │     JSON         │   backend/       │                 │  schema.sql  │
└─────────────────┘                  └──────────────────┘                 └──────────────┘
   TODO: du!                            ✅ fertig                            ✅ fertig
```

- Die **App** zeigt Räume und Nachrichten und schickt Anfragen an das Backend.
- Das **Backend** ist die einzige Stelle, die mit der Datenbank redet
  (mit dem geheimen Admin-Schlüssel).
- **Supabase** speichert Benutzer, Räume und Nachrichten.

---

## Ordnerstruktur

```
.
├── README.md               ← du bist hier
├── schema.sql              ← Datenbank-Tabellen für Supabase
│
├── backend/                ← Flask-Server (FERTIG)
│   ├── app.py              ← Start des Servers
│   ├── routes.py           ← ALLE Routen (register, login, rooms, messages …)
│   ├── supabase_client.py  ← Supabase-Verbindung + Benutzerverwaltung
│   ├── requirements.txt    ← Python-Pakete
│   ├── .env.example        ← Vorlage für die geheimen Schlüssel
│   └── tests/
│       └── test_api.py     ← Beispiel-Tests: funktioniert das Backend?
│
├── frontend/               ← Expo-App (expo-router, Verbindung = TODO)
│   ├── config.ts           ← Server-Adresse (API_URL)
│   ├── session.ts          ← merkt sich den Login-Token
│   └── app/                ← ⭐ HIER sind die TODOs (Verbindung zum Backend)
│       ├── _layout.tsx     ← Navigation (Stack)
│       ├── index.tsx       ← Login / Registrieren   (2 TODOs)
│       ├── rooms.tsx       ← Liste der Räume         (1 TODO)
│       └── chat.tsx        ← Nachrichten lesen & schreiben (2 TODOs)
│
├── frontend_solution/      ← fertige Lösung (alle TODOs ausgefüllt, läuft sofort)
│
└── docs/                   ← Schritt-für-Schritt-Anleitung
    ├── 1_supabase.md
    ├── 2_backend.md
    ├── 3_backend_testen.md
    └── 4_frontend_verbinden.md   ← ⭐ deine Hauptaufgabe
```

---

## Reihenfolge (so gehst du vor)

| Schritt | Anleitung | Was passiert |
|--------:|-----------|--------------|
| 1 | [docs/1_supabase.md](docs/1_supabase.md) | Supabase-Projekt + Tabellen anlegen, Schlüssel kopieren |
| 2 | [docs/2_backend.md](docs/2_backend.md) | Flask-Server einrichten und starten |
| 3 | [docs/3_backend_testen.md](docs/3_backend_testen.md) | Testen, ob das Backend funktioniert |
| 4 | [docs/4_frontend_verbinden.md](docs/4_frontend_verbinden.md) | ⭐ Die TODOs ausfüllen → App läuft! |

---

## Schnellstart (Kurzfassung)

**Backend:**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env             # dann SUPABASE_URL und SUPABASE_SERVICE_KEY eintragen
python app.py
```

**Frontend:**

```bash
cd frontend
npm install
npx expo start                   # dann "w" für Browser, oder QR-Code mit Expo Go scannen
```

---

## Voraussetzungen

- [Python 3](https://www.python.org/) (für das Backend)
- [Node.js](https://nodejs.org/) (für die Expo-App)
- Ein kostenloser [Supabase](https://supabase.com)-Account
- Optional fürs Handy: die App **Expo Go** (App Store / Google Play)
