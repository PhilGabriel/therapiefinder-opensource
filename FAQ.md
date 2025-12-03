# ❓ Häufig gestellte Fragen (FAQ)

Diese FAQ beantwortet ehrlich die wichtigsten Fragen zu diesem Projekt – ohne Beschönigung, aber mit konstruktiven Lösungsansätzen.

---

## 1. Hilft das Tool wirklich, einen Therapieplatz zu finden?

**Kurze Antwort:** Es hilft, schneller an Kontaktinformationen zu kommen. Einen Platz garantieren kann es nicht.

**Lange Antwort:**
Dieses Tool automatisiert den Prozess, Therapeut:innen-Profile zu durchsuchen und E-Mail-Adressen zu extrahieren. Es spart dir Zeit beim manuellen Durchklicken von therapie.de. **Aber:** Am Ende musst du selbst die E-Mails schreiben oder anrufen – und das ist oft der härteste Teil.

Die Therapieplatz-Situation in Deutschland ist strukturell kaputt. Dieses Tool ist ein Pflaster, keine Heilung. Es macht den Prozess *etwas* erträglicher, aber die eigentliche Arbeit (anfragen, warten, Absagen verkraften, weitermachen) bleibt bei dir.

**Was das Tool kann:**
- Therapeut:innen nach Aktualität sortieren
- E-Mail-Adressen automatisch extrahieren
- Dir eine Liste geben, die du systematisch abarbeiten kannst

**Was das Tool nicht kann:**
- Dir garantieren, dass jemand freie Plätze hat
- Die Wartezeit verkürzen
- Dir die emotionale Last der Suche abnehmen

---

## 2. Bedeutet "zuletzt aktualisiert" = freie Plätze?

**Nein. Und das ist wichtig zu verstehen.**

Ein kürzlich aktualisiertes Profil bedeutet nur, dass jemand das Profil gepflegt hat. Das kann verschiedene Gründe haben:
- Urlaubsabwesenheit eingetragen
- Neue Schwerpunkte hinzugefügt
- Kontaktdaten geändert
- Routine-Update ohne Bezug zur Kapazität

**Warum sortieren wir dann danach?**
Weil ein gepflegtes Profil ein Indiz für Aktivität ist. Therapeut:innen, die ihr Profil seit 3 Jahren nicht angefasst haben, sind oft nicht mehr erreichbar oder haben die Praxis geschlossen. Die Sortierung hilft dir, *aktive* Profile zuerst zu sehen – nicht Profile mit freien Plätzen.

**Was du tun solltest:**
- Nutze die Sortierung als Startpunkt, nicht als Garantie
- Schreibe trotzdem auch Profile weiter unten an
- Setze deine Erwartungen realistisch

---

## 3. Ist das Scraping von therapie.de legal?

**Ehrliche Antwort:** Es bewegt sich in einer Grauzone.

**Rechtliche Einordnung:**
- **DSGVO:** Die Daten auf therapie.de sind von den Therapeut:innen selbst öffentlich gestellt. Das Tool speichert keine Daten dauerhaft, sondern zeigt sie dir nur an. Du lädst die CSV-Datei herunter – dann liegt die Verantwortung bei dir.
- **AGBs von therapie.de:** Möglicherweise verbieten die AGBs automatisiertes Crawling. Ich habe dieses Tool gebaut, weil ich selbst betroffen bin und die Situation unerträglich finde. Das macht es nicht zwingend legal.
- **Urheberrecht:** Die Daten selbst (Namen, E-Mail-Adressen) sind nicht urheberrechtlich geschützt. Die *Struktur* der Webseite schon – aber wir kopieren die Webseite nicht, sondern extrahieren nur Daten.

**Was passiert, wenn therapie.de das Tool blockiert?**
Siehe [CONTINGENCY.md](CONTINGENCY.md) für Alternativen. Kurz gesagt: Du kannst die Suche dann wieder manuell machen. Dieses Tool ist eine Krücke, kein Recht.

**Meine Position:**
Ich glaube, dass Menschen in psychischen Krisen ein moralisches Recht haben, effizient nach Hilfe zu suchen. Die Tatsache, dass wir solche Tools brauchen, ist ein Versagen des Gesundheitssystems. Aber ja, rechtlich ist das heikel. Nutze das Tool auf eigene Verantwortung.

---

## 4. Was passiert, wenn therapie.de die Webseite ändert oder das Scraping blockiert?

