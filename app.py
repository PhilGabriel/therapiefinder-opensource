import streamlit as st
import pandas as pd
from scraper_lib import scrape_therapists

# --- Configuration & Constants ---
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
    # Add more as needed based on analysis
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

st.set_page_config(page_title="Therapiefinder Open Source", page_icon="🧘", layout="wide")

# --- UI Layout ---
st.title("🧘 Therapiefinder Open Source")
st.markdown("""
Dieses Tool durchsucht **therapie.de** nach aktuellen Einträgen und sortiert diese nach dem Datum der letzten Änderung.
So findest du Profile, die kürzlich aktualisiert wurden, was auf freie Kapazitäten hindeuten könnte.
""")

with st.sidebar:
    st.header("🔍 Sucheinstellungen")
    
    zip_code = st.text_input("Postleitzahl", value="50737", max_chars=5)
    
    selected_verfahren = st.selectbox("Verfahren", options=list(VERFAHREN_OPTIONS.keys()))
    selected_abrechnung = st.selectbox("Abrechnung", options=list(ABRECHNUNG_OPTIONS.keys()))
    selected_angebot = st.selectbox("Angebot", options=list(ANGEBOT_OPTIONS.keys()))
    selected_schwerpunkt = st.selectbox("Schwerpunkt", options=list(SCHWERPUNKT_OPTIONS.keys()))
    
    max_pages = st.slider("Anzahl zu durchsuchender Seiten", 1, 5, 2)
    
    start_search = st.button("Suche starten", type="primary")

# --- Main Logic ---
if start_search:
    if not zip_code or len(zip_code) != 5:
        st.error("Bitte gib eine gültige 5-stellige Postleitzahl ein.")
    else:
        with st.spinner(f"Suche läuft für PLZ {zip_code}... Bitte warten (dies kann einige Sekunden dauern)"):
            
            # Map labels to IDs
            verfahren_id = VERFAHREN_OPTIONS[selected_verfahren]
            abrechnung_id = ABRECHNUNG_OPTIONS[selected_abrechnung]
            angebot_id = ANGEBOT_OPTIONS[selected_angebot]
            schwerpunkt_id = SCHWERPUNKT_OPTIONS[selected_schwerpunkt]
            
            try:
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
                    
                    # Convert to DataFrame for better display
                    df = pd.DataFrame(results)
                    
                    # Reorder and rename columns for display
                    df_display = df[['name', 'last_modified', 'email', 'website', 'url']].copy()
                    df_display.columns = ['Name', 'Letzte Änderung', 'E-Mail', 'Webseite', 'Profil-Link']
                    
                    # Make links clickable in the table (Streamlit LinkColumn)
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
                    
                    # CSV Download
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
st.markdown("*Hinweis: Dieses Tool ist ein inoffizieller Helper und steht in keiner Verbindung zu therapie.de.*")
