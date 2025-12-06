import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from scraper_lib import scrape_therapists

# --- Konfiguration & Konstanten ---
# Diese Dictionaries mappen die lesbaren Namen (die der Nutzer sieht)
# auf die internen IDs, die therapie.de für die Suche verwendet.

# Rate Limiting & Performance
COOLDOWN_SECONDS = 15  # Wartezeit zwischen Suchanfragen
DELAY_PENALTY_INCREMENT = 0.5  # Erhöhung der Wartezeit pro Suche in der Sitzung
DEFAULT_ZIP_CODE = "12345"  # Standard-PLZ für Eingabefeld

VERFAHREN_OPTIONS = {
    "Alle": "",
    "Verhaltenstherapie": "2",
    "Tiefenpsychologisches Verfahren": "1",
    "Psychoanalyse": "14",
    "Systemische Therapie": "3",
    "Gesprächstherapie": "5",
    "Gestalttherapie": "4",
    "EMDR": "36",
    "Traumatherapie": "30",
}

ABRECHNUNG_OPTIONS = {
    "Egal": "",
    "GKV: Kassenzulassung": "1",
    "GKV: Kostenerstattungsverfahren": "6",
    "Private Krankenversicherung": "2",
    "Selbstzahler": "3",
}

ANGEBOT_OPTIONS = {
    "Egal": "",
    "Einzeltherapie": "1",
    "Gruppentherapie": "3",
    "Paartherapie": "5",
    "Kinder & Jugendliche": "4",
}

SCHWERPUNKT_OPTIONS = {
    "Egal": "",
    "Depression": "10",
    "Angst - Phobie": "2",
    "Stress - Burnout - Mobbing": "18",
    "Trauma - Gewalt - Missbrauch": "13",
    "ADHS": "30",
    "Essstörung": "3",
    "Persönlichkeitsstörung": "4",
    "Psychosomatik": "9",
    "Schmerzen": "20",
}

GESCHLECHT_OPTIONS = {
    "Egal": "",
    "Weiblich": "1",
    "Männlich": "2",
}

WARTEZEIT_OPTIONS = {
    "Egal": "1", # Standardwert, wenn keine Auswahl getroffen wird
    "Freie Plätze / Kurzfristig": "7",
    "Wartezeit bis 3 Monate": "2",
    "Wartezeit 3 bis 6 Monate": "3",
    "Wartezeit 6 bis 12 Monate": "4",
    "Wartezeit > 1 Jahr": "5",
    "Wartezeit unbekannt": "6",
}

UMKREIS_OPTIONS = {
    "Kein Umkreis (nur genaue PLZ)": "0",
    "5 km": "5",
    "10 km": "10",
    "20 km": "20",
    "50 km": "50",
    "100 km": "100",
}

# E-Mail-Vorlagen
EMAIL_TEMPLATE_ERSTGESPRAECH = """Sehr geehrte/r Frau/Herr [Name des Therapeuten],

ich bin auf der Suche nach einem Therapieplatz und habe Ihr Profil auf therapie.de gefunden. Ich leide unter [kurze Beschreibung des Problems, z.B. Angstzuständen / Depressionen] und würde gerne ein Erstgespräch mit Ihnen vereinbaren, um zu prüfen, ob eine Therapie bei Ihnen für mich in Frage kommt.

Ich bin [Versicherungsstatus, z.B. gesetzlich / privat] versichert.

Über eine Rückmeldung freue ich mich sehr.

Mit freundlichen Grüßen,

[Dein Name]
[Deine Telefonnummer]"""

EMAIL_TEMPLATE_WARTELISTE = """Sehr geehrte/r Frau/Herr [Name des Therapeuten],

ich bin auf der Suche nach einem Therapieplatz und habe Ihr Profil auf therapie.de gefunden. Mir ist bewusst, dass es oft Wartezeiten gibt. Ich würde mich dennoch gerne für einen Therapieplatz vormerken lassen und mich ggf. auf Ihre Warteliste setzen lassen.

Ich leide unter [kurze Beschreibung des Problems, z.B. Angstzuständen / Depressionen] und bin [Versicherungsstatus, z.B. gesetzlich / privat] versichert.

Über eine Rückmeldung freue ich mich sehr.

Mit freundlichen Grüßen,

[Dein Name]
[Deine Telefonnummer]"""

