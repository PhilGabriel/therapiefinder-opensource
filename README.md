# 🧘 Therapiefinder Open Source

Ein einfaches, aber mächtiges Tool, um die Suche nach Therapieplätzen auf [therapie.de](https://www.therapie.de) effizienter zu gestalten. 

Dieses Projekt bietet eine benutzerfreundliche Web-Oberfläche, um Therapeuten zu finden und die Ergebnisse nach dem **Datum der letzten Profil-Aktualisierung** zu sortieren. So findest du schneller aktive Profile.
**WICHTIG** Mit jeder Suchanfrage greifst du auf Therapie.de zu, scannst Seiten und erzeugst so Serverlast. Nutze dieses Tool mit Bedacht und nicht übermäßig. Das Tool selbst hat zwar Limiter, die die Abfragen reduzieren, sei trotzdem achtsam damit. Ich übernehme keine Haftung für missbräuchliche Nutzung.

## Warum dieses Projekt?
Ich bin selbst Betroffener. Ich habe selbst die frustrierende Erfahrung gemacht 100x Nachrichten an Therapeut:inne zu schicken und finde den Prozess einfach nur quälend. Gleichzeitig hasse ich es zu telefonieren - also habe ich mir ein Tool gebaut das mir schnell die Arbeit abnimmt. Das ganze so - dass es möglichst einfach ist. Dieses Projekt bleibt solange aktiv, bis es die gesetzlichen Krankenkassen hinbekommen eine zentrale Datenbank mit allen Therapeut:innen inkl. Kontaktmöglichkeit zu etablieren, so dass es die geforderte Anonymität gegenüber den Betroffenen sicherstellt und für jede/n zugägnlich ist. Verbunden ist dieses Projekt ebenfalls mit dem Appell: Hebt die Kassensitzpflicht für Psyschotherapeut:innen auf. 

## ✨ Features

*   **Einfache Suche:** Filterung nach Postleitzahl, Verfahren, Abrechnungsmethode, Therapieangebot und Arbeitsschwerpunkt.
*   **Sortierung nach Aktualität:** Ergebnisse werden automatisch so sortiert, dass Profile, die zuletzt bearbeitet wurden, ganz oben stehen.
*   **Erweiterte Details:** Versucht automatisch, E-Mail-Adressen (auch "verschlüsselte") und Webseiten-Links aus den Profilen zu extrahieren.
*   **CSV-Export:** Lade deine Suchergebnisse bequem als Excel-kompatible CSV-Datei herunter.
*   **Lokale Ausführung:** Deine Daten bleiben bei dir. Keine Cloud, kein Tracking.

## 🚀 Installation & Start

Du benötigst [Python](https://www.python.org/) (Version 3.8 oder höher) auf deinem Computer.

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/DEIN-USERNAME/therapiefinder-opensource.git
    cd therapiefinder-opensource
    ```

2.  **Abhängigkeiten installieren:**
    Es wird empfohlen, eine virtuelle Umgebung zu nutzen:
    ```bash
    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```
    
    Dann die Pakete installieren:
    ```bash
    pip install -r requirements.txt
    ```

3.  **App starten:**
    ```bash
    streamlit run app.py
    ```

4.  **Öffnen:**
    Dein Browser sollte sich automatisch öffnen. Falls nicht, rufe `http://localhost:8501` auf.

## ⚠️ Rechtlicher Hinweis

Dieses Tool ist ein inoffizielles Hilfsprojekt und steht in keiner Verbindung zu *therapie.de* oder dem Verein *Pro Psychotherapie e.V.*. 

Bitte nutze dieses Tool verantwortungsbewusst und respektiere die Serverlast der Webseite. Das Tool beinhaltet eingebaute Pausen, um die Anfragen zu drosseln. Verwende die gesammelten Daten nur für deine persönliche Therapieplatzsuche.

## ⚖️ Haftungsausschluss

Die Nutzung dieses Tools erfolgt auf eigene Gefahr. Der Autor übernimmt keine Haftung für Schäden, die durch die Nutzung entstehen, insbesondere nicht für rechtliche Konsequenzen, die aus dem Crawlen von Webseiten resultieren könnten. Bitte informiere dich über die AGB der Zielwebseite und handele verantwortungsvoll.

## 🛡️ Datenschutz & Datenspeicherung

*   **Lokale Ausführung:** Das gesamte Programm läuft lokal auf deinem Computer. Es werden keine Daten an externe Server (außer die notwendigen Suchanfragen an `therapie.de`) gesendet.
*   **Keine Datenbank:** Das Tool speichert **keine** Suchergebnisse oder personenbezogene Daten dauerhaft auf deiner Festplatte. Alle Daten werden nur temporär im Arbeitsspeicher (RAM) gehalten, während das Programm läuft.
*   **CSV-Export:** Wenn du auf "Ergebnisse als CSV herunterladen" klickst, wird eine Datei generiert und in deinem Standard-Download-Ordner gespeichert. Diese Datei liegt in deiner Verantwortung und kann wie jede andere Datei von dir gelöscht werden.
*   **Spurenlos:** Sobald du das Browser-Fenster schließt oder das Programm beendest, sind die Suchergebnisse aus dem Arbeitsspeicher gelöscht.

## 🤝 Mitwirken

Pull Requests sind willkommen! Wenn du Ideen hast, wie man das Tool verbessern kann, eröffne gerne ein Issue.

## ❤️ Danksagung & Tech-Stack

Ein großes Dankeschön an die Entwickler der Tools, die dieses Projekt möglich machen:

*   **[Streamlit](https://streamlit.io/)** - Ermöglichte die schnelle Entwicklung der Benutzeroberfläche.
*   **[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)** - Das Herzstück für das Parsen der Webseiten.
*   **[Pandas](https://pandas.pydata.org/)** - Für die effiziente Datenverarbeitung und den CSV-Export.
*   **[Google Gemini](https://deepmind.google/technologies/gemini/)** - KI-Unterstützung bei der Code-Entwicklung und Optimierung.

## 📄 Lizenz

[MIT](LICENSE)
