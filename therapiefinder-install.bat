@echo off
chcp 65001 >nul
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║       🧘 Therapiefinder Open Source - Installer             ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Dieser Installer richtet das Programm automatisch ein.
echo Das kann ein paar Minuten dauern...
echo.

REM Prüfe ob Python installiert ist
echo [1/4] Prüfe Python-Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ FEHLER: Python ist nicht installiert!
    echo.
    echo Bitte installiere Python von: https://www.python.org/downloads/
    echo.
    echo WICHTIG: Aktiviere bei der Installation "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo    ✓ Python gefunden!
echo.

REM Erstelle virtuelle Umgebung
echo [2/4] Erstelle virtuelle Umgebung...
if exist venv (
    echo    Virtuelle Umgebung existiert bereits - überspringe
) else (
    python -m venv venv
    if errorlevel 1 (
        echo    ❌ Fehler beim Erstellen der virtuellen Umgebung
        pause
        exit /b 1
    )
    echo    ✓ Virtuelle Umgebung erstellt
)
echo.

REM Prüfe ob requirements.txt existiert
if not exist requirements.txt (
    echo.
    echo    ❌ FEHLER: requirements.txt nicht gefunden!
    echo    Bist du im richtigen Ordner?
    pause
    exit /b 1
)

REM Aktiviere virtuelle Umgebung und installiere Pakete
echo [3/4] Installiere benötigte Pakete...
echo    (Dies kann 1-2 Minuten dauern...)
echo.
call venv\Scripts\activate.bat
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo    ❌ Fehler beim Installieren der Pakete
    echo    Möglicherweise fehlt eine Internetverbindung?
    pause
    exit /b 1
)
echo    ✓ Alle Pakete erfolgreich installiert
echo.

REM Erstelle Start-Script
echo [4/4] Erstelle Start-Script...
if exist therapiefinder-start.bat (
    echo    Start-Script existiert bereits - überspringe
) else (
    (
        echo @echo off
        echo chcp 65001 ^>nul
        echo cls
        echo.
        echo ╔══════════════════════════════════════════════════════════════╗
        echo ║                                                              ║
        echo ║       🧘 Therapiefinder Open Source                         ║
        echo ║                                                              ║
        echo ╚══════════════════════════════════════════════════════════════╝
        echo.
        echo Starte Anwendung...
        echo.
        echo Die App öffnet sich automatisch im Browser.
        echo Drücke STRG+C zum Beenden.
        echo.
        echo.
        echo REM Wechsle ins Script-Verzeichnis
        echo cd /d "%%~dp0"
        echo.
        echo REM Prüfe ob venv existiert
        echo if not exist venv (
        echo     echo ❌ FEHLER: Virtuelle Umgebung nicht gefunden!
        echo     echo Bitte führe zuerst therapiefinder-install.bat aus.
        echo     pause
        echo     exit /b 1
        echo ^)
        echo.
        echo REM Aktiviere virtuelle Umgebung
        echo call venv\Scripts\activate.bat
        echo if errorlevel 1 (
        echo     echo ❌ FEHLER: Konnte virtuelle Umgebung nicht aktivieren.
        echo     pause
        echo     exit /b 1
        echo ^)
        echo.
        echo REM Starte Streamlit
        echo streamlit run app.py
        echo pause
    ) > therapiefinder-start.bat
    echo    ✓ Start-Script erstellt
)
echo.

echo ══════════════════════════════════════════════════════════════
echo.
echo ✅ Installation erfolgreich abgeschlossen!
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo 📋 Nächste Schritte:
echo.
echo    1. Doppelklick auf "therapiefinder-start.bat" zum Starten
echo    2. Die App öffnet sich automatisch im Browser
echo    3. Gib deine Postleitzahl ein und klicke "Suche starten"
echo.
echo 💡 Tipp: Du kannst "therapiefinder-start.bat" als Verknüpfung
echo    auf den Desktop ziehen für noch einfacheren Zugriff!
echo.
echo ══════════════════════════════════════════════════════════════
echo.
pause