EMAIL_TEMPLATE_KOSTENERSTATTUNG = """Sehr geehrte/r Frau/Herr [Name des Therapeuten],

ich bin auf der dringenden Suche nach einem Therapieplatz und habe Ihr Profil auf therapie.de gefunden. Da ich innerhalb einer angemessenen Frist keinen kassenärztlich zugelassenen Therapieplatz finden konnte, prüfe ich derzeit die Möglichkeit eines Kostenerstattungsverfahrens bei meiner Krankenkasse.

Ich leide unter [kurze Beschreibung des Problems, z.B. Angstzuständen / Depressionen] und würde gerne ein Erstgespräch mit Ihnen vereinbaren, um zu klären, ob Sie mich im Rahmen eines Kostenerstattungsverfahrens behandeln würden.

Ich bin [Versicherungsstatus, z.B. gesetzlich / privat] versichert.

Über eine Rückmeldung freue ich mich sehr.

Mit freundlichen Grüßen,

[Dein Name]
[Deine Telefonnummer]"""

# --- Session State Initialisierung ---
# Wir merken uns Dinge über die Session hinweg (z.B. wann zuletzt gesucht wurde).
if 'last_search_time' not in st.session_state:
    st.session_state.last_search_time = None
if 'delay_penalty' not in st.session_state:
    st.session_state.delay_penalty = 0.0
if 'knows_alternatives' not in st.session_state:
    st.session_state.knows_alternatives = False

# --- Streamlit Page Config ---
st.set_page_config(page_title="Therapiefinder Open Source", page_icon="🧘", layout="wide")

# --- UI Layout: Hauptbereich ---
st.title("🧘 Therapiefinder Open Source")

# "Bevor du suchst"-Box (wenn noch nicht bestätigt)
if not st.session_state.knows_alternatives:
    st.info("👋 **Willkommen!** Bevor du suchst, lies bitte kurz die Box unten – sie kann dir Zeit und Nerven sparen.")

    with st.container():
        st.markdown("### 🆘 Kennst du diese Wege bereits?")
        st.markdown("""
        Bevor du mit diesem Tool suchst, prüfe bitte, ob du diese **offiziellen und oft schnelleren Wege** schon kennst:
        """)

        with st.expander("📞 116 117 – Terminservicestelle (Erstgespräch in 4 Wochen garantiert!)", expanded=False):
            st.markdown("""
            **Was ist das?**
            Die gesetzlichen Krankenkassen sind verpflichtet, dir innerhalb von 4 Wochen ein Erstgespräch zu vermitteln.

            **Wie?**
            - Anrufen: **116 117** (kostenlos, 24/7)
            - Online: [https://www.116117.de](https://www.116117.de)
            - Oder direkt bei der Kassenärztlichen Vereinigung deines Bundeslandes

            **Wichtig:** Das ist ein gesetzlicher Anspruch! Nutze ihn.
            """)

        with st.expander("💶 Kostenerstattungsverfahren (Krankenkasse zahlt Privattherapie)", expanded=False):
            st.markdown("""
            **Was ist das?**
            Wenn du nachweisen kannst, dass du keinen Kassenplatz findest (ca. 5 Absagen), kann deine Krankenkasse die Kosten für eine:n Therapeut:in ohne Kassenzulassung übernehmen.

            **Wie?**
            1. Sammle Absagen von Kassentherapeut:innen (5-10 Stück, je nach Kasse)
            2. Stelle einen Antrag bei deiner Krankenkasse (§13 Abs. 3 SGB V)
            3. Suche eine:n Therapeut:in ohne Kassensitz

            **Wichtig:** Antrag ERST stellen, DANN Therapie beginnen!

            **Mehr Infos:** [Deutsche Psychotherapeuten Vereinigung](https://www.deutsche-psychotherapeuten-vereinigung.de/patienten/kostenerstattung/)
            """)

        with st.expander("🏥 Weitere Optionen (PIAs, Ausbildungsinstitute, Online-Therapie)", expanded=False):
            st.markdown("""
            **Psychiatrische Institutsambulanzen (PIAs):**
            Ambulanzen an psychiatrischen Kliniken – oft kürzere Wartezeiten, interdisziplinäres Team.

            **Ausbildungsinstitute:**
            Therapeut:innen in Ausbildung (unter Supervision) – oft kürzere Wartezeiten, motiviert, oft Kassenzulassung.

            **Online-Therapie / Videosprechstunde:**
            Viele Therapeut:innen bieten Videotherapie an – erweitert deinen Suchradius auf ganz Deutschland.

            **Selbsthilfegruppen:**
            Überbrücken die Wartezeit und bieten Austausch. [https://www.nakos.de](https://www.nakos.de)
            """)

        st.markdown("---")
        knows_alternatives_checkbox = st.checkbox(
            "✅ Ich kenne diese Optionen und möchte trotzdem mit der Suche fortfahren",
            value=False
        )

        if knows_alternatives_checkbox:
            st.session_state.knows_alternatives = True
            st.rerun()

