# 🛠️ Notfallplan: Was tun, wenn das Tool nicht mehr funktioniert?

Dieses Dokument beschreibt, was passiert, wenn therapie.de das Scraping blockiert oder die Webseite so ändert, dass das Tool nicht mehr funktioniert.

---

## 🚨 Szenarien, in denen das Tool ausfallen kann

### 1. **therapie.de ändert die Webseitenstruktur**
**Symptom:** Das Tool findet keine Ergebnisse mehr, obwohl welche existieren sollten.
**Ursache:** therapie.de hat die HTML-Struktur geändert (z.B. neue CSS-Klassen, andere DOM-Elemente).
**Lösung:** Der Code in `scraper_lib.py` muss angepasst werden. Das erfordert technische Kenntnisse.

### 2. **therapie.de blockiert aktiv Scraper**
**Symptom:** Du bekommst Fehlermeldungen wie "403 Forbidden", "Rate Limit Exceeded" oder CAPTCHAs.
**Ursache:** therapie.de hat automatisiertes Crawling erkannt und blockiert (z.B. via IP-Ban, User-Agent-Filtering, CAPTCHAs).
**Lösung:** Technisch sehr schwierig bis unmöglich zu umgehen. Nutze manuelle Alternativen (siehe unten).

### 3. **Rechtliche Konsequenzen**
**Symptom:** therapie.de sendet Abmahnungen oder rechtliche Aufforderungen.
**Ursache:** Sie bestehen auf Einhaltung ihrer AGBs, die automatisiertes Crawling verbieten.
**Lösung:** Projekt einstellen. Manuelle Suche nutzen.

### 4. **Der Maintainer ist weg**
**Symptom:** Das Projekt wird nicht mehr gewartet, Issues bleiben unbeantwortet.
**Ursache:** Ich (der Maintainer) habe keine Zeit mehr / Interesse verloren / bin nicht mehr erreichbar.
**Lösung:** Jemand anderes muss das Projekt forken und weiterführen (siehe "Bus-Faktor-Problem" unten).

---

## 🔧 Sofortmaßnahmen: Was du jetzt tun kannst

