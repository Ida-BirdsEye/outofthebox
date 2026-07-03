# Bouwplan — Out-of-the-Box Pakketpunten Viewer

Instructie voor Claude Code: lees eerst `Out-of-the-Box-Pakketpunten-PRD (1).md`
volledig. Bouw de app in onderstaande fasen, één fase per keer. Stop na elke
fase zodat de output gereviewd kan worden. Vraag bij twijfel eerst.

## Fase 1 — Datapijplijn

Schrijf een Python-script (`pijplijn/`) dat per databron uit de PRD-tabel:

1. de data ophaalt (download of API-call)
2. filtert op de gemeente Den Haag
3. converteert naar WGS84 / EPSG:4326 (met pyproj of GDAL/ogr2ogr)
4. wegschrijft als GeoJSON in `data/`

Bronnen (zie PRD-sectie "Databronnen" voor links):

- Parkeerplekken — Dataplatform Den Haag (CKAN)
- Ondergrondse afvalcontainers (ORAC's) — Bakken Den Haag
- Parkeergarages — Dataplatform Den Haag
- Winkelgevels — BAG-panden met gebruiksdoel winkelfunctie via PDOK
- Bruggen en viaducten — OpenStreetMap via Overpass API
  (`man_made=bridge` / `bridge=yes` binnen gemeentegrens Den Haag)
- Boulevards — geen dataset; teken handmatig in (Scheveningen, Kijkduin)
  of haal uit OSM
- Evenementenlocaties — Evenementen Den Haag (CKAN)

Voeg daarnaast de voorbeeldlocaties uit de PRD-sectie
"Voorbeeldlocaties" toe als curated locaties wanneer de bron ze niet
levert (in elk geval: Westbroekpark → evenementenlocaties).

**Reviewmoment:** elk GeoJSON-bestand wordt visueel gecontroleerd
(bijv. geojson.io): aantallen plausibel, punten liggen in Den Haag.

## Fase 2 — Conceptmanifest

Genereer `concepten.json` met per concept (9 stuks, zie PRD-sectie
"Concepten"):

- naam
- pad naar afbeelding in `Afbeeldingen/`
- gekoppelde datalagen (meerdere lagen per concept mogelijk; de
  koppeling is nadrukkelijk niet één-op-één, zie PRD-sectie "Kansenkaart")

## Fase 3 — Webapp

Plain HTML/JS, geen framework, geen build-stap. Leaflet via CDN.
Modulaire opbouw:

- `index.html`
- `kaart.js` — Leaflet-kaart, laadt GeoJSON-lagen, filtert
- `bibliotheek.js` — conceptbibliotheek
- `popup.js` — popup-inhoud bij klik op kaartpunt

Alles gedreven door `concepten.json`: een nieuw concept toevoegen mag
geen codewijziging vragen.

Functionele eisen (uit de PRD):

- Conceptbibliotheek toont alleen de conceptafbeeldingen (naam en
  uitleg zitten in de afbeelding)
- Per concept een knop "Toon mij waar in Den Haag dit mogelijk is" die
  de kansenkaart opent, gefilterd op de datalagen van dat concept
- Klik op een kaartpunt toont een popup met de conceptafbeelding; bij
  meerdere gekoppelde concepten kan de gebruiker door de afbeeldingen
  bladeren
- De popup bevat een link "Bekijk deze plek in Street View":
  `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lng}`
  (opent in nieuw tabblad)
- Attributieregel: "© OpenStreetMap contributors (ODbL)" en
  bronvermelding gemeente Den Haag

**Reviewmoment:** lokaal testen (`python -m http.server`), alle negen
concepten nalopen.

## Fase 4 — Deploy

Minimale static-serve setup voor Railway (bijv. Caddy of een klein
Node/Python-servertje) en deployen.

## Buiten scope (volgende fase, niet nu bouwen)

- Eigen concepten via LLM (lokale pijplijn)
- Locatievisualisatie (2D-afbeelding genereren op aangeklikte locatie)
- Datafiltering op kansrijkheid
