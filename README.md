# 🧘 Therapiefinder Open Source

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0%2B-orange)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

Ein einfaches, aber mächtiges Tool, um die Suche nach Therapieplätzen auf [therapie.de](https://www.therapie.de) effizienter zu gestalten. 

Dieses Projekt bietet eine benutzerfreundliche Web-Oberfläche, um Therapeuten zu finden und die Ergebnisse nach dem **Datum der letzten Profil-Aktualisierung** zu sortieren. So findest du schneller aktive Profile.
**WICHTIG** Mit jeder Suchanfrage greifst du auf Therapie.de zu, scannst Seiten und erzeugst so Serverlast. Nutze dieses Tool mit Bedacht und nicht übermäßig. Das Tool selbst hat zwar Limiter, die die Abfragen reduzieren, sei trotzdem achtsam damit. Ich übernehme keine Haftung für missbräuchliche Nutzung.

---
### 📸 Screenshots

![Tool Startseite](assets/screenshots/Tool%20Startseite.jpg)
![Tool Liste](assets/screenshots/Tool%20Liste.jpg)
---

## Warum dieses Projekt?
Ich bin selbst Betroffener. Ich habe selbst die frustrierende Erfahrung gemacht 100x Nachrichten an Therapeut:inne zu schicken und finde den Prozess einfach nur quälend. Gleichzeitig hasse ich es zu telefonieren - also habe ich mir ein Tool gebaut das mir schnell die Arbeit abnimmt. Das ganze so - dass es möglichst einfach ist. Dieses Projekt bleibt solange aktiv, bis es die gesetzlichen Krankenkassen hinbekommen eine zentrale Datenbank mit allen Therapeut:innen inkl. Kontaktmöglichkeit zu etablieren, so dass es die geforderte Anonymität gegenüber den Betroffenen sicherstellt und für jede/n zugägnlich ist. Verbunden ist dieses Projekt ebenfalls mit dem Appell: Hebt die Kassensitzpflicht für Psyschotherapeut:innen auf. 

## 🆘 Wichtiger Hinweis & Unterstützung

Dieses Tool ist ein Werkzeug, das dir hilft, schneller Kontaktmöglichkeiten zu finden. **Das Anschreiben oder Anrufen der Therapeuten übernimmt es nicht – diesen Schritt musst du selbst gehen.**

Es ist ein großer und mutiger Schritt, dass du dich um einen Therapieplatz bemühst. Auch wenn die Suche oft frustrierend, langwierig und kräftezehrend sein kann: **Lass dich nicht entmutigen.** Du bist es wert, Hilfe zu bekommen, und du bist auf dem richtigen Weg.

**Wenn du sofort Hilfe brauchst:**

*   **116 117:** Der ärztliche Bereitschaftsdienst (rund um die Uhr, hilft auch bei der Terminvermittlung für Erstgespräche).
*   **Telefonseelsorge:** `0800 / 111 0 111` oder `0800 / 111 0 222` oder `116 123` (kostenlos, anonym, rund um die Uhr).
*   **Im absoluten Notfall (Suizidgedanken, Fremdgefährdung):** Wähle bitte sofort den Notruf **112** oder begib dich in die Notaufnahme der nächsten psychiatrischen Klinik.

## 💡 Tipps für eine erfolgreiche Suche

Um das Beste aus diesem Tool herauszuholen und deine Suche effizient zu gestalten, beachte folgende Hinweise:

*   **Datum der letzten Änderung:** Die Hauptfunktion dieses Tools ist die Sortierung nach dem Datum der letzten Profil-Aktualisierung. Ein kürzlich aktualisiertes Profil kann ein starkes Indiz dafür sein, dass der Therapeut aktiv ist und möglicherweise neue Patient:innen aufnimmt oder zumindest seine Informationen pflegt. Konzentriere dich daher zuerst auf die obersten Einträge der Ergebnisliste.
*   **Filter gezielt einsetzen:** Beginne mit breiteren Filtern (z.B. nur Postleitzahl) und verfeinere diese schrittweise, wenn du zu viele Ergebnisse erhältst. Manchmal führt eine zu spezifische Suche dazu, dass du relevante Therapeut:innen übersiehst.
*   **E-Mail-Adressen:** Das Tool versucht, E-Mail-Adressen (auch "verschlüsselte") zu extrahieren. Dies funktioniert nicht immer perfekt, aber es ist ein guter Startpunkt für die Kontaktaufnahme.
*   **Webseite besuchen:** Nutze den Profil-Link, um direkt zur Profilseite des Therapeuten auf `therapie.de` zu gelangen. Dort findest du oft weitere Informationen.

## ✨ Features

*   **Einfache Suche:** Filterung nach Postleitzahl, **Umkreis**, Verfahren, Geschlecht, Abrechnungsmethode, Therapieangebot, Wartezeit und Arbeitsschwerpunkt.
*   **Sortierung nach Aktualität:** Ergebnisse werden automatisch so sortiert, dass Profile, die zuletzt bearbeitet wurden, ganz oben stehen.
*   **E-Mail-Vorlagen:** Integrierte, kopierbare Textbausteine für Erstkontakt, Wartelisten-Anfragen und Kostenerstattungsverfahren.
*   **Bewerbungs-Tracker:** Lade deine Suchergebnisse oder eine leere "Kontakte-Übersicht" als CSV herunter, um den Überblick über deine Anfragen zu behalten.
*   **Erweiterte Details:** Versucht automatisch, E-Mail-Adressen (auch "verschlüsselte") und Webseiten-Links aus den Profilen zu extrahieren.
*   **Sicherheit & Fairness:** Intelligente Drosselung und Cooldown-Phasen schützen die Server von `therapie.de` vor Überlastung.
*   **Docker Support:** Einfache Installation und Ausführung in einem Container möglich.
*   **Lokale Ausführung:** Deine Daten bleiben bei dir. Keine Cloud, kein Tracking.

## 🚀 Installation & Start

### ⚡ Einfachste Methode: One-Click-Installer (Empfohlen für Einsteiger)

**Keine technischen Kenntnisse nötig!** Der Installer richtet alles automatisch ein.

1. **Download**: Lade das Projekt herunter
   - Klicke oben auf den grünen Button "Code" → "Download ZIP"
   - Entpacke die ZIP-Datei an einen Ort deiner Wahl

2. **Installation**: Doppelklick auf die richtige Datei für dein System:
   - **Windows**: `therapiefinder-install.bat` (doppelklicken)
   - **Mac/Linux**: `therapiefinder-install.sh` (im Terminal: `./therapiefinder-install.sh`)

3. **Starten**: Nach erfolgreicher Installation:
   - **Windows**: Doppelklick auf `therapiefinder-start.bat`
   - **Mac/Linux**: Im Terminal: `./therapiefinder-start.sh`

4. **Fertig!** Die App öffnet sich automatisch im Browser 🎉

**⚠️ Hinweis beim ersten Start:**
Streamlit wird beim ersten Start nach einer E-Mail-Adresse für Updates fragen. **Du musst keine E-Mail angeben** – drücke einfach **Enter**, um diesen Schritt zu überspringen. Deine Privatsphäre bleibt gewahrt, und das Tool funktioniert genauso.

💡 **Tipp**: Du kannst `therapiefinder-start.bat` (Windows) bzw. `therapiefinder-start.sh` (Mac/Linux) als Verknüpfung auf deinen Desktop ziehen!

---

### 📚 Weitere Installationsmethoden

Eine **ausführliche Schritt-für-Schritt-Anleitung** (auch für Anfänger geeignet) sowie Hilfe bei Problemen findest du in der Datei **[INSTALLATION.md](INSTALLATION.md)**.

**Schnellstart mit Docker:**
Wenn du [Docker](https://www.docker.com/) installiert hast, kannst du das Tool mit wenigen Befehlen starten. Siehe [INSTALLATION.md](INSTALLATION.md) für Details.

**Kurzfassung für Profis:**

```bash
# Repository klonen
git clone https://github.com/PhilGabriel/therapiefinder-opensource.git
cd therapiefinder-opensource

# Virtuelle Umgebung erstellen & aktivieren
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Starten
streamlit run app.py
```

## ⚠️ Rechtlicher Hinweis

Dieses Tool ist ein inoffizielles Hilfsprojekt und steht in keiner Verbindung zu *therapie.de* oder dem Verein *Pro Psychotherapie e.V.*. 

Bitte nutze dieses Tool verantwortungsbewusst und respektiere die Serverlast der Webseite. Das Tool beinhaltet eingebaute Pausen, um die Anfragen zu drosseln. Verwende die gesammelten Daten nur für deine persönliche Therapieplatzsuche.

## ⚖️ Haftungsausschluss

Die Nutzung dieses Tools erfolgt auf eigene Gefahr. Der Autor übernimmt keine Haftung für Schäden, die durch die Nutzung entstehen, insbesondere nicht für rechtliche Konsequenzen, die aus dem Crawlen von Webseiten resultieren könnten. Bitte informiere dich über die AGB der Zielwebseite und handele verantwortungsvoll.

## 🛡️ Datenschutz & Datenspeicherung

**🔒 Deine Daten bleiben privat und werden NICHT gespeichert!**

*   **Lokale Ausführung:** Das gesamte Programm läuft lokal auf deinem Computer. Es werden keine Daten an externe Server (außer die notwendigen Suchanfragen an `therapie.de`) gesendet.
*   **Keine Datenbank:** Das Tool speichert **keine** Suchergebnisse oder personenbezogene Daten dauerhaft auf deiner Festplatte. Alle Daten werden nur temporär im Arbeitsspeicher (RAM) gehalten, während das Programm läuft.
*   **Nur im Arbeitsspeicher:** Suchergebnisse existieren ausschließlich im RAM deines Computers, solange das Programm im Browser/Terminal läuft. Es gibt keine Log-Dateien, keine Datenbanken, keine persistente Speicherung.
*   **CSV-Export:** Wenn du auf "Ergebnisse als CSV herunterladen" klickst, wird eine Datei generiert und in deinem Standard-Download-Ordner gespeichert. Diese Datei liegt in deiner Verantwortung und kann wie jede andere Datei von dir gelöscht werden.
*   **Spurenlos:** Sobald du das Browser-Fenster schließt oder das Programm beendest, sind die Suchergebnisse aus dem Arbeitsspeicher gelöscht und unwiederbringlich weg.

## 🐛 Bekannte Einschränkungen & mögliche Probleme

*   **Zunehmende Wartezeit:** Um den Server zu schonen, erhöht sich die Wartezeit zwischen den Anfragen mit jeder durchgeführten Suche in einer Sitzung leicht (+0,5s). Das ist gewolltes Verhalten.
*   **Geschwindigkeit:** Die Suche kann langsam erscheinen. Das liegt daran, dass das Tool bewusst Pausen zwischen den Anfragen einlegt.
*   **Unvollständige Ergebnisse:** Manchmal werden nicht alle erwarteten Informationen (z.B. E-Mail-Adressen) gefunden. Dies kann an unterschiedlichen Formatierungen auf den Profilseiten liegen oder an Verschlüsselungstechniken von `therapie.de`.
*   **Fehlende Therapeut:innen:** Wenn du trotz lockerer Filter keine Therapeut:innen findest, kann es sein, dass zum aktuellen Zeitpunkt keine passenden Profile auf `therapie.de` verfügbar sind, die deinen Kriterien entsprechen.

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