### Schritt 1: Prüfe, ob es ein bekanntes Problem ist
1. **GitHub Issues checken:** [https://github.com/PhilGabriel/therapiefinder-opensource/issues](https://github.com/PhilGabriel/therapiefinder-opensource/issues)
2. **Neueste Version holen:** Vielleicht wurde das Problem schon gefixt. `git pull` ausführen oder ZIP neu herunterladen.

### Schritt 2: Eröffne ein Issue (wenn noch keins existiert)
Beschreibe das Problem so detailliert wie möglich:
- Welche Fehlermeldung siehst du?
- Welche Filter hast du verwendet?
- Welche Region/PLZ?
- Screenshot der Fehlermeldung

### Schritt 3: Nutze manuelle Alternativen (siehe unten)
Wenn das Tool nicht mehr funktioniert, musst du auf manuelle Suche zurückgreifen.

---

## 📝 Manuelle Alternativen zur Therapieplatzsuche

Falls das Tool ausfällt, sind das deine Optionen:

### 1. **Manuelle Suche auf therapie.de**
**Wie:**
1. Gehe zu [https://www.therapie.de/psychotherapie](https://www.therapie.de/psychotherapie)
2. Filter setzen (PLZ, Verfahren, etc.)
3. Profile durchklicken
4. Sortiere mental nach "zuletzt aktualisiert" (Datum steht meist im Profil)
5. E-Mail-Adressen manuell rausschreiben

**Vorteil:** Funktioniert immer, kann nicht blockiert werden.
**Nachteil:** Zeitaufwändig, nervig, frustrierend.

### 2. **116 117 – Terminservicestelle**
**Was:** Gesetzliche Krankenkassen haben Anspruch auf Vermittlung eines Erstgesprächs innerhalb von 4 Wochen.
**Wie:**
- Anrufen: **116 117**
- Online: [https://www.116117.de](https://www.116117.de) → "Terminservicestelle"
- Regional unterschiedlich: Manche KVen haben eigene Portale (z.B. [kvno.de](https://www.kvno.de) für NRW)

**Vorteil:** Offizieller Weg, gesetzlicher Anspruch.
**Nachteil:** Nur für Erstgespräche, nicht für die ganze Therapie. Aber ein Erstgespräch kann dir helfen, ins System zu kommen.

### 3. **Kassenärztliche Vereinigung (KV) deines Bundeslandes**
Jedes Bundesland hat eine KV mit eigener Therapeut:innen-Suche. Beispiele:
- **Nordrhein-Westfalen:** [https://arztsuche.kvno.de](https://arztsuche.kvno.de)
- **Bayern:** [https://www.kvb.de/service/patienten/arztsuche](https://www.kvb.de/service/patienten/arztsuche)
- **Berlin:** [https://www.kvberlin.de/fuer-patienten/arztsuche](https://www.kvberlin.de/fuer-patienten/arztsuche)

Google nach "Kassenärztliche Vereinigung [dein Bundesland] Psychotherapeuten-Suche".

### 4. **Kostenerstattungsverfahren**
**Was:** Krankenkasse übernimmt Kosten für Therapeut:in ohne Kassenzulassung.
**Voraussetzungen:**
- Mindestens 5 Absagen von Kassentherapeut:innen (variiert je nach Kasse)
- Antrag bei der Krankenkasse stellen **BEVOR** du die Therapie beginnst

**Vorteil:** Mehr Therapeut:innen verfügbar (auch ohne Kassensitz).
**Nachteil:** Bürokratisch, nicht alle Kassen kooperieren gut, du musst in Vorleistung gehen.

**Anleitungen:**
- [https://www.deutsche-psychotherapeuten-vereinigung.de/patienten/kostenerstattung/](https://www.deutsche-psychotherapeuten-vereinigung.de/patienten/kostenerstattung/)
- Frag deine Krankenkasse nach dem "Kostenerstattungsverfahren §13 Abs. 3 SGB V"

### 5. **Ausbildungsinstitute**
Psychotherapeut:innen in Ausbildung bieten Therapie unter Supervision an.
**Vorteile:** Oft kürzere Wartezeiten, motivierte Therapeut:innen, oft Kassenzulassung.
**Nachteile:** Therapeut:in wechselt nach Abschluss der Ausbildung.

**Wo finden:**
- Google: "Psychotherapie Ausbildungsinstitut [deine Stadt]"
- Beispiele: DVT (Verhaltenstherapie), IfP (Tiefenpsychologie), etc.

### 6. **Psychiatrische Institutsambulanzen (PIA)**
**Was:** Ambulanzen an psychiatrischen Kliniken, die auch Psychotherapie anbieten.
**Für wen:** Oft für schwere Fälle oder Menschen mit eingeschränkter Mobilität.
**Vorteil:** Interdisziplinäres Team, schnellere Termine.

**Wo finden:**
- Google: "Psychiatrische Institutsambulanz [deine Stadt]"
- Oft an Unikliniken oder größeren psychiatrischen Krankenhäusern angegliedert

### 7. **Online-Therapie / Videosprechstunde**
Viele Therapeut:innen bieten Videotherapie an. Das erweitert deinen Suchradius auf ganz Deutschland.

**Plattformen:**
- therapie.de (Filter: "Videosprechstunde")
- [https://www.psychotherapiesuche.de](https://www.psychotherapiesuche.de) (Deutsche Psychotherapeuten Vereinigung)

---

## 🧑‍💻 Technisch versiert? So kannst du das Tool selbst reparieren

Falls du Programmierkenntnisse hast und das Tool selbst reparieren willst:

### Schritt 1: Analysiere das Problem
```bash
# Öffne die Python-Konsole und teste den Scraper manuell
python3
>>> from scraper_lib import scrape_therapists
>>> results = scrape_therapists(zip_code="10115", verfahren="", abrechnung="", angebot="", schwerpunkt="", geschlecht="", terminzeitraum="1", umkreis="10", max_pages=1)
```

Wenn hier ein Fehler kommt, liegt es am Scraper. Wenn es funktioniert, liegt es an Streamlit.

### Schritt 2: Untersuche die HTML-Struktur
```bash
# Öffne therapie.de im Browser
# Rechtsklick → "Element untersuchen"
# Prüfe, ob die CSS-Klassen noch stimmen (z.B. `class="contact-mail"`)
```

Vergleiche mit dem Code in `scraper_lib.py`, Zeile 140-151 (E-Mail-Extraktion).

### Schritt 3: Passe den Code an
- Ändere die CSS-Selektoren in `scraper_lib.py` entsprechend der neuen HTML-Struktur
- Teste lokal, ob es wieder funktioniert
- Öffne einen Pull Request auf GitHub

### Schritt 4: Dokumentiere die Änderung
Schreibe in den Pull Request oder ins Issue, was du geändert hast und warum.

---

## 🚌 Das Bus-Faktor-Problem

**Was ist das?**
Der "Bus-Faktor" beschreibt, wie viele Menschen von einem Bus überfahren werden müssten, damit ein Projekt stirbt. Bei diesem Projekt ist der Bus-Faktor **1** (ich, der Maintainer).

**Warum ist das ein Problem?**
Wenn ich aus irgendeinem Grund das Projekt nicht mehr pflege (keine Zeit, kein Interesse, gesundheitliche Gründe, etc.), gibt es niemanden, der es weiterführt.

**Was kannst du tun?**
1. **Forke das Projekt auf GitHub:** So hast du eine eigene Kopie, die du weiterentwickeln kannst
2. **Trage zum Projekt bei:** Pull Requests, Issues, Dokumentation – je mehr Menschen involviert sind, desto robuster wird das Projekt
3. **Werde Co-Maintainer:** Wenn du regelmäßig beiträgst, können wir über Co-Maintainer-Rechte sprechen

**So forkst du das Projekt:**
1. Gehe zu [https://github.com/PhilGabriel/therapiefinder-opensource](https://github.com/PhilGabriel/therapiefinder-opensource)
2. Klicke auf "Fork" (oben rechts)
3. Du hast jetzt eine eigene Kopie unter deinem GitHub-Account
4. Änderungen kannst du dort vornehmen und auch veröffentlichen

---

## 🆘 Wenn gar nichts mehr geht

Falls das Tool nicht funktioniert UND keine der Alternativen hilft:

### Sofortmaßnahmen:
- **116 117** anrufen (Terminservicestelle)
- **Telefonseelsorge:** 0800 / 111 0 111 oder 0800 / 111 0 222 (kostenlos, anonym, 24/7)
- **Im Notfall:** 112 oder nächste psychiatrische Notaufnahme

### Selbsthilfegruppen & Foren:
- Reddit: r/de, r/depression (auf Deutsch)
- [https://www.nakos.de](https://www.nakos.de) (Nationale Kontakt- und Informationsstelle zur Anregung und Unterstützung von Selbsthilfegruppen)

### Patientenberatung:
- **Unabhängige Patientenberatung Deutschland:** 0800 / 011 77 22 (kostenlos)
- [https://www.patientenberatung.de](https://www.patientenberatung.de)

**Du bist nicht allein. Es gibt Wege. Und du bist es wert, Hilfe zu bekommen. Gib nicht auf. ❤️**

---

## 📌 Zusammenfassung

| Szenario | Lösung |
|----------|--------|
| **Tool findet keine Ergebnisse** | GitHub Issue checken, manuelle Suche nutzen |
| **therapie.de blockiert Scraper** | Manuelle Suche, 116 117, Kostenerstattungsverfahren |
| **Maintainer ist inaktiv** | Projekt forken, selbst weiterführen |
| **Technischer Fehler** | Issue auf GitHub öffnen mit Details |
| **Ich brauche JETZT Hilfe** | 116 117, Telefonseelsorge, Notaufnahme |

**Wichtigste Erkenntnis:**
Dieses Tool ist eine Krücke, keine Lösung. Die echten Lösungen sind politisch (siehe [POLITIK.md](POLITIK.md)) und strukturell (mehr Kassensitze, zentrale Datenbank, Abschaffung der Kassensitzpflicht). Bis dahin: Nutze alle Wege, die dir zur Verfügung stehen.
