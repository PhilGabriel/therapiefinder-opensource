# 📖 Detaillierte Installationsanleitung & Fehlerbehebung

Willkommen! Diese Anleitung führt dich Schritt für Schritt durch die Installation des **Therapiefinder Open Source** Tools. Sie ist so geschrieben, dass auch Personen ohne Programmierkenntnisse sie befolgen können.

---

## ⚡ Schnellstart: One-Click-Installer (Empfohlen!)

**Die einfachste Methode - keine technischen Kenntnisse nötig!**

### Für Windows-Nutzer:

1. **Download**:
   - Klicke auf [diesen Link](https://github.com/PhilGabriel/therapiefinder-opensource/archive/refs/heads/main.zip) oder oben auf GitHub auf den grünen Button "Code" → "Download ZIP"
   - Entpacke die ZIP-Datei in einen Ordner (z.B. auf dem Desktop)

2. **Installation**:
   - Öffne den entpackten Ordner
   - **Doppelklick** auf die Datei `therapiefinder-install.bat`
   - Ein schwarzes Fenster öffnet sich und richtet alles automatisch ein (dauert ca. 2-3 Minuten)
   - Warte, bis "Installation erfolgreich abgeschlossen!" erscheint

3. **Starten**:
   - **Doppelklick** auf die neu erstellte Datei `therapiefinder-start.bat`
   - Die App öffnet sich automatisch im Browser
   - Fertig! 🎉

**💡 Tipp für später**: Du kannst `therapiefinder-start.bat` als Verknüpfung auf deinen Desktop ziehen, um das Programm schnell zu starten.

### Für Mac/Linux-Nutzer:

1. **Download**:
   - Klicke auf [diesen Link](https://github.com/PhilGabriel/therapiefinder-opensource/archive/refs/heads/main.zip) oder oben auf GitHub auf den grünen Button "Code" → "Download ZIP"
   - Entpacke die ZIP-Datei in einen Ordner

2. **Installation**:
   - Öffne das Terminal (Mac: Programme → Dienstprogramme → Terminal)
   - Wechsle in den entpackten Ordner:
     ```bash
     cd Pfad/zum/therapiefinder-opensource
     ```
   - Führe den Installer aus:
     ```bash
     ./therapiefinder-install.sh
     ```
   - Warte, bis "Installation erfolgreich abgeschlossen!" erscheint

3. **Starten**:
   - Im Terminal ausführen:
     ```bash
     ./therapiefinder-start.sh
     ```
   - Die App öffnet sich automatisch im Browser
   - Fertig! 🎉

---

## 📚 Manuelle Installation (Für erfahrene Nutzer oder bei Problemen)

Falls der One-Click-Installer nicht funktioniert oder du die Installation lieber manuell durchführen möchtest, folge den Schritten unten:

## 1. Voraussetzungen

Bevor wir starten, benötigst du zwei Dinge auf deinem Computer:

1.  **Python:** Das ist die Programmiersprache, in der das Tool geschrieben ist.
2.  **Git (Optional):** Ein Werkzeug, um den Code herunterzuladen. (Du kannst den Code auch als ZIP-Datei herunterladen, wenn du Git nicht installieren möchtest).

### Python installieren

*   **Windows:**
    *   Lade den Installer von [python.org](https://www.python.org/downloads/) herunter.
    *   **WICHTIG:** Setze beim Start der Installation unbedingt das Häkchen bei **"Add Python to PATH"** (ganz unten im ersten Fenster). Das ist entscheidend!
*   **macOS:**
    *   macOS hat oft schon Python, aber meist eine alte Version. Lade am besten die aktuelle Version von [python.org](https://www.python.org/downloads/) herunter und installiere sie.
*   **Linux:**
    *   In der Regel bereits installiert. Falls nicht: `sudo apt-get install python3 python3-venv python3-pip` (für Ubuntu/Debian).

---

## 2. Code herunterladen

### Variante A: Mit Git (Empfohlen)
Öffne dein Terminal (Mac/Linux) oder die Eingabeaufforderung/PowerShell (Windows) und gib ein:
```bash
git clone https://github.com/PhilGabriel/therapiefinder-opensource.git
cd therapiefinder-opensource
```

### Variante B: Als ZIP-Datei
1.  Gehe auf die [GitHub-Seite des Projekts](https://github.com/PhilGabriel/therapiefinder-opensource).
2.  Klicke auf den grünen Button **Code** und dann auf **Download ZIP**.
3.  Entpacke die Datei in einen Ordner deiner Wahl.
4.  Öffne diesen Ordner in deinem Terminal/Eingabeaufforderung.
    *   *Tipp für Windows:* Öffne den Ordner im Explorer, klicke oben in die Adressleiste, tippe `cmd` ein und drücke Enter.

---

## 3. Installation einrichten

Wir nutzen eine "virtuelle Umgebung". Das ist wie ein eigener kleiner Raum für dieses Programm, damit es sich nicht mit anderen Programmen auf deinem Computer beißt.

### Schritt 3.1: Virtuelle Umgebung erstellen

**Windows:**
```cmd
python -m venv venv
```

**Mac / Linux:**
```bash
python3 -m venv venv
```

### Schritt 3.2: Virtuelle Umgebung aktivieren

Dies musst du **jedes Mal** tun, wenn du ein neues Terminal-Fenster öffnest, um das Tool zu benutzen.

**Windows (Eingabeaufforderung / cmd):**
```cmd
venv\Scripts\activate
```
*Wenn es geklappt hat, steht jetzt `(venv)` ganz am Anfang deiner Zeile.*

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```
*Falls du einen Fehler wegen "Skriptausführung" bekommst, nutze die Eingabeaufforderung (cmd) statt PowerShell.*

**Mac / Linux:**
```bash
source venv/bin/activate
```

### Schritt 3.3: Pakete installieren

Jetzt laden wir die notwendigen Hilfsprogramme herunter. Stelle sicher, dass `(venv)` am Zeilenanfang steht.

```bash
pip install -r requirements.txt
```

---

## 4. Starten

```bash
streamlit run app.py
```

Dein Browser sollte sich nun automatisch öffnen und das Tool anzeigen. Falls nicht, kopiere die Adresse (meist `http://localhost:8501`), die im schwarzen Fenster angezeigt wird, in deinen Browser.

---

## 🚀 Alternative Installation: Mit Docker

Wenn du [Docker](https://www.docker.com/) auf deinem System installiert hast, kannst du das Tool auch ganz ohne manuelle Python-Installation nutzen. Das ist besonders praktisch, wenn du keine Python-Umgebung einrichten möchtest.

1.  **Code herunterladen** (siehe Schritt 2, entweder mit Git oder als ZIP).
    ```bash
    git clone https://github.com/PhilGabriel/therapiefinder-opensource.git
    cd therapiefinder-opensource
    ```

2.  **Docker Image bauen:**
    Öffne dein Terminal/Eingabeaufforderung im Projektordner und gib ein:
    ```bash
    docker build -t therapiefinder-app .
    ```
    *(Dies kann beim ersten Mal etwas dauern, da Docker alle Abhängigkeiten herunterlädt.)*

3.  **Docker Container starten:**
    ```bash
    docker run -p 8501:8501 therapiefinder-app
    ```
    Dieser Befehl startet das Tool im Container und macht es auf deinem Computer unter `http://localhost:8501` verfügbar.

---

## ❓ Fehlerbehebung (Troubleshooting)

Hier sind Lösungen für die häufigsten Probleme:

### 0. Probleme mit dem One-Click-Installer

#### Windows: "Python ist nicht installiert"
*   **Ursache:** Python ist nicht auf deinem System installiert.
*   **Lösung:**
    1. Lade Python von [python.org/downloads](https://www.python.org/downloads/) herunter
    2. **WICHTIG**: Setze das Häkchen bei "Add Python to PATH" während der Installation
    3. Starte `install.bat` erneut

#### Mac/Linux: "Python 3 ist nicht installiert"
*   **Ursache:** Python 3 ist nicht installiert oder nicht im PATH.
*   **Lösung:**
    - **macOS**: `brew install python3` (falls Homebrew installiert ist)
    - **Linux (Ubuntu/Debian)**: `sudo apt install python3 python3-venv python3-pip`
    - Führe dann `./therapiefinder-install.sh` erneut aus

#### "Permission denied" beim Ausführen der Scripts
*   **Ursache:** Die Scripts haben keine Ausführungsrechte.
*   **Lösung:**
    ```bash
    chmod +x therapiefinder-install.sh therapiefinder-start.sh
    ./therapiefinder-install.sh
    ```

### 1. "Befehl nicht gefunden" (Command not found) bei `python` oder `pip`
*   **Ursache:** Python ist nicht installiert oder wurde nicht dem "PATH" hinzugefügt.
*   **Lösung Windows:** Installiere Python neu und vergiss das Häkchen bei **"Add Python to PATH"** nicht.
*   **Lösung Mac/Linux:** Versuche `python3` und `pip3` statt `python` und `pip`.

### 2. Fehlermeldung: `ModuleNotFoundError: No module named ...`
*   **Ursache:** Die Abhängigkeiten wurden nicht installiert oder die virtuelle Umgebung ist nicht aktiv.
*   **Lösung:**
    1.  Prüfe, ob `(venv)` am Zeilenanfang steht.
    2.  Wenn nein: Aktiviere sie (siehe Schritt 3.2).
    3.  Wenn ja: Führe `pip install -r requirements.txt` noch einmal aus.

### 3. Rote Fehlermeldungen im Browser
*   **Ursache:** Das Internet ist weg oder `therapie.de` hat die Struktur geändert.
*   **Lösung:** Überprüfe deine Internetverbindung. Wenn das Problem bestehen bleibt, erstelle bitte ein "Issue" auf GitHub, damit wir das reparieren können.

### 4. "Port 8501 is already in use"
*   **Ursache:** Das Programm läuft bereits im Hintergrund oder ein anderes Programm nutzt diesen Port.
*   **Lösung:**
    *   Schließe andere Terminal-Fenster, in denen das Tool läuft.
    *   Oder starte das Tool auf einem anderen Port: `streamlit run app.py --server.port 8502`

### 5. PowerShell Fehler: "Das Ausführen von Skripts ist deaktiviert"
*   **Lösung:** Nutze stattdessen die klassische "Eingabeaufforderung" (CMD) oder erlaube Skripte in PowerShell (google nach "PowerShell Set-ExecutionPolicy"). CMD ist für Anfänger meist einfacher.
