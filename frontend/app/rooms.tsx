// ============================================================================
//  app/rooms.tsx  –  Liste aller Chaträume
// ============================================================================
//  Verbindungs-Stelle zum Backend (mit TODO markiert):
//    - ladeRaeume()  -> GET /rooms
//  Tippt man auf einen Raum, öffnet sich der Chat (router.push -> /chat).
//  Die fertige Lösung steht in  docs/4_frontend_verbinden.md
// ============================================================================

import { useEffect, useState } from "react";
import { View, Text, FlatList, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { useRouter } from "expo-router";
import { API_URL } from "../config";

export default function RoomsScreen() {
  const router = useRouter();
  const [rooms, setRooms] = useState<any[]>([]);

  // Beim ersten Anzeigen die Räume laden.
  useEffect(() => {
    async function ladeRaeume() {
      try {
        // ===== TODO (Schritt 5): Räume laden – mit dem Backend verbinden =====
        //  GET-Anfrage an  `${API_URL}/rooms`
        //  Das Ergebnis (eine Liste) mit  setRooms(...)  setzen.
        setRooms([]); // Platzhalter: bis du das TODO ausfüllst, bleibt die Liste leer
        // ===================================================================
      } catch (e: any) {
        Alert.alert("Fehler", e.message);
      }
    }
    ladeRaeume();
  }, []);

  // Raum öffnen: room.id und room.name an den Chat-Bildschirm weitergeben.
  function oeffneRaum(room: any) {
    router.push({
      pathname: "/chat",
      params: { roomId: room.id, roomName: room.name },
    });
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={rooms}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.room} onPress={() => oeffneRaum(item)}>
            <Text style={styles.roomName}># {item.name}</Text>
          </TouchableOpacity>
        )}
        ListEmptyComponent={
          <Text style={styles.hint}>
            Noch keine Räume geladen.
            {"\n"}(TODO in app/rooms.tsx erledigt? Siehe docs/4_frontend_verbinden.md)
          </Text>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  room: {
    padding: 16,
    borderRadius: 8,
    backgroundColor: "#f0f0f0",
    marginBottom: 10,
  },
  roomName: { fontSize: 18 },
  hint: { color: "#888", textAlign: "center", marginTop: 40 },
});
