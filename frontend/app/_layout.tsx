// ============================================================================
//  app/_layout.tsx  –  Die Navigation (expo-router)
// ============================================================================
//  Bei expo-router ist jede Datei im Ordner "app" automatisch ein Bildschirm:
//    app/index.tsx  ->  "/"        (Login)
//    app/rooms.tsx  ->  "/rooms"   (Raum-Liste)
//    app/chat.tsx   ->  "/chat"    (Chat in einem Raum)
//
//  Der Stack sorgt für die Kopfzeile oben und den "Zurück"-Pfeil.
// ============================================================================

import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";

export default function RootLayout() {
  return (
    <>
      <Stack>
        <Stack.Screen name="index" options={{ title: "ChatApp 💬" }} />
        <Stack.Screen name="rooms" options={{ title: "Räume" }} />
        <Stack.Screen name="chat" options={{ title: "Chat" }} />
      </Stack>
      <StatusBar style="auto" />
    </>
  );
}
