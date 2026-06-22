// ============================================================================
//  session.ts  –  merkt sich den Login-Token
// ============================================================================
//  Beim Login speichern wir den Token hier (setToken).
//  Beim Senden einer Nachricht lesen wir ihn wieder aus (getToken).
//  So können alle Screens auf den Token zugreifen.
// ============================================================================

let token: string | null = null;

export function setToken(neuerToken: string) {
  token = neuerToken;
}

export function getToken() {
  return token;
}