# Erwartungsmanagement-Hinweis
st.warning("""
⚠️ **Wichtig: Erwartungen realistisch setzen**

**Was dieses Tool kann:**
- Dir eine Liste von Therapeut:innen geben, sortiert nach Profil-Aktualisierung
- E-Mail-Adressen automatisch extrahieren
- Dir Zeit beim manuellen Durchklicken sparen

**Was dieses Tool NICHT kann:**
- Garantieren, dass jemand freie Plätze hat
- Dir die emotionale Last der Suche abnehmen
- "Zuletzt aktualisiert" bedeutet NICHT "freie Plätze" – es zeigt nur, dass das Profil gepflegt wird

**Nutze dieses Tool parallel zu den offiziellen Wegen (116 117, Kostenerstattung, etc.) – nicht als Ersatz.**
""")

# Anleitung in einem Expander (aufklappbar)
with st.expander("📖 Anleitung: So funktioniert's", expanded=False):
    st.markdown("""
    1.  **Sucheinstellungen:** Gib links in der Leiste deine Postleitzahl ein und wähle Filter (z.B. Verfahren).
    2.  **Starten:** Klicke auf "Suche starten".
    3.  **Ergebnisse:** Warte kurz. Die Ergebnisse erscheinen hier.
    4.  **Sortierung:** Die Liste ist automatisch sortiert: **Zuletzt aktualisierte Profile stehen oben.**
    5.  **Kontakt & Dokumentation:** Nutze die Links oder E-Mail-Buttons für den Kontakt. Unter der Liste findest du zudem eine Vorlage für deine **Kontakte-Übersicht** zum Download.
    """)

st.info("""
**Hinweis zur Serverlast:** Um die Server von *therapie.de* zu schonen, baut dieses Tool automatisch Pausen ein. 
Zusätzlich wird die Wartezeit mit jeder durchgeführten Suche in dieser Sitzung leicht erhöht (0,5s). 
Bitte nutze das Tool verantwortungsbewusst.
""")

# --- UI Layout: Seitenleiste (Sidebar) ---
with st.sidebar:
    st.header("🔍 Sucheinstellungen")

    # === 📍 Ort & Umkreis ===
    st.subheader("📍 Ort & Umkreis")

    zip_code = st.text_input(
        "Postleitzahl",
        value=DEFAULT_ZIP_CODE,
        max_chars=5,
        help="Gib hier die 5-stellige Postleitzahl des Ortes ein, in dem du suchen möchtest."
    )

    selected_umkreis = st.selectbox(
        "Umkreis (km)",
        options=list(UMKREIS_OPTIONS.keys()),
        help="Suche in einem Umkreis um die angegebene Postleitzahl. 'Kein Umkreis' sucht nur in der exakten PLZ."
    )

    st.markdown("---")

    # === 🏥 Therapieart ===
    st.subheader("🏥 Therapieart")

    selected_verfahren = st.selectbox(
        "Verfahren",
        options=list(VERFAHREN_OPTIONS.keys()),
        help="Welches Therapieverfahren suchst du? (z.B. Verhaltenstherapie oder Psychoanalyse)"
    )

    selected_angebot = st.selectbox(
        "Angebot",
        options=list(ANGEBOT_OPTIONS.keys()),
        help="Für wen ist die Therapie? Einzelperson, Paar, Gruppe oder Kind/Jugendlicher?"
    )

    selected_schwerpunkt = st.selectbox(
        "Schwerpunkt",
        options=list(SCHWERPUNKT_OPTIONS.keys()),
        help="Hast du ein spezielles Anliegen oder eine Diagnose? (z.B. Depression, ADHS, Angst)"
    )

    st.markdown("---")

    # === 💰 Praktisches ===
    st.subheader("💰 Praktisches")

    selected_abrechnung = st.selectbox(
        "Abrechnung",
        options=list(ABRECHNUNG_OPTIONS.keys()),
        help="Wie möchtest du die Therapie bezahlen? Gesetzlich (GKV), Privat oder als Selbstzahler?"
    )

    selected_wartezeit = st.selectbox(
        "Verfügbarkeit / Wartezeit",
        options=list(WARTEZEIT_OPTIONS.keys()),
        help="Filtere nach Therapeuten, die explizit freie Plätze oder kurzfristige Termine melden."
    )

    st.markdown("---")

    # === 👤 Persönliches ===
    st.subheader("👤 Persönliches")

    selected_geschlecht = st.selectbox(
        "Geschlecht",
        options=list(GESCHLECHT_OPTIONS.keys()),
        help="Bevorzugst du eine Therapeutin oder einen Therapeuten?"
    )

    st.markdown("---")

    # Info zur automatischen Pagination
    st.info("ℹ️ Das Tool durchsucht automatisch **alle** verfügbaren Ergebnisseiten. Je mehr Ergebnisse, desto länger dauert die Suche.")

    # Der "Start"-Button
    start_search = st.button("Suche starten", type="primary")

    st.markdown("---") # Trennlinie

    # E-Mail-Vorlagen zum Kopieren
    with st.expander("✉️ E-Mail-Vorlagen zum Kopieren"):
        st.markdown("""
        Hier findest du Vorlagen, die dir das Anschreiben von Therapeuten erleichtern.
        Kopiere den Text, füge die Details ein und sende die E-Mail.
        """)

        st.subheader("Anfrage Erstgespräch (Standard)")
        st.code(EMAIL_TEMPLATE_ERSTGESPRAECH, language="text")

        st.subheader("Anfrage Warteliste")
        st.code(EMAIL_TEMPLATE_WARTELISTE, language="text")

        st.subheader("Anfrage Kostenerstattungsverfahren")
        st.warning("(Bitte informiere dich vorher bei deiner Krankenkasse über die Voraussetzungen!)")
        st.code(EMAIL_TEMPLATE_KOSTENERSTATTUNG, language="text")

