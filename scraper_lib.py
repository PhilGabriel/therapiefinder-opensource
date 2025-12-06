import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import time
import random
import re
import logging
from datetime import datetime
from typing import Optional, Dict, List

# Logger konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Konfiguration
BASE_URL = "https://www.therapie.de/therapeutensuche/ergebnisse/"
REQUEST_TIMEOUT = 30  # Timeout für HTTP-Requests in Sekunden
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Rate Limiting - Wartezeiten zwischen Requests (in Sekunden)
MIN_DELAY_SEARCH = 0.5  # Minimale Wartezeit zwischen Suchergebnisseiten
MAX_DELAY_SEARCH = 1.5  # Maximale Wartezeit zwischen Suchergebnisseiten
MIN_DELAY_PROFILE = 0.5  # Minimale Wartezeit zwischen Profilaufrufen
MAX_DELAY_PROFILE = 1.0  # Maximale Wartezeit zwischen Profilaufrufen

# Retry-Konfiguration für Netzwerkfehler
RETRY_TOTAL = 3  # Anzahl der Wiederholungsversuche
RETRY_BACKOFF_FACTOR = 1  # Wartezeit zwischen Retries (1s, 2s, 4s, ...)
RETRY_STATUS_FORCELIST = [500, 502, 503, 504]  # HTTP-Codes, bei denen wiederholt wird


