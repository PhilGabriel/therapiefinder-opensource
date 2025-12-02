import requests
from bs4 import BeautifulSoup
import time
import random
import re
from datetime import datetime

BASE_URL = "https://www.therapie.de/therapeutensuche/ergebnisse/"

def get_page_content(session, url, params=None):
    """Fetches the content of a page using a session."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = session.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_therapists(zip_code, verfahren, abrechnung, angebot, schwerpunkt, max_pages=2):
    """
    Scrapes therapists based on filter parameters.
    """
    search_params = {
        "ort": zip_code,
        "verfahren": verfahren,
        "abrechnungsverfahren": abrechnung,
        "therapieangebot": angebot,
        "arbeitsschwerpunkt": schwerpunkt,
        "terminzeitraum": 1 # Default to "kurzfristig" or allow passing it? Let's keep it fixed or simple for now.
    }

    therapists = []
    
    with requests.Session() as session:
        for page in range(1, max_pages + 1):
            params = search_params.copy()
            if page > 1:
                params['page'] = page
            
            # Progress callback or simple print could go here
            content = get_page_content(session, BASE_URL, params=params)
            if not content:
                break
                
            soup = BeautifulSoup(content, 'lxml')
            therapist_cards = soup.find_all('li', class_='panel-default')
            
            if not therapist_cards:
                break

            for card in therapist_cards:
                link_tag = card.find('a')
                name_tag = link_tag.find('div', class_='search-results-name')
                
                if link_tag and link_tag.has_attr('href') and name_tag:
                    profile_url = "https://www.therapie.de" + link_tag['href']
                    name = name_tag.text.strip()
                    
                    # Avoid duplicates
                    if not any(t['url'] == profile_url for t in therapists):
                        therapists.append({"name": name, "url": profile_url})
            
            time.sleep(random.uniform(0.5, 1.5)) # Be polite

    # Enhance with details (Email, Website, Date)
    enhanced_therapists = []
    with requests.Session() as session:
        for therapist in therapists:
            # Fetch profile
            profile_content = get_page_content(session, therapist['url'])
            if profile_content:
                profile_soup = BeautifulSoup(profile_content, 'lxml')
                
                # Last Modified
                last_modified_tag = profile_soup.find(string=re.compile(r"Letzte Änderung am"))
                therapist['last_modified'] = last_modified_tag.strip().replace("Letzte Änderung am ", "") if last_modified_tag else "N/A"
                
                # Website
                web_div = profile_soup.find('div', class_='contact-web')
                if web_div:
                    link = web_div.find('a')
                    therapist['website'] = link['href'] if link else ""
                else:
                    therapist['website'] = ""

                # Email (Decryption)
                email_div = profile_soup.find('div', class_='contact-mail')
                therapist['email'] = ""
                if email_div:
                    email_btn = email_div.find('button', attrs={'data-contact-email': True})
                    if email_btn:
                        encrypted = email_btn['data-contact-email']
                        try:
                            therapist['email'] = "".join([chr(ord(c) - 1) for c in encrypted])
                        except:
                            pass

            enhanced_therapists.append(therapist)
            time.sleep(random.uniform(0.5, 1.0))
            
    # Sort by date (newest first)
    def parse_date(date_str):
        if date_str == "N/A": return datetime.min
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except:
            return datetime.min

    enhanced_therapists.sort(key=lambda x: parse_date(x['last_modified']), reverse=True)
    return enhanced_therapists
