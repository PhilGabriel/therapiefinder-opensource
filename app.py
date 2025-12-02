import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
from scraper_lib import scrape_therapists

# --- Konfiguration & Konstanten ---
# Diese Dictionaries mappen die lesbaren Namen (die der Nutzer sieht)
# auf die internen IDs, die therapie.de für die Suche verwendet.

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

# --- Session State Initialisierung ---
# Wir merken uns Dinge über die Session hinweg (z.B. wann zuletzt gesucht wurde).
if 'last_search_time' not in st.session_state:
    st.session_state.last_search_time = None
if 'delay_penalty' not in st.session_state:
    st.session_state.delay_penalty = 0.0

# --- Streamlit Page Config ---
st.set_page_config(page_title="Therapiefinder Open Source", page_icon="🧘", layout="wide")

# --- UI Layout: Hauptbereich ---
st.title("🧘 Therapiefinder Open Source")

# Anleitung in einem Expander (aufklappbar)
with st.expander("📖 Anleitung: So funktioniert's", expanded=True):
    st.markdown("""
    1.  **Sucheinstellungen:** Gib links in der Leiste deine Postleitzahl ein und wähle Filter (z.B. Verfahren).
    2.  **Starten:** Klicke auf "Suche starten".
    3.  **Ergebnisse:** Warte kurz. Die Ergebnisse erscheinen hier.
    4.  **Sortierung:** Die Liste ist automatisch sortiert: **Zuletzt aktualisierte Profile stehen oben.**
    5.  **Kontakt:** Nutze die Links oder E-Mail-Buttons, um Therapeuten zu kontaktieren.
    """)

st.info("""
**Hinweis zur Serverlast:** Um die Server von *therapie.de* zu schonen, baut dieses Tool automatisch Pausen ein. 
Zusätzlich wird die Wartezeit mit jeder durchgeführten Suche in dieser Sitzung leicht erhöht (0,5s). 
Bitte nutze das Tool verantwortungsbewusst.
""")

