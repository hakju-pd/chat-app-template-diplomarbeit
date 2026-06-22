# Schritt 1 – Supabase einrichten

Supabase ist unsere Datenbank in der Cloud. Hier legen wir das Projekt an
und erstellen die Tabellen.

## 1.1 Projekt erstellen

1. Gehe auf [https://supabase.com](https://supabase.com) und logge dich ein
   (kostenloser Account).
2. Klicke auf **New project**.
3. Gib einen Namen ein (z.B. `chatapp`) und ein Datenbank-Passwort
   (irgendeins, du brauchst es später nicht zwingend – aber merke es dir).
4. Warte ~2 Minuten, bis das Projekt fertig erstellt ist.

## 1.2 Tabellen anlegen

1. Links im Menü auf **SQL Editor** klicken.
2. Auf **New query** klicken.
3. Öffne die Datei [`schema.sql`](../schema.sql) aus diesem Projekt,
   kopiere den **kompletten Inhalt** und füge ihn in den SQL-Editor ein.
4. Auf **Run** (unten rechts) klicken.

✅ Wenn alles geklappt hat, findest du links unter **Table Editor** die
drei Tabellen: `profiles`, `rooms`, `messages`. Im Raum-Tabelle stehen schon
drei Beispiel-Räume.

## 1.3 Die Schlüssel kopieren

Damit unser Flask-Server mit Supabase reden kann, brauchen wir zwei Werte:

1. Links im Menü auf **Project Settings** (Zahnrad) → **API**.
2. Kopiere dir diese beiden Werte:

| Wert | Wo? | Wofür? |
|------|-----|--------|
| **Project URL** | Abschnitt "Project URL" | Adresse deiner Datenbank |
| **service_role key** | Abschnitt "Project API keys" → `service_role` (geheim) | Admin-Schlüssel für den Server |

> ⚠️ **Wichtig:** Wir brauchen den **`service_role`**-Schlüssel, NICHT den
> `anon`-Schlüssel. Der `service_role`-Schlüssel ist geheim und darf nur im
> Backend benutzt werden – niemals im Frontend / in der App!

➡️ Weiter mit **[Schritt 2 – Backend starten](2_backend.md)**
