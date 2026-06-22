// ============================================================================
//  app/chat.tsx  –  Nachrichten in einem Raum lesen und schreiben
// ============================================================================
//  roomId und roomName kommen über die Navigation (useLocalSearchParams).
//  Zwei Verbindungs-Stellen zum Backend (mit TODO markiert):
//    - laden()   -> GET  /rooms/<id>/messages
//    - senden()  -> POST /rooms/<id>/messages   (geschützt: braucht den Token!)
//  Die fertige Lösung steht in  docs/4_frontend_verbinden.md
// ============================================================================

import { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  Button,
  FlatList,
  StyleSheet,
  Alert,
} from "react-native";
import { Stack, useLocalSearchParams } from "expo-router";
import { API_URL } from "../config";
import { getToken } from "../session";

export default function ChatScreen() {
  // Werte, die uns die Raum-Liste mitgegeben hat:
  const { roomId, roomName } = useLocalSearchParams<{
    roomId: string;
    roomName: string;
  }>();

  const [messages, setMessages] = useState<any[]>([]);
  const [text, setText] = useState("");

  // Nachrichten (neu) laden.
  async function laden() {
    try {
      // ===== TODO (Schritt 6): Nachrichten laden – mit dem Backend verbinden =====
      //  GET-Anfrage an  `${API_URL}/rooms/${roomId}/messages`
      //  Das Ergebnis (eine Liste) mit  setMessages(...)  setzen.
      setMessages([]); // Platzhalter, bis du das TODO ausfüllst
      // =========================================================================
    } catch (e: any) {
      Alert.alert("Fehler", e.message);
    }
  }

  // Beim Öffnen des Raums laden.
  useEffect(() => {
    laden();
  }, []);

  // Nachricht senden.
  async function senden() {
    if (!text.trim()) return;
    try {
      // ===== TODO (Schritt 7): Nachricht senden – geschützte Verbindung =====
      //  POST an  `${API_URL}/rooms/${roomId}/messages`
      //  WICHTIG: Der Token muss mit im Header:
      //      Authorization: "Bearer " + getToken()
      //  Body (JSON):  { content: text }
      //  Danach:  setText("")  und  laden()  (damit die neue Nachricht erscheint)
      Alert.alert("TODO", "sendMessage ist noch nicht verbunden.\nSiehe docs/4_frontend_verbinden.md");
      // =====================================================================
    } catch (e: any) {
      Alert.alert("Fehler", e.message);
    }
  }

  return (
    <View style={styles.container}>
      {/* Setzt den Titel der Kopfzeile auf den Raum-Namen */}
      <Stack.Screen options={{ title: "# " + roomName }} />

      <FlatList
        style={styles.list}
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.message}>
            <Text style={styles.author}>
              {item.profiles?.username ?? "Unbekannt"}
            </Text>
            <Text>{item.content}</Text>
          </View>
        )}
        ListEmptyComponent={
          <Text style={styles.hint}>Noch keine Nachrichten. Schreib die erste!</Text>
        }
      />

      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder="Nachricht..."
          value={text}
          onChangeText={setText}
        />
        <Button title="Senden" onPress={senden} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  list: { flex: 1 },
  message: {
    padding: 10,
    borderRadius: 8,
    backgroundColor: "#f0f0f0",
    marginBottom: 8,
  },
  author: { fontWeight: "bold", marginBottom: 2 },
  hint: { color: "#888", textAlign: "center", marginTop: 40 },
  inputRow: { flexDirection: "row", alignItems: "center", gap: 8, marginTop: 8 },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
});