# --- UI Layout: Seitenleiste (Sidebar) ---
with st.sidebar:
    st.header("🔍 Sucheinstellungen")
    
    # Eingabefeld für die Postleitzahl mit Tooltip
    zip_code = st.text_input(
        "Postleitzahl", 
        value="50737", 
        max_chars=5,
        help="Gib hier die 5-stellige Postleitzahl des Ortes ein, in dem du suchen möchtest."
    )
    
    # Dropdown-Menüs mit Tooltips
    selected_verfahren = st.selectbox(
        "Verfahren", 
        options=list(VERFAHREN_OPTIONS.keys()),
        help="Welches Therapieverfahren suchst du? (z.B. Verhaltenstherapie oder Psychoanalyse)"
    )
    
    selected_abrechnung = st.selectbox(
        "Abrechnung", 
        options=list(ABRECHNUNG_OPTIONS.keys()),
        help="Wie möchtest du die Therapie bezahlen? Gesetzlich (GKV), Privat oder als Selbstzahler?"
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
    
    # Slider
    max_pages = st.slider(
        "Anzahl zu durchsuchender Seiten", 1, 5, 2,
        help="Wie viele Ergebnisseiten auf therapie.de sollen durchsucht werden? Mehr Seiten = Längere Wartezeit."
    )
    
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
        st.code(f"""Sehr geehrte/r Frau/Herr [Name des Therapeuten],

ich bin auf der Suche nach einem Therapieplatz und habe Ihr Profil auf therapie.de gefunden. Ich leide unter [kurze Beschreibung des Problems, z.B. Angstzuständen / Depressionen] und würde gerne ein Erstgespräch mit Ihnen vereinbaren, um zu prüfen, ob eine Therapie bei Ihnen für mich in Frage kommt.

Ich bin [Versicherungsstatus, z.B. gesetzlich / privat] versichert.

Über eine Rückmeldung freue ich mich sehr.

Mit freundlichen Grüßen,

[Dein Name]
[Deine Telefonnummer]""", language="text")

        st.subheader("Anfrage Warteliste")
        st.code(f"""Sehr geehrte/r Frau/Herr [Name des Therapeuten],

ich bin auf der Suche nach einem Therapieplatz und habe Ihr Profil auf therapie.de gefunden. Mir ist bewusst, dass es oft Wartezeiten gibt. Ich würde mich dennoch gerne für einen Therapieplatz vormerken lassen und mich ggf. auf Ihre Warteliste setzen lassen.

Ich leide unter [kurze Beschreibung des Problems, z.B. Angstzuständen / Depressionen] und bin [Versicherungsstatus, z.B. gesetzlich / privat] versichert.

Über eine Rückmeldung freue ich mich sehr.

Mit freundlichen Grüßen,

[Dein Name]
[Deine Telefonnummer]""", language="text")
        
        st.subheader("Anfrage Kostenerstattungsverfahren")
        st.warning("(Bitte informiere dich vorher bei deiner Krankenkasse über die Voraussetzungen!)")
        st.code(f"""Sehr geehrte/r Frau/Herr [Name des Therapeuten],

ich bin auf der dringenden Suche nach einem Therapieplatz und habe Ihr Profil auf therapie.de gefunden. Da ich innerhalb einer angemessenen Frist keinen kassenärztlich zugelassenen Therapieplatz finden konnte, prüfe ich derzeit die Möglichkeit eines Kostenerstattungsverfahrens bei meiner Krankenkasse.

Ich leide unter [kurze Beschreibung des Problems, z.B. Angstzuständen / Depressionen] und würde gerne ein Erstgespräch mit Ihnen vereinbaren, um zu klären, ob Sie mich im Rahmen eines Kostenerstattungsverfahrens behandeln würden.

Ich bin [Versicherungsstatus, z.B. gesetzlich / privat] versichert.

Über eine Rückmeldung freue ich mich sehr.

Mit freundlichen Grüßen,

[Dein Name]
[Deine Telefonnummer]""", language="text")

# --- Hauptlogik ---
if start_search:
    # 1. Cooldown Check (Sicherheitsmechanismus)
    now = datetime.now()
    cooldown_seconds = 15
    
    if st.session_state.last_search_time is not None:
        elapsed = (now - st.session_state.last_search_time).total_seconds()
        if elapsed < cooldown_seconds:
            wait_time = int(cooldown_seconds - elapsed)
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
            
            try:
                # Scraper aufrufen mit der aktuellen "Strafe"
                results = scrape_therapists(
                    zip_code=zip_code, 
                    verfahren=verfahren_id, 
                    abrechnung=abrechnung_id, 
                    angebot=angebot_id, 
                    schwerpunkt=schwerpunkt_id,
                    max_pages=max_pages,
                    additional_delay=st.session_state.delay_penalty
                )
                
                # Update Session State NACH erfolgreicher Suche
                st.session_state.last_search_time = datetime.now()
                st.session_state.delay_penalty += 0.5 # Strafe erhöhen
                
                if not results:
                    st.warning("Keine Therapeuten gefunden. Versuche, die Filter weniger strikt zu setzen.")
                else:
                    st.success(f"{len(results)} Therapeuten gefunden!")
                    
                    df = pd.DataFrame(results)
                    df_display = df[['name', 'last_modified', 'email', 'website', 'url']].copy()
                    df_display.columns = ['Name', 'Letzte Änderung', 'E-Mail', 'Webseite', 'Profil-Link']
                    
                    st.data_editor(
                        df_display,
                        column_config={
                            "Profil-Link": st.column_config.LinkColumn("Link"),
                            "Webseite": st.column_config.LinkColumn("Webseite"),
                            "E-Mail": st.column_config.LinkColumn("E-Mail", display_text="E-Mail senden")
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    csv = df_display.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Ergebnisse als CSV herunterladen",
                        data=csv,
                        file_name=f'therapeuten_{zip_code}.csv',
                        mime='text/csv',
                    )

            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {e}")

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
tracking_csv = tracking_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇️ Vorlage Kontakte-Übersicht herunterladen (CSV)",
    data=tracking_csv,
    file_name='Therapie_Kontakte_Uebersicht_Vorlage.csv',
    mime='text/csv',
)
# --- UI Layout: Hauptbereich - E-Mail-Vorlagen (zusätzlich) ---
with st.expander("✉️ E-Mail-Vorlagen", expanded=False):
    st.markdown("""
Hier findest du Vorlagen, die dir das Anschreiben von Therapeuten erleichtern. 
Kopiere den Text (nutze das **Kopier-Icon** oben rechts im Code-Feld), füge die Details ein und sende die E-Mail.
    """)

    st.subheader("Anfrage Erstgespräch (Standard)")
    st.code(f"""Sehr geehrte/r Frau/Herr [Name des Therapeuten],

ich bin auf der Suche nach einem Therapieplatz und habe Ihr Profil auf therapie.de gefunden. Ich leide unter [kurze Beschreibung des Problems, z.B. Angstzuständen / Depressionen] und würde gerne ein Erstgespräch mit Ihnen vereinbaren, um zu prüfen, ob eine Therapie bei Ihnen für mich in Frage kommt.

Ich bin [Versicherungsstatus, z.b. gesetzlich / privat] versichert.

Über eine Rückmeldung freue ich mich sehr.

Mit freundlichen Grüßen,

[Dein Name]
[Deine Telefonnummer]""", language="text")

    st.subheader("Anfrage Warteliste")
    st.code(f"""Sehr geehrte/r Frau/Herr [Name des Therapeuten],

ich bin auf der Suche nach einem Therapieplatz und habe Ihr Profil auf therapie.de gefunden. Mir ist bewusst, dass es oft Wartezeiten gibt. Ich würde mich dennoch gerne für einen Therapieplatz vormerken lassen und mich ggf. auf Ihre Warteliste setzen lassen.

Ich leide unter [kurze Beschreibung des Problems, z.B. Angstzuständen / Depressionen] und bin [Versicherungsstatus, z.b. gesetzlich / privat] versichert.

Über eine Rückmeldung freue ich mich sehr.

Mit freundlichen Grüßen,

[Dein Name]
[Deine Telefonnummer]""", language="text")
    
    st.subheader("Anfrage Kostenerstattungsverfahren")
    st.warning("(Bitte informiere dich vorher bei deiner Krankenkasse über die Voraussetzungen!)")
    st.code(f"""Sehr geehrte/r Frau/Herr [Name des Therapeuten],

ich bin auf der dringenden Suche nach einem Therapieplatz und habe Ihr Profil auf therapie.de gefunden. Da ich innerhalb einer angemessenen Frist keinen kassenärztlich zugelassenen Therapieplatz finden konnte, prüfe ich derzeit die Möglichkeit eines Kostenerstattungsverfahrens bei meiner Krankenkasse.

Ich leide unter [kurze Beschreibung des Problems, z.B. Angstzuständen / Depressionen] und würde gerne ein Erstgespräch mit Ihnen vereinbaren, um zu klären, ob Sie mich im Rahmen eines Kostenerstattungsverfahrens behandeln würden.

Ich bin [Versicherungsstatus, z.b. gesetzlich / privat] versichert.

Über eine Rückmeldung freue ich mich sehr.

Mit freundlichen Grüßen,

[Dein Name]
[Deine Telefonnummer]""", language="text")

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

