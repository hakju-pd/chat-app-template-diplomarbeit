# Schritt 4 – Frontend mit dem Backend verbinden ⭐

Das ist **deine Hauptaufgabe**. Die Expo-App ist fertig gebaut (alle Screens,
Knöpfe und die Navigation funktionieren bereits). Was noch fehlt: die App muss
mit dem Flask-Server **reden**. Diese Stellen sind im Code mit `// TODO`
markiert – direkt dort, wo sie gebraucht werden.

> Die App nutzt **expo-router**: Jede Datei im Ordner `app/` ist automatisch
> ein Bildschirm. `app/index.tsx` = Start (Login), `app/rooms.tsx` = Räume,
> `app/chat.tsx` = Chat.

## Wo sind die TODOs?

| # | Datei | Funktion | Was passiert |
|---|-------|----------|--------------|
| 1 | `frontend/config.ts` | — | Server-Adresse eintragen |
| 3 | `frontend/app/index.tsx` | `handleRegister` | Registrieren |
| 4 | `frontend/app/index.tsx` | `handleLogin` | Einloggen |
| 5 | `frontend/app/rooms.tsx` | `ladeRaeume` | Räume laden |
| 6 | `frontend/app/chat.tsx` | `laden` | Nachrichten laden |
| 7 | `frontend/app/chat.tsx` | `senden` | Nachricht senden |

Wir gehen sie der Reihe nach durch. Zu jedem Schritt gibt es die Erklärung
**und** die fertige Lösung zum Ersetzen des `TODO`-Blocks.

---

## Wie funktioniert die Verbindung überhaupt?

Das Frontend schickt eine **Anfrage (Request)** an den Flask-Server und bekommt
eine **Antwort (Response)** zurück – meistens als JSON. Dafür benutzen wir die
eingebaute Funktion **`fetch`**.

Grundgerüst einer Anfrage:

```ts
const response = await fetch(URL, {
  method: "POST",                                  // oder "GET"
  headers: { "Content-Type": "application/json" }, // wir senden JSON
  body: JSON.stringify({ ... }),                   // die Daten
});
const data = await response.json();                // Antwort als JSON lesen
```

- **GET** = etwas holen (z.B. Räume laden). Braucht keinen `body`.
- **POST** = etwas senden (z.B. Nachricht schreiben). Braucht einen `body`.

> 💡 `await` bedeutet „warte, bis die Antwort da ist". Deshalb steht vor den
> Funktionen das Wort `async`.

---

## Schritt 1 – Die Server-Adresse eintragen

Öffne `frontend/config.ts`:

```ts
export const API_URL = "http://localhost:5001";
```

- Im **Browser** (in Expo `w` drücken): `http://localhost:5001` passt.
- Am **Handy** mit **Expo Go**: `localhost` funktioniert NICHT! Trage die
  **IP-Adresse deines Computers** ein (zeigt Expo beim Start an, z.B.
  `exp://192.168.0.42:8081` → nimm den Teil davor):

  ```ts
  export const API_URL = "http://192.168.0.42:5001";
  ```

  > Computer und Handy müssen im **gleichen WLAN** sein.

---

## Schritt 3 – Registrieren (`app/index.tsx`)

Öffne `frontend/app/index.tsx`. Ersetze die Funktion `handleRegister` durch:

```ts
async function handleRegister() {
  try {
    const response = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, username }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Registrierung fehlgeschlagen");
    }
    Alert.alert("Super!", "Registrierung erfolgreich. Du kannst dich jetzt einloggen.");
  } catch (e: any) {
    Alert.alert("Fehler", e.message);
  }
}
```

---

## Schritt 4 – Einloggen (`app/index.tsx`)

Beim Login bekommen wir einen `access_token`. Den speichern wir mit
`setToken(...)` (aus `session.ts`) und wechseln zur Raum-Liste.

Ersetze die Funktion `handleLogin` durch:

```ts
async function handleLogin() {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Login fehlgeschlagen");
    }
    setToken(data.access_token); // Token merken
    router.replace("/rooms");    // weiter zur Raum-Liste
  } catch (e: any) {
    Alert.alert("Fehler", e.message);
  }
}
```

---

## Schritt 5 – Räume laden (`app/rooms.tsx`)

Öffne `frontend/app/rooms.tsx`. Ersetze die Funktion `ladeRaeume`
(innerhalb von `useEffect`) durch:

```ts
async function ladeRaeume() {
  try {
    const response = await fetch(`${API_URL}/rooms`);
    const data = await response.json();
    setRooms(data);
  } catch (e: any) {
    Alert.alert("Fehler", e.message);
  }
}
```

---

## Schritt 6 – Nachrichten laden (`app/chat.tsx`)

Öffne `frontend/app/chat.tsx`. Ersetze die Funktion `laden` durch:

```ts
async function laden() {
  try {
    const response = await fetch(`${API_URL}/rooms/${roomId}/messages`);
    const data = await response.json();
    setMessages(data);
  } catch (e: any) {
    Alert.alert("Fehler", e.message);
  }
}
```

---

## Schritt 7 – Nachricht senden (`app/chat.tsx`)

Das ist eine **geschützte** Route. Wichtig: Wir schicken den Token
(mit `getToken()` aus `session.ts`) im `Authorization`-Header mit!

Ersetze die Funktion `senden` durch:

```ts
async function senden() {
  if (!text.trim()) return;
  try {
    const response = await fetch(`${API_URL}/rooms/${roomId}/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + getToken(), // <-- Login-Token mitschicken!
      },
      body: JSON.stringify({ content: text }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Nachricht konnte nicht gesendet werden");
    }
    setText("");
    laden(); // neu laden, damit die neue Nachricht erscheint
  } catch (e: any) {
    Alert.alert("Fehler", e.message);
  }
}
```

---

## Schritt 8 – App starten und ausprobieren

1. Stelle sicher, dass das **Backend läuft** (Terminal aus Schritt 2).
2. Neues Terminal, in den Frontend-Ordner gehen:

   ```bash
   cd frontend
   npm install      # nur beim ersten Mal nötig
   npx expo start
   ```

3. Jetzt entweder:
   - **`w`** drücken → App öffnet sich im Browser, oder
   - **Expo Go**-App am Handy öffnen und den QR-Code scannen.

4. Ablauf in der App:
   - **Registrieren** (E-Mail, Passwort, Benutzername → „Registrieren").
   - **Einloggen** (E-Mail + Passwort → „Einloggen").
   - Einen **Raum** antippen.
   - Eine **Nachricht** schreiben und „Senden".

🎉 **Geschafft!** Wenn deine Nachricht erscheint, ist die App komplett mit dem
Flask-Backend und Supabase verbunden.

---

## Es klappt nicht? – Hilfe

| Problem | Mögliche Ursache / Lösung |
|---------|---------------------------|
| Fenster „TODO ..." erscheint | An dieser Stelle ist der `// TODO`-Block noch nicht ersetzt. |
| „Network request failed" | Backend läuft nicht, oder am Handy `localhost` statt IP benutzt (Schritt 1). |
| Keine Räume sichtbar | Wurde `schema.sql` in Supabase ausgeführt? (Schritt 1) Und das TODO in `app/rooms.tsx` erledigt? |
| „Bitte zuerst einloggen" beim Senden | Erst einloggen – `handleLogin` muss `setToken(data.access_token)` aufrufen. |
| Computer + Handy finden sich nicht | Beide müssen im **gleichen WLAN** sein. |
