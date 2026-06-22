// ============================================================================
//  app/index.tsx  –  Startbildschirm: Einloggen oder Registrieren
// ============================================================================
//  Zwei Verbindungs-Stellen zum Backend (mit TODO markiert):
//    - handleRegister()  -> POST /register
//    - handleLogin()     -> POST /login
//  Die fertige Lösung steht in  docs/4_frontend_verbinden.md
// ============================================================================

import { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { useRouter } from "expo-router";
import { API_URL } from "../config";
import { setToken } from "../session";

export default function LoginScreen() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");

  async function handleRegister() {
    try {
      // ===== TODO (Schritt 3): Registrieren – mit dem Backend verbinden =====
      //  Sende eine POST-Anfrage an  `${API_URL}/register`
      //  mit dem Body (JSON):  { email, password, username }
      //  Bei Erfolg: Alert "Registrierung erfolgreich" anzeigen.
      Alert.alert("TODO", "register ist noch nicht verbunden.\nSiehe docs/4_frontend_verbinden.md");
      // =====================================================================
    } catch (e: any) {
      Alert.alert("Fehler", e.message);
    }
  }

  async function handleLogin() {
    try {
      // ===== TODO (Schritt 4): Login – mit dem Backend verbinden =====
      //  1. POST an  `${API_URL}/login`  mit Body (JSON):  { email, password }
      //  2. access_token holen und mit  setToken(...)  speichern
      //  3. router.replace("/rooms")  -> weiter zur Raum-Liste
      Alert.alert("TODO", "login ist noch nicht verbunden.\nSiehe docs/4_frontend_verbinden.md");
      // ==============================================================
    } catch (e: any) {
      Alert.alert("Fehler", e.message);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>ChatApp 💬</Text>

      <TextInput
        style={styles.input}
        placeholder="E-Mail"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Passwort"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <TextInput
        style={styles.input}
        placeholder="Benutzername (nur für Registrierung)"
        autoCapitalize="none"
        value={username}
        onChangeText={setUsername}
      />

      <Button title="Einloggen" onPress={handleLogin} />
      <View style={{ height: 10 }} />
      <Button title="Registrieren" onPress={handleRegister} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 20, gap: 10 },
  title: { fontSize: 32, fontWeight: "bold", textAlign: "center", marginBottom: 20 },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
});
