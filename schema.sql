-- =============================================================================
--  ChatApp – Supabase Datenbank-Schema
-- =============================================================================
--  Dieses Skript legt alle Tabellen an, die die ChatApp braucht.
--
--  SO WIRD ES AUSGEFÜHRT:
--    1. Supabase-Projekt öffnen  ->  https://supabase.com
--    2. Links im Menü auf  "SQL Editor"  klicken
--    3. "New query"  ->  diesen kompletten Inhalt hineinkopieren
--    4. Auf  "Run"  klicken
--
--  Danach existieren die Tabellen:  profiles, rooms, messages
--
--  HINWEIS zu auth.users:
--    Supabase hat bereits eine eingebaute Tabelle  auth.users  für die
--    Anmeldung (E-Mail + Passwort).  Die legen wir NICHT selbst an.
--    Unsere Tabelle  profiles  zeigt nur mit einem Verweis (Foreign Key)
--    auf diese eingebaute Benutzer-Tabelle.
-- =============================================================================


-- -----------------------------------------------------------------------------
--  Aufräumen (nur nützlich, wenn man das Skript erneut laufen lässt)
--  Reihenfolge wichtig: erst die Tabellen löschen, die auf andere zeigen.
-- -----------------------------------------------------------------------------
drop table if exists public.messages cascade;
drop table if exists public.rooms cascade;
drop table if exists public.profiles cascade;


-- -----------------------------------------------------------------------------
--  1) profiles  –  Benutzerprofile
-- -----------------------------------------------------------------------------
--  Jede Zeile gehört zu genau einem Login aus  auth.users.
--  Hier speichern wir Zusatzinfos wie den Benutzernamen.
-- -----------------------------------------------------------------------------
create table public.profiles (
    -- id ist gleichzeitig der Verweis auf den Supabase-Login.
    id            uuid        primary key references auth.users (id) on delete cascade,
    username      text        unique not null,
    display_name  text,
    avatar_url    text,
    created_at    timestamptz not null default now()
);


-- -----------------------------------------------------------------------------
--  2) rooms  –  Chaträume
-- -----------------------------------------------------------------------------
--  Ein Raum ist z. B. "Allgemein", "Hausübungen", "Smalltalk".
-- -----------------------------------------------------------------------------
create table public.rooms (
    id          uuid        primary key default gen_random_uuid(),
    name        text        not null,
    created_by  uuid        references public.profiles (id) on delete set null,
    created_at  timestamptz not null default now()
);


-- -----------------------------------------------------------------------------
--  3) messages  –  Nachrichten
-- -----------------------------------------------------------------------------
--  Jede Nachricht gehört zu einem Raum (room_id) und zu einem Benutzer (user_id).
-- -----------------------------------------------------------------------------
create table public.messages (
    id          uuid        primary key default gen_random_uuid(),
    room_id     uuid        not null references public.rooms (id)    on delete cascade,
    user_id     uuid        not null references public.profiles (id) on delete cascade,
    content     text        not null check (char_length(content) > 0),
    created_at  timestamptz not null default now()
);


-- -----------------------------------------------------------------------------
--  Indizes  –  machen das Laden der Nachrichten eines Raums schneller
-- -----------------------------------------------------------------------------
create index idx_messages_room_id    on public.messages (room_id);
create index idx_messages_created_at on public.messages (created_at);


-- -----------------------------------------------------------------------------
--  Beispiel-Daten  –  damit beim ersten Start schon etwas zu sehen ist
-- -----------------------------------------------------------------------------
insert into public.rooms (name) values
    ('Allgemein'),
    ('Hausübungen'),
    ('Smalltalk');


-- =============================================================================
--  Row Level Security (RLS)  –  Sicherheits-Regeln
-- =============================================================================
--  WICHTIG ZUM VERSTEHEN:
--  Unser Flask-Server verbindet sich mit dem "service_role"-Schlüssel.
--  Dieser Schlüssel ist ein Admin-Schlüssel und DARF ALLES – er umgeht RLS.
--
--  Trotzdem schalten wir RLS ein und definieren Lese-Regeln. Das ist
--  "Sicherheit in der Tiefe": Sollte sich jemals jemand mit dem
--  öffentlichen "anon"-Schlüssel verbinden, kann er nur lesen, nicht
--  alles verändern.
--
--  Für den Unterricht reicht es zu wissen:
--    - RLS = "Wer darf welche Zeilen sehen/ändern?"
--    - Der Flask-Server arbeitet als Admin und ist von diesen Regeln nicht betroffen.
-- =============================================================================

alter table public.profiles enable row level security;
alter table public.rooms    enable row level security;
alter table public.messages enable row level security;

-- Jeder darf Profile, Räume und Nachrichten LESEN.
create policy "Profile sind öffentlich lesbar"
    on public.profiles for select using (true);

create policy "Räume sind öffentlich lesbar"
    on public.rooms for select using (true);

create policy "Nachrichten sind öffentlich lesbar"
    on public.messages for select using (true);

-- Schreiben (insert/update/delete) erledigt nur der Flask-Server (service_role),
-- der RLS sowieso umgeht. Deshalb brauchen wir hier keine weiteren Policies.

-- =============================================================================
--  Fertig!  In Supabase unter  "Table Editor"  kannst du die Tabellen ansehen.
-- =============================================================================
