# 🧘 Therapiefinder Open Source

Ein einfaches, aber mächtiges Tool, um die Suche nach Therapieplätzen auf [therapie.de](https://www.therapie.de) effizienter zu gestalten. 

Dieses Projekt bietet eine benutzerfreundliche Web-Oberfläche, um Therapeuten zu finden und die Ergebnisse nach dem **Datum der letzten Profil-Aktualisierung** zu sortieren. So findest du schneller aktive Profile.

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

## 🤝 Mitwirken

Pull Requests sind willkommen! Wenn du Ideen hast, wie man das Tool verbessern kann, eröffne gerne ein Issue.

## 📄 Lizenz

[MIT](LICENSE)