# --- Hauptlogik ---
if start_search:
    # 1. Cooldown Check (Sicherheitsmechanismus)
    now = datetime.now()

    if st.session_state.last_search_time is not None:
        elapsed = (now - st.session_state.last_search_time).total_seconds()
        if elapsed < COOLDOWN_SECONDS:
            wait_time = int(COOLDOWN_SECONDS - elapsed)
            st.error(f"🛑 Bitte warte noch {wait_time} Sekunden vor der nächsten Suche, um den Server nicht zu überlasten.")
            st.stop() # Bricht die Ausführung hier ab
            
    # 2. Validierung
    if not zip_code or len(zip_code) != 5:
        st.error("Bitte gib eine gültige 5-stellige Postleitzahl ein.")
    else:
        # Aktuelle Strafe anzeigen (nur wenn > 0)
        penalty_msg = ""
        if st.session_state.delay_penalty > 0:
            penalty_msg = f" (Drosselung aktiv: +{st.session_state.delay_penalty}s pro Anfrage)"
            
        with st.spinner(f"Suche läuft für PLZ {zip_code}... {penalty_msg}"):

            # IDs holen
            verfahren_id = VERFAHREN_OPTIONS[selected_verfahren]
            abrechnung_id = ABRECHNUNG_OPTIONS[selected_abrechnung]
            angebot_id = ANGEBOT_OPTIONS[selected_angebot]
            schwerpunkt_id = SCHWERPUNKT_OPTIONS[selected_schwerpunkt]
            geschlecht_id = GESCHLECHT_OPTIONS[selected_geschlecht]
            wartezeit_id = WARTEZEIT_OPTIONS[selected_wartezeit]
            umkreis_id = UMKREIS_OPTIONS[selected_umkreis]
            
            try:
                # Scraper aufrufen mit der aktuellen "Strafe"
                results = scrape_therapists(
                    zip_code=zip_code,
                    verfahren=verfahren_id,
                    abrechnung=abrechnung_id,
                    angebot=angebot_id,
                    schwerpunkt=schwerpunkt_id,
                    geschlecht=geschlecht_id,
                    terminzeitraum=wartezeit_id,
                    umkreis=umkreis_id,
                    additional_delay=st.session_state.delay_penalty
                )
                
                # Update Session State NACH erfolgreicher Suche
                st.session_state.last_search_time = datetime.now()
                st.session_state.delay_penalty += DELAY_PENALTY_INCREMENT # Strafe erhöhen
                
                if not results:
                    st.warning("Keine Therapeuten gefunden. Versuche, die Filter weniger strikt zu setzen.")
                else:
                    st.success(f"{len(results)} Therapeuten gefunden!")

                    # Hinweis zur Sortierung
                    st.info("ℹ️ **Die Liste ist nach 'Letzte Änderung' sortiert.** Das bedeutet NICHT, dass Plätze frei sind – es zeigt nur, dass das Profil gepflegt wird. Trotzdem sind aktive Profile oft eher erreichbar als verwaiste Profile.")

                    df = pd.DataFrame(results)
                    df_display = df[['name', 'last_modified', 'email', 'website', 'url']].copy()
                    df_display.columns = ['Name', 'Letzte Änderung', 'E-Mail', 'Webseite', 'Profil-Link']

                    st.data_editor(
                        df_display,
                        column_config={
                            "Profil-Link": st.column_config.LinkColumn("Link"),
                            "Webseite": st.column_config.LinkColumn("Webseite"),
                            "E-Mail": st.column_config.LinkColumn("E-Mail", display_text="E-Mail senden"),
                            "Letzte Änderung": st.column_config.TextColumn(
                                "Letzte Änderung",
                                help="⚠️ Aktualisiert ≠ Plätze frei. Es zeigt nur, dass das Profil gepflegt wird."
                            )
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # UTF-8-BOM für bessere Excel-Kompatibilität
                    csv = df_display.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 Ergebnisse als CSV herunterladen",
                        data=csv,
                        file_name=f'therapeuten_{zip_code}.csv',
                        mime='text/csv',
                    )

                    st.markdown("---")
                    
                    # Download-Button für die Kontakte-Übersicht (Tracking-Vorlage)
                    st.markdown("### 📊 Deine Kontakte-Übersicht")
                    st.markdown("Um den Überblick über deine Kontaktaufnahmen zu behalten, lade dir hier eine Vorlage herunter. Du kannst sie mit Excel oder Google Sheets bearbeiten.")

                    tracking_template_columns = [
                        "Name des Therapeuten",
                        "Datum des Kontakts",
                        "Kontaktaufnahme per (Telefon/E-Mail)",
                        "Status (z.B. Warteliste, Termin erhalten, Absage, kein Rückruf)",
                        "Notizen",
                        "Nächster Schritt"
                    ]
                    tracking_df = pd.DataFrame(columns=tracking_template_columns)
                    # UTF-8-BOM für bessere Excel-Kompatibilität
                    tracking_csv = tracking_df.to_csv(index=False, encoding='utf-8-sig')

                    st.download_button(
                        label="⬇️ Vorlage Kontakte-Übersicht herunterladen (CSV)",
                        data=tracking_csv,
                        file_name='Therapie_Kontakte_Uebersicht_Vorlage.csv',
                        mime='text/csv',
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Netzwerkfehler: Verbindung zu therapie.de fehlgeschlagen. Bitte überprüfe deine Internetverbindung und versuche es erneut.")
                st.error(f"Details: {e}")
            except Exception as e:
                st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
                st.error("Bitte versuche es erneut oder melde das Problem.")

st.markdown("---")

# --- UI Layout: Hauptbereich - E-Mail-Vorlagen (zusätzlich) ---
with st.expander("✉️ E-Mail-Vorlagen", expanded=False):
    st.markdown("""
Hier findest du Vorlagen, die dir das Anschreiben von Therapeuten erleichtern.
Kopiere den Text (nutze das **Kopier-Icon** oben rechts im Code-Feld), füge die Details ein und sende die E-Mail.
    """)

    st.subheader("Anfrage Erstgespräch (Standard)")
    st.code(EMAIL_TEMPLATE_ERSTGESPRAECH, language="text")

    st.subheader("Anfrage Warteliste")
    st.code(EMAIL_TEMPLATE_WARTELISTE, language="text")

    st.subheader("Anfrage Kostenerstattungsverfahren")
    st.warning("(Bitte informiere dich vorher bei deiner Krankenkasse über die Voraussetzungen!)")
    st.code(EMAIL_TEMPLATE_KOSTENERSTATTUNG, language="text")

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; color: #555;">
        <p><em>Hinweis: Dieses Tool ist ein inoffizieller Helper und steht in keiner Verbindung zu therapie.de.</em></p>
        <h3 style="margin: 20px 0; color: #2e7d32;">Du bist es wert – gib nicht auf! ❤️</h3>
        <p>
            <a href="https://github.com/PhilGabriel/therapiefinder-opensource" target="_blank" style="text-decoration: none; color: #0366d6;">GitHub-Projekt</a> •
            <a href="https://github.com/PhilGabriel/therapiefinder-opensource/blob/main/LICENSE" target="_blank" style="text-decoration: none; color: #0366d6;">Lizenz (MIT)</a> •
            <a href="https://github.com/PhilGabriel/therapiefinder-opensource/blob/main/INSTALLATION.md" target="_blank" style="text-decoration: none; color: #0366d6;">Installation</a> •
            <a href="https://github.com/PhilGabriel/therapiefinder-opensource/blob/main/CONTRIBUTING.md" target="_blank" style="text-decoration: none; color: #0366d6;">Mitarbeiten</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

