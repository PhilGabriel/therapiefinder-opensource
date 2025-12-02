# Dockerfile für den Therapiefinder Open Source

# Nutze ein kleines Python-Image als Basis. 
# python:3.9-slim-buster ist eine gute Wahl für schlanke Images.
FROM python:3.9-slim-buster

# Lege das Arbeitsverzeichnis im Container fest.
WORKDIR /app

# Kopiere die requirements.txt in den Container und installiere die Abhängigkeiten.
# Dies ist ein separater Schritt, damit Docker die Abhängigkeiten cachen kann.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Anwendungscodes in das Arbeitsverzeichnis.
COPY . .

# Öffne Port 8501 im Container, den Streamlit standardmäßig nutzt.
EXPOSE 8501

# Definiere den Befehl, der ausgeführt wird, wenn der Container startet.
# Streamlit soll die app.py ausführen und auf allen verfügbaren Netzwerkschnittstellen lauschen (0.0.0.0).
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