**Dann funktioniert das Tool nicht mehr.**

Dieses Projekt hat einen **Bus-Faktor von 1** – also ich, der Maintainer. Wenn therapie.de die Struktur ihrer Webseite ändert, muss der Code angepasst werden. Wenn sie aktiv Scraper blockieren (z.B. via Rate Limiting, CAPTCHAs, IP-Bans), kann das Tool nicht mehr funktionieren.

**Was du tun kannst:**
1. **Lies [CONTINGENCY.md](CONTINGENCY.md)** – dort stehen alternative Suchstrategien
2. **Fork das Projekt auf GitHub** – wenn du technische Kenntnisse hast, kannst du es selbst reparieren
3. **Öffne ein Issue auf GitHub** – vielleicht springt jemand ein
4. **Nutze offizielle Wege:** 116 117, Kassenärztliche Vereinigung, Kostenerstattungsverfahren

**Warum gibt es keine Community?**
Weil ich das Projekt alleine gebaut habe und nicht aktiv Community-Building betreibe. Das ist ein Schwachpunkt. Wenn du helfen willst: Pull Requests sind willkommen.

---

## 5. Woher weiß ich, ob das Tool überhaupt geholfen hat?

**Gar nicht. Und das ist ein Problem.**

Ich habe keine Analytics, kein Tracking, keine Datenbank. Das ist gut für deine Privatsphäre, aber schlecht für Wirksamkeitsmessung. Ich weiß nicht:
- Wie viele Menschen das Tool nutzen
- Ob jemand dadurch einen Platz gefunden hat
- Welche Features am hilfreichsten sind

**Was du tun kannst:**
- **GitHub-Star geben:** Wenn dir das Tool geholfen hat (oder auch nur ein bisschen geholfen hat), lass einen ⭐ auf GitHub da. Das ist die einzige Metrik, die ich habe.
- **Issue öffnen:** Teile deine Erfahrung – positiv oder negativ. Das hilft mir, das Tool zu verbessern.
- **Mund-zu-Mund-Propaganda:** Wenn du jemanden kennst, der einen Platz sucht, erzähl von diesem Tool.

---

## 6. Kenne ich schon alle anderen Wege, um an einen Therapieplatz zu kommen?

**Wahrscheinlich nicht. Hier sind die wichtigsten Alternativen:**

