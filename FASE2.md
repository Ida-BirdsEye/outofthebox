# Fase 2 — Toekomstige functionaliteiten

Uitwerking van de twee volgende-fase-functies uit de PRD. Elke functie
heeft een eigen prompt die later aan Claude Code gevoerd kan worden.
Voorwaarde: fase 1 t/m 4 uit `BOUWPLAN.md` zijn af en de app draait op
Railway. Functie 1 wordt als eerste uitgewerkt.

---

## Functie 1 — Locatievisualisatie (in de gehoste webapp)

**Doel:** een stakeholder klikt een locatie op de kaart aan en ziet een
gegenereerde 2D-afbeelding van het concept op die specifieke locatie.
Dit is het overtuigingsmoment: het concept in de eigen straat.

**Draait:** in de gehoste webapp op Railway. Vereist een kleine
backend; de rest van de app blijft statisch.

**Tussenstap (al in fase 1 gebouwd):** de popup bevat een Street
View-link op de coördinaten van het punt, zodat stakeholders de plek
alvast echt kunnen bekijken. Deze functie vervangt dit passieve kijken
door het concept ín dat straatbeeld te tonen.

### Prompt voor Claude Code

> Breid de viewer uit met locatievisualisatie:
>
> 1. **UI** — in de popup van een kaartpunt komt een knop "Visualiseer
>    op deze locatie". Na klikken: laadstatus, daarna de gegenereerde
>    afbeelding in de popup, met downloadknop. Nette foutmelding als
>    genereren mislukt.
> 2. **Backend** — voeg een klein server-endpoint toe (op de bestaande
>    Railway-app) dat de beeldgeneratie-API aanroept. De API-key staat
>    server-side als environment variable, nooit in de frontend.
> 3. **Beeldinput** — bouw de generatieprompt op uit: de
>    conceptafbeelding, het concepttype, en context van de locatie
>    (adres/omgevingstype via reverse geocoding; optioneel een
>    Mapillary-straatbeeld van de dichtstbijzijnde positie als
>    referentie, met bronvermelding).
> 4. **Kostenbeheersing** — cache resultaten per combinatie
>    locatie+concept (eenmaal gegenereerd wordt hergebruikt) en stel
>    een rate limit in per bezoeker.

### Acceptatiecriteria

- Klik → beeld binnen acceptabele wachttijd, met zichtbare laadstatus
- Herhaalde klik op dezelfde locatie+concept is direct (cache)
- API-key niet zichtbaar in de frontend
- Werkt voor alle concepten met een datalaag

### Consequentie voor de techniek

De PRD-regel "geen live API-koppelingen in de viewer" vervalt deels in
fase 2: er komt één backend-endpoint voor beeldgeneratie bij. De
datalagen blijven statische snapshots.

---

## Functie 2 — Eigen concepten via LLM (lokaal)

**Doel:** de beheerder verzint met een LLM-koppeling een nieuw concept;
het resultaat (tekst + afbeelding + datalaag) wordt als snapshot aan de
app toegevoegd zonder codewijziging.

**Draait:** alleen lokaal bij de beheerder, als CLI-tool. Niet in de
gehoste webapp.

### Prompt voor Claude Code

> Bouw een lokale CLI-tool (`nieuw-concept/`) die op basis van een
> ideebeschrijving in natuurlijke taal een compleet nieuw concept
> toevoegt aan de viewer. De tool doet vier dingen:
>
> 1. **Concepttekst** — roept de Claude API aan en genereert:
>    conceptnaam en 2-3 kenmerken, in dezelfde stijl als de bestaande
>    concepten in de PRD.
> 2. **Conceptafbeelding** — genereert via een beeldgeneratie-API een
>    afbeelding in de stijl van de bestaande afbeeldingen in
>    `Afbeeldingen/`: fotorealistisch, Haagse setting, het pakketpunt
>    prominent met opschrift "PAKKETPUNT" en blad-logo, mensen in
>    gebruikssituatie. Naam en uitleg van het concept zichtbaar in het
>    beeld (conform conceptbibliotheek-eis uit de PRD).
> 3. **Datalaag** — laat de LLM een passend locatietype en bron
>    voorstellen (bestaande dataset uit de PRD-bronnentabel, een
>    Overpass-query, of handmatige invoer), voert die uit via de
>    bestaande datapijplijn (filteren op Den Haag, conversie naar
>    WGS84, GeoJSON in `data/`).
> 4. **Registratie** — voegt het concept toe aan `concepten.json`.
>
> De tool toont vóór het wegschrijven een preview (tekst, afbeelding,
> aantal locaties in de datalaag) en vraagt om bevestiging. API-keys
> via een lokaal `.env`-bestand, dat niet in git komt.

### Acceptatiecriteria

- Eén commando, van idee tot zichtbaar concept in de lokale app
- Menselijke bevestigingsstap vóór wegschrijven
- Geen codewijziging in de viewer nodig; alleen nieuwe bestanden in
  `data/`, `Afbeeldingen/` en een regel in `concepten.json`