def create_session_with_retries() -> requests.Session:
    """
    Erstellt eine requests-Session mit automatischer Retry-Logik.

    Returns:
        Konfigurierte Session mit Retry-Adapter.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=RETRY_TOTAL,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=RETRY_STATUS_FORCELIST,
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_page_content(session: requests.Session, url: str, params: Optional[Dict[str, str]] = None) -> Optional[str]:
    """
    Lädt den Inhalt einer Webseite herunter.

    Nutzt eine bestehende Session, um Cookies (falls nötig) beizubehalten
    und effizienter zu sein.

    Args:
        session: Die aktive Browser-Session.
        url: Die URL, die geladen werden soll.
        params: URL-Parameter (z.B. Suchfilter).

    Returns:
        Der HTML-Text der Seite oder None bei Fehlern.
    """
    try:
        # Wir tarnen uns als normaler Browser (Chrome auf Windows),
        # damit wir nicht sofort als Bot blockiert werden.
        headers = {
            'User-Agent': USER_AGENT
        }
        response = session.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status() # Wirft einen Fehler, wenn der Statuscode nicht 200 (OK) ist.
        return response.text
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout beim Abrufen von {url}: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP-Fehler beim Abrufen von {url}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Fehler beim Abrufen von {url}: {e}")
        return None

def parse_date(date_str: str) -> datetime:
    """
    Parst ein Datum im Format DD.MM.YYYY.

    Args:
        date_str: Datumsstring im Format "DD.MM.YYYY" oder "N/A".

    Returns:
        Geparste datetime-Objekt oder datetime.min bei ungültigem Datum.
    """
    if date_str == "N/A":
        return datetime.min
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except (ValueError, TypeError):
        return datetime.min


def extract_therapist_details(session: requests.Session, therapist: Dict[str, str]) -> Dict[str, str]:
    """
    Lädt Details für einen einzelnen Therapeuten von seiner Profilseite.

    Args:
        session: Die aktive Browser-Session.
        therapist: Dictionary mit Basis-Infos (name, url).

    Returns:
        Dictionary mit allen Details (name, url, last_modified, website, email).
    """
    therapist_data = therapist.copy()
    therapist_data['last_modified'] = "N/A"
    therapist_data['website'] = ""
    therapist_data['email'] = ""

    # Profilseite laden
    profile_content = get_page_content(session, therapist_data['url'])
    if not profile_content:
        return therapist_data

    profile_soup = BeautifulSoup(profile_content, 'lxml')

    # -- Datum der letzten Änderung finden --
    last_modified_tag = profile_soup.find(string=re.compile(r"Letzte Änderung am"))
    if last_modified_tag:
        therapist_data['last_modified'] = last_modified_tag.strip().replace("Letzte Änderung am ", "")

    # -- Webseite finden --
    web_div = profile_soup.find('div', class_='contact-web')
    if web_div:
        link = web_div.find('a')
        therapist_data['website'] = link['href'] if link else ""

    # -- E-Mail entschlüsseln --
    email_div = profile_soup.find('div', class_='contact-mail')
    if email_div:
        email_btn = email_div.find('button', attrs={'data-contact-email': True})
        if email_btn:
            encrypted = email_btn['data-contact-email']
            try:
                decrypted_email = "".join([chr(ord(c) - 1) for c in encrypted])
                # Mailto-Link für direktes Öffnen im E-Mail-Programm
                therapist_data['email'] = f"mailto:{decrypted_email}" if decrypted_email else ""
            except (ValueError, TypeError) as e:
                logger.warning(f"Fehler beim Entschlüsseln der E-Mail für {therapist_data['name']}: {e}")
                therapist_data['email'] = ""

    return therapist_data


def scrape_therapists(
    zip_code: str,
    verfahren: str,
    abrechnung: str,
    angebot: str,
    schwerpunkt: str,
    geschlecht: str,
    terminzeitraum: str,
    umkreis: str,
    additional_delay: float = 0.0
) -> List[Dict[str, str]]:
    """
    Hauptfunktion zum Sammeln der Therapeuten-Daten.

    Durchsucht ALLE verfügbaren Ergebnisseiten automatisch, extrahiert die Basis-Infos
    und geht dann auf jedes einzelne Profil, um Details wie E-Mail und "Letzte Änderung" zu holen.

    Args:
        zip_code: Postleitzahl für die Suche.
        verfahren: ID des Therapieverfahrens.
        abrechnung: ID der Abrechnungsmethode.
        angebot: ID des Therapieangebots.
        schwerpunkt: ID des Arbeitsschwerpunkts.
        geschlecht: ID des Geschlechts (1=w, 2=m).
        terminzeitraum: ID der Wartezeit/Verfügbarkeit.
        umkreis: Radius in km (0, 5, 10, ...).
        additional_delay: Zusätzliche Wartezeit in Sekunden pro Anfrage (zur Drosselung).

    Returns:
        Eine Liste von Dictionaries mit den Daten der Therapeuten.
    """

    # Parameter für die Suchanfrage an therapie.de zusammenbauen
    search_params = {
        "ort": zip_code,
        "verfahren": verfahren,
        "abrechnungsverfahren": abrechnung,
        "therapieangebot": angebot,
        "arbeitsschwerpunkt": schwerpunkt,
        "geschlecht": geschlecht,
        "terminzeitraum": terminzeitraum,
        "umkreis": umkreis
    }

    therapists = []
    enhanced_therapists = []

    # Wir nutzen einen Context Manager für die Session, damit Verbindungen sauber geschlossen werden.
    # Eine Session für beide Schritte verbessert die Performance durch Connection-Pooling.
    # Die Session hat automatische Retry-Logik für Netzwerkfehler.
    with create_session_with_retries() as session:

        # --- SCHRITT 1: Erste Seite laden und maximale Seitenzahl ermitteln ---
        content = get_page_content(session, BASE_URL, params=search_params)
        if not content:
            logger.warning("Erste Seite konnte nicht geladen werden.")
            return []

        soup = BeautifulSoup(content, 'lxml')

        # Maximale Seitenzahl aus dem pagenav bottom Element ermitteln
        max_pages = 1
        pagenav = soup.find('ul', class_='pagenav bottom')
        if pagenav:
            page_items = pagenav.find_all('li')
            for item in page_items:
                link = item.find('a')
                if link and link.text.strip().isdigit():
                    page_num = int(link.text.strip())
                    max_pages = max(max_pages, page_num)

        logger.info(f"Maximale Seitenzahl ermittelt: {max_pages}")

        # --- SCHRITT 2: ALLE Suchergebnisseiten durchlaufen ---
        for page in range(1, max_pages + 1):
            params = search_params.copy()
            if page > 1:
                params['page'] = page
                # Seite laden (außer Seite 1, die haben wir schon)
                content = get_page_content(session, BASE_URL, params=params)
                if not content:
                    logger.warning(f"Seite {page} konnte nicht geladen werden, überspringe.")
                    continue
                soup = BeautifulSoup(content, 'lxml')

            # Die Therapeuten sind in Listen-Elementen (li) mit der Klasse 'panel-default'
            therapist_cards = soup.find_all('li', class_='panel-default')

            if not therapist_cards:
                logger.info(f"Keine Ergebnisse auf Seite {page}.")
                continue

            logger.info(f"Seite {page}/{max_pages}: {len(therapist_cards)} Therapeut:innen gefunden.")

            for card in therapist_cards:
                link_tag = card.find('a')
                name_tag = link_tag.find('div', class_='search-results-name')

                if link_tag and link_tag.has_attr('href') and name_tag:
                    profile_url = "https://www.therapie.de" + link_tag['href']
                    name = name_tag.text.strip()

                    # Duplikate vermeiden (falls jemand auf Seite 1 und 2 auftaucht)
                    if not any(t['url'] == profile_url for t in therapists):
                        therapists.append({"name": name, "url": profile_url})

            # WICHTIG: Kurze Pause + dynamische Drosselung (außer nach der letzten Seite)
            if page < max_pages:
                time.sleep(random.uniform(MIN_DELAY_SEARCH, MAX_DELAY_SEARCH) + additional_delay)

        # --- SCHRITT 3: Details für jeden Therapeuten laden ---
        for therapist in therapists:
            therapist_data = extract_therapist_details(session, therapist)
            enhanced_therapists.append(therapist_data)
            time.sleep(random.uniform(MIN_DELAY_PROFILE, MAX_DELAY_PROFILE) + additional_delay)

    # --- SCHRITT 4: Sortierung ---
    # Wir sortieren die Ergebnisse so, dass das aktuellste Datum oben steht.
    enhanced_therapists.sort(key=lambda x: parse_date(x['last_modified']), reverse=True)
    
    return enhanced_therapists

