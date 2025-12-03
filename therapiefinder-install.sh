#!/bin/bash

# Farben für Terminal-Output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

clear

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║       🧘 Therapiefinder Open Source - Installer             ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Dieser Installer richtet das Programm automatisch ein."
echo "Das kann ein paar Minuten dauern..."
echo ""

# Prüfe ob Python 3 installiert ist
echo -e "${BLUE}[1/4] Prüfe Python-Installation...${NC}"

if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | grep -oP '\d+' | head -1)
    if [ "$PYTHON_VERSION" -ge 3 ]; then
        PYTHON_CMD=python
    else
        echo -e "${RED}❌ FEHLER: Python 3 ist nicht installiert!${NC}"
        echo ""
        echo "Bitte installiere Python 3:"
        echo "  - macOS: brew install python3"
        echo "  - Linux: sudo apt install python3 python3-venv python3-pip"
        echo ""
        exit 1
    fi
else
    echo -e "${RED}❌ FEHLER: Python ist nicht installiert!${NC}"
    echo ""
    echo "Bitte installiere Python 3:"
    echo "  - macOS: brew install python3"
    echo "  - Linux: sudo apt install python3 python3-venv python3-pip"
    echo ""
    exit 1
fi

$PYTHON_CMD --version
echo -e "${GREEN}   ✓ Python gefunden!${NC}"
echo ""

# Erstelle virtuelle Umgebung
echo -e "${BLUE}[2/4] Erstelle virtuelle Umgebung...${NC}"
if [ -d "venv" ]; then
    echo "   Virtuelle Umgebung existiert bereits - überspringe"
else
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}   ❌ Fehler beim Erstellen der virtuellen Umgebung${NC}"
        echo ""
        echo "Falls python3-venv fehlt, installiere es mit:"
        echo "  - Linux: sudo apt install python3-venv"
        echo ""
        exit 1
    fi
    echo -e "${GREEN}   ✓ Virtuelle Umgebung erstellt${NC}"
fi
echo ""

# Prüfe ob requirements.txt existiert
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}   ❌ FEHLER: requirements.txt nicht gefunden!${NC}"
    echo ""
    echo "Bist du im richtigen Ordner?"
    echo ""
    exit 1
fi

# Aktiviere virtuelle Umgebung und installiere Pakete
echo -e "${BLUE}[3/4] Installiere benötigte Pakete...${NC}"
echo "   (Dies kann 1-2 Minuten dauern...)"
echo ""
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo -e "${RED}   ❌ Fehler beim Installieren der Pakete${NC}"
    echo ""
    echo "Möglicherweise fehlt eine Internetverbindung?"
    echo ""
    exit 1
fi
echo -e "${GREEN}   ✓ Alle Pakete erfolgreich installiert${NC}"
echo ""

# Erstelle Start-Script
echo -e "${BLUE}[4/4] Erstelle Start-Script...${NC}"
if [ -f "therapiefinder-start.sh" ]; then
    echo "   Start-Script existiert bereits - überspringe"
else
    cat > therapiefinder-start.sh << 'EOF'
#!/bin/bash

# Farben für Fehlerausgabe
RED='\033[0;31m'
NC='\033[0m'

clear

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║       🧘 Therapiefinder Open Source                         ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Starte Anwendung..."
echo ""
echo "Die App öffnet sich automatisch im Browser."
echo "Drücke STRG+C zum Beenden."
echo ""

# Wechsle in das Script-Verzeichnis
cd "$(dirname "$0")"

# Prüfe ob venv existiert
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ FEHLER: Virtuelle Umgebung nicht gefunden!${NC}"
    echo ""
    echo "Bitte führe zuerst ./therapiefinder-install.sh aus."
    echo ""
    read -p "Drücke Enter zum Beenden..."
    exit 1
fi

# Aktiviere virtuelle Umgebung
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ FEHLER: Konnte virtuelle Umgebung nicht aktivieren.${NC}"
    echo ""
    read -p "Drücke Enter zum Beenden..."
    exit 1
fi

# Starte Streamlit
streamlit run app.py
EOF

    chmod +x therapiefinder-start.sh
    echo -e "${GREEN}   ✓ Start-Script erstellt${NC}"
fi
echo ""

echo "══════════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}✅ Installation erfolgreich abgeschlossen!${NC}"
echo ""
echo "══════════════════════════════════════════════════════════════"
echo ""
echo "📋 Nächste Schritte:"
echo ""
echo "   1. Starte das Programm mit: ./therapiefinder-start.sh"
echo "   2. Die App öffnet sich automatisch im Browser"
echo "   3. Gib deine Postleitzahl ein und klicke 'Suche starten'"
echo ""
echo "💡 Tipp: Du kannst therapiefinder-start.sh als Verknüpfung anlegen"
echo "   oder ins Dock/Panel ziehen für einfacheren Zugriff!"
echo ""
echo "══════════════════════════════════════════════════════════════"
echo ""
