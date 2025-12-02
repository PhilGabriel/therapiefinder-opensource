import streamlit as st
import pandas as pd
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
    # Bei Bedarf können hier weitere Verfahren ergänzt werden.
    # Die IDs findet man im Quelltext der therapie.de Suchmaske.
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

# --- Streamlit Page Config ---
# Setzt den Titel des Browser-Tabs und das Icon.
st.set_page_config(page_title="Therapiefinder Open Source", page_icon="🧘", layout="wide")

# --- UI Layout: Hauptbereich ---
st.title("🧘 Therapiefinder Open Source")
st.markdown("""
Dieses Tool durchsucht **therapie.de** nach aktuellen Einträgen und sortiert diese nach dem Datum der letzten Änderung.
So findest du Profile, die kürzlich aktualisiert wurden, was auf freie Kapazitäten hindeuten könnte. Bitte benutze das Tool mit Bedacht. Jedes mal wenn du eine Suche startest, ruft das Tool viele Seiten ab.
Das führt zu höheren Serverlasten bei Therapie.de. Sei dir also bei deiner Suchanfrage dessen bewusst.
""")

# --- UI Layout: Seitenleiste (Sidebar) ---
with st.sidebar:
    st.header("🔍 Sucheinstellungen")
    
    # Eingabefeld für die Postleitzahl (begrenzt auf 5 Zeichen)
    zip_code = st.text_input("Postleitzahl", value="50737", max_chars=5)
    
    # Dropdown-Menüs für die Filter
    selected_verfahren = st.selectbox("Verfahren", options=list(VERFAHREN_OPTIONS.keys()))
    selected_abrechnung = st.selectbox("Abrechnung", options=list(ABRECHNUNG_OPTIONS.keys()))
    selected_angebot = st.selectbox("Angebot", options=list(ANGEBOT_OPTIONS.keys()))
    selected_schwerpunkt = st.selectbox("Schwerpunkt", options=list(SCHWERPUNKT_OPTIONS.keys()))
    
    # Slider für die Anzahl der zu durchsuchenden Seiten (Performance-Bremse für Nutzer)
    max_pages = st.slider("Anzahl zu durchsuchender Seiten", 1, 5, 2)
    
    # Der "Start"-Button
    start_search = st.button("Suche starten", type="primary")

# --- Hauptlogik ---
if start_search:
    # Validierung der Eingabe
    if not zip_code or len(zip_code) != 5:
        st.error("Bitte gib eine gültige 5-stellige Postleitzahl ein.")
    else:
        # Lade-Animation anzeigen
        with st.spinner(f"Suche läuft für PLZ {zip_code}... Bitte warten (dies kann einige Sekunden dauern)"):
            
            # Hole die IDs aus den Dictionaries anhand der Auswahl
            verfahren_id = VERFAHREN_OPTIONS[selected_verfahren]
            abrechnung_id = ABRECHNUNG_OPTIONS[selected_abrechnung]
            angebot_id = ANGEBOT_OPTIONS[selected_angebot]
            schwerpunkt_id = SCHWERPUNKT_OPTIONS[selected_schwerpunkt]
            
            try:
                # Rufe die Scraper-Funktion auf (Importiert aus scraper_lib.py)
                results = scrape_therapists(
                    zip_code=zip_code, 
                    verfahren=verfahren_id, 
                    abrechnung=abrechnung_id, 
                    angebot=angebot_id, 
                    schwerpunkt=schwerpunkt_id,
                    max_pages=max_pages
                )
                
                if not results:
                    st.warning("Keine Therapeuten gefunden. Versuche, die Filter weniger strikt zu setzen.")
                else:
                    st.success(f"{len(results)} Therapeuten gefunden!")
                    
                    # Daten in einen Pandas DataFrame umwandeln (besser für Darstellung & Export)
                    df = pd.DataFrame(results)
                    
                    # Spalten auswählen und umbenennen für die Anzeige
                    df_display = df[['name', 'last_modified', 'email', 'website', 'url']].copy()
                    df_display.columns = ['Name', 'Letzte Änderung', 'E-Mail', 'Webseite', 'Profil-Link']
                    
                    # Interaktive Tabelle anzeigen
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
                    
                    # CSV Download Button erstellen
                    csv = df_display.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Ergebnisse als CSV herunterladen",
                        data=csv,
                        file_name=f'therapeuten_{zip_code}.csv',
                        mime='text/csv',
                    )

            except Exception as e:
                # Generelle Fehlerbehandlung, falls der Scraper abstürzt
                st.error(f"Ein Fehler ist aufgetreten: {e}")

st.markdown("---")
st.markdown("*Hinweis: Dieses Tool ist ein inoffizieller Helper und steht in keiner Verbindung zu therapie.de.*")

