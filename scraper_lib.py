import requests
from bs4 import BeautifulSoup
import time
import random
import re
from datetime import datetime

# Die Basis-URL für die Therapeutensuche auf therapie.de
BASE_URL = "https://www.therapie.de/therapeutensuche/ergebnisse/"

def get_page_content(session, url, params=None):
    """
    Lädt den Inhalt einer Webseite herunter.
    
    Nutzt eine bestehende Session, um Cookies (falls nötig) beizubehalten
    und effizienter zu sein.
    
    Args:
        session (requests.Session): Die aktive Browser-Session.
        url (str): Die URL, die geladen werden soll.
        params (dict, optional): URL-Parameter (z.B. Suchfilter).
        
    Returns:
        str: Der HTML-Text der Seite oder None bei Fehlern.
    """
    try:
        # Wir tarnen uns als normaler Browser (Chrome auf Windows), 
        # damit wir nicht sofort als Bot blockiert werden.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = session.get(url, params=params, headers=headers)
        response.raise_for_status() # Wirft einen Fehler, wenn der Statuscode nicht 200 (OK) ist.
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen von {url}: {e}")
        return None

def scrape_therapists(zip_code, verfahren, abrechnung, angebot, schwerpunkt, max_pages=2, additional_delay=0.0):
    """
    Hauptfunktion zum Sammeln der Therapeuten-Daten.
    
    Durchsucht mehrere Ergebnisseiten, extrahiert die Basis-Infos und geht dann
    auf jedes einzelne Profil, um Details wie E-Mail und "Letzte Änderung" zu holen.
    
    Args:
        zip_code (str): Postleitzahl für die Suche.
        verfahren (str): ID des Therapieverfahrens.
        abrechnung (str): ID der Abrechnungsmethode.
        angebot (str): ID des Therapieangebots.
        schwerpunkt (str): ID des Arbeitsschwerpunkts.
        max_pages (int): Wie viele Seiten der Suchergebnisse durchsucht werden sollen.
        additional_delay (float): Zusätzliche Wartezeit in Sekunden pro Anfrage (zur Drosselung).
        
    Returns:
        list: Eine Liste von Dictionaries mit den Daten der Therapeuten.
    """
    
    # Parameter für die Suchanfrage an therapie.de zusammenbauen
    search_params = {
        "ort": zip_code,
        "verfahren": verfahren,
        "abrechnungsverfahren": abrechnung,
        "therapieangebot": angebot,
        "arbeitsschwerpunkt": schwerpunkt,
        "terminzeitraum": 1 # 1 steht oft für "kurzfristig" oder allgemeine Suche
    }

    therapists = []
    
    # Wir nutzen einen Context Manager für die Session, damit Verbindungen sauber geschlossen werden.
    with requests.Session() as session:
        
        # --- SCHRITT 1: Suchergebnisseiten durchlaufen ---
        for page in range(1, max_pages + 1):
            params = search_params.copy()
            if page > 1:
                params['page'] = page
            
            # Seite laden
            content = get_page_content(session, BASE_URL, params=params)
            if not content:
                break # Wenn Seite leer oder Fehler, brechen wir ab.
                
            soup = BeautifulSoup(content, 'lxml')
            
            # Die Therapeuten sind in Listen-Elementen (li) mit der Klasse 'panel-default'
            therapist_cards = soup.find_all('li', class_='panel-default')
            
            if not therapist_cards:
                break # Keine Ergebnisse mehr

            for card in therapist_cards:
                link_tag = card.find('a')
                name_tag = link_tag.find('div', class_='search-results-name')
                
                if link_tag and link_tag.has_attr('href') and name_tag:
                    profile_url = "https://www.therapie.de" + link_tag['href']
                    name = name_tag.text.strip()
                    
                    # Duplikate vermeiden (falls jemand auf Seite 1 und 2 auftaucht)
                    if not any(t['url'] == profile_url for t in therapists):
                        therapists.append({"name": name, "url": profile_url})
            
            # WICHTIG: Kurze Pause + dynamische Drosselung
            time.sleep(random.uniform(0.5, 1.5) + additional_delay) 

    # --- SCHRITT 2: Details pro Profil laden ---
    # Jetzt besuchen wir jedes gefundene Profil einzeln.
    enhanced_therapists = []
    
    with requests.Session() as session:
        for therapist in therapists:
            # Profilseite laden
            profile_content = get_page_content(session, therapist['url'])
            if profile_content:
                profile_soup = BeautifulSoup(profile_content, 'lxml')
                
                # -- Datum der letzten Änderung finden --
                # Das ist das Kern-Feature: Wir suchen nach dem Text "Letzte Änderung am"
                last_modified_tag = profile_soup.find(string=re.compile(r"Letzte Änderung am"))
                if last_modified_tag:
                    therapist['last_modified'] = last_modified_tag.strip().replace("Letzte Änderung am ", "")
                else:
                    therapist['last_modified'] = "N/A"
                
                # -- Webseite finden --
                web_div = profile_soup.find('div', class_='contact-web')
                if web_div:
                    link = web_div.find('a')
                    therapist['website'] = link['href'] if link else ""
                else:
                    therapist['website'] = ""

                # -- E-Mail entschlüsseln --
                # Therapie.de schützt E-Mails oft durch eine einfache Verschlüsselung (Caesar-Chiffre o.ä.)
                # oder versteckt sie in data-Attributen.
                email_div = profile_soup.find('div', class_='contact-mail')
                therapist['email'] = ""
                if email_div:
                    email_btn = email_div.find('button', attrs={'data-contact-email': True})
                    if email_btn:
                        encrypted = email_btn['data-contact-email']
                        try:
                            # Versuch einer einfachen Entschlüsselung (Shift -1)
                            # Hinweis: Das funktioniert nicht immer garantiert für alle Profile,
                            # ist aber der gängige Weg bei dieser Art von Schutz.
                            therapist['email'] = "".join([chr(ord(c) - 1) for c in encrypted])
                        except:
                            pass # Wenn es fehlschlägt, bleibt das Feld leer.

            enhanced_therapists.append(therapist)
            
            # WICHTIG: Wieder Pause + dynamische Drosselung
            time.sleep(random.uniform(0.5, 1.0) + additional_delay)
            
    # --- SCHRITT 3: Sortierung ---
    # Wir sortieren die Ergebnisse so, dass das aktuellste Datum oben steht.
    def parse_date(date_str):
        if date_str == "N/A": return datetime.min # N/A kommt ganz nach unten
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except:
            return datetime.min

    enhanced_therapists.sort(key=lambda x: parse_date(x['last_modified']), reverse=True)
    
    return enhanced_therapists