### 🆘 **116 117 – Terminservicestelle**
- **Was ist das?** Der ärztliche Bereitschaftsdienst vermittelt innerhalb von 4 Wochen ein Erstgespräch (gesetzliche Pflicht!)
- **Für wen?** Gesetzlich Versicherte
- **Wie?** Anrufen (116 117) oder online über die KV-Terminservicestelle deines Bundeslandes
- **Link:** [https://www.116117.de](https://www.116117.de)

### 💶 **Kostenerstattungsverfahren**
- **Was ist das?** Die Krankenkasse übernimmt die Kosten für eine:n Therapeut:in ohne Kassenzulassung, wenn du nachweisen kannst, dass du keinen Kassenplatz findest
- **Für wen?** Gesetzlich Versicherte, die mindestens 5 Absagen nachweisen können (Anforderungen variieren je nach Kasse)
- **Wie?** Absagen sammeln, Antrag bei der Krankenkasse stellen, Therapeut:in ohne Kassenzulassung suchen
- **Wichtig:** Erst den Antrag stellen, dann die Therapie beginnen!

### 🏥 **Psychiatrische Institutsambulanzen (PIA)**
- **Was ist das?** Ambulanzen an psychiatrischen Kliniken, die auch Therapie anbieten
- **Vorteil:** Oft kürzere Wartezeiten, interdisziplinäres Team
- **Nachteil:** Meist nur für schwere Fälle oder Menschen mit geringer Mobilität

### 🎓 **Ausbildungsinstitute**
- **Was ist das?** Psychotherapeut:innen in Ausbildung bieten Therapie unter Supervision an
- **Vorteil:** Oft kürzere Wartezeiten, motivierte Therapeut:innen, günstiger oder Kassenzulassung
- **Nachteil:** Therapeut:in wechselt nach Abschluss der Ausbildung

### 🌐 **Online-Therapie / Videosprechstunde**
- Viele Therapeut:innen bieten inzwischen Videotherapie an – das erweitert deinen Suchradius deutschlandweit

**Nutze dieses Tool nicht als ersten Weg – nutze es parallel zu den offiziellen Strukturen.**

---

## 7. Warum steht hier ein politischer Appell? Ändert das was?

**Kurze Antwort:** Wahrscheinlich nicht. Aber ich musste ihn loswerden.

**Lange Antwort:**
Die README dieses Tools ist nicht der richtige Ort, um politische Forderungen zu stellen. Das weiß ich. Aber ich bin frustriert, und dieses Projekt ist meine Art, mit dieser Frustration umzugehen.

**Die eigentlichen Adressaten meiner Wut:**
- **Gesetzgeber:** Die Kassensitzpflicht sorgt dafür, dass es künstlich zu wenige Kassenplätze gibt
- **Krankenkassen:** Die intransparente Zulassungspraxis verschärft das Problem
- **Kassenärztliche Vereinigungen:** Lobby-Interessen über Patientenwohl

**Was wirklich helfen würde:**
- Abschaffung der Kassensitzpflicht (oder massive Erhöhung der Sitze)
- Zentrale, anonyme Datenbank für freie Therapieplätze
- Bessere Vergütung für Kassensitze (damit mehr Therapeut:innen Kassenpatienten nehmen)

**Was du tun kannst:**
Wenn du politisch aktiv werden willst, lies [POLITIK.md](POLITIK.md). Dort findest du konkrete Ansprechpartner, Musterbriefe und Forderungen. Das ist effektiver als mein Rant in der README.

---

## 8. Ich finde das Tool nicht hilfreich / Es funktioniert nicht bei mir. Was jetzt?

**Das tut mir leid.** Ernsthaft.

Dieses Tool ist eine Krücke, die ich für mich selbst gebaut habe. Dass andere es nutzen wollen, freut mich – aber ich kann nicht garantieren, dass es für jeden funktioniert.

**Was du tun kannst:**
1. **Öffne ein Issue auf GitHub** mit Details zu deinem Problem (welcher Fehler? Welche Filter? Welche Region?)
2. **Lies [CONTINGENCY.md](CONTINGENCY.md)** für alternative Suchstrategien
3. **Nutze die offiziellen Wege:** 116 117, Kassenärztliche Vereinigung, Kostenerstattungsverfahren
4. **Frag in Selbsthilfegruppen:** Oft haben andere Betroffene Tipps für deine Region

**Was ich nicht kann:**
- Dir persönlich bei der Suche helfen
- Garantieren, dass das Tool immer funktioniert
- Einen Therapieplatz für dich finden

**Aber ich wünsche dir von Herzen, dass du Hilfe findest. Du bist es wert. Gib nicht auf. ❤️**

---

## 9. Kann ich zum Projekt beitragen?

**Ja! Bitte!**

Dieses Projekt hat einen Bus-Faktor von 1 (ich). Je mehr Menschen mithelfen, desto robuster wird es.

**Wie du helfen kannst:**
- **Code:** Pull Requests für neue Features, Bugfixes, Code-Verbesserungen
- **Dokumentation:** Rechtschreibfehler korrigieren, Anleitungen verbessern, Übersetzungen
- **Testing:** Probiere das Tool aus und berichte über Bugs oder fehlende Features
- **Spread the word:** Erzähl anderen von diesem Tool (aber bitte verantwortungsvoll)

**Was ich NICHT will:**
- Kommerzialisierung dieses Tools
- Tracking oder Analytics
- Features, die therapie.de schädigen (z.B. aggressive Scraping-Raten)

Pull Requests sind willkommen. Öffne vorher ein Issue, wenn du größere Änderungen planst.

---

## 10. Wo finde ich Hilfe, wenn ich nicht weiterkomme?

**Bei der Installation:**
Lies [INSTALLATION.md](INSTALLATION.md) – dort sind häufige Probleme und Lösungen dokumentiert.

**Bei technischen Problemen:**
Öffne ein Issue auf GitHub: [https://github.com/PhilGabriel/therapiefinder-opensource/issues](https://github.com/PhilGabriel/therapiefinder-opensource/issues)

**Bei der Therapieplatzsuche:**
- **116 117** (Terminservicestelle)
- **Telefonseelsorge:** 0800 / 111 0 111 oder 0800 / 111 0 222 (kostenlos, anonym, 24/7)
- **Im Notfall:** 112 oder nächste psychiatrische Notaufnahme

**Du bist nicht allein. Es gibt Hilfe. Und du bist es wert, sie zu bekommen. ❤️**
