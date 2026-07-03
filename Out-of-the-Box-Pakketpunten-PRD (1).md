# PRD --- Out-of-the-Box Pakketpunten Viewer

## Productvisie

Een inspirerende GIS- en visualisatietool voor innovatieve pakketpunten
in Den Haag. De kaart toont geen waarheid, maar mogelijkheden.

## Doelgroep en doel

-   **Doelgroep:** beleidsmakers bij de gemeente die stakeholders mee
    willen krijgen om plaatsing van pakketpunten in de publieke ruimte
    mogelijk te maken.
-   **Doel:** stakeholders over de streep krijgen. De veelgehoorde
    weerstand is: "pakketpunten zijn lelijk en nemen te veel ruimte in
    in de schaarse publieke ruimte." De tool weerlegt dit beeld met
    aantrekkelijke, ruimte-efficiënte concepten op reële locaties in
    Den Haag.

## Ruimtelijke strategieën

1.  De hoogte in --- Verticale pakketkluis
2.  De grond in --- Ondergrondse pakketkluis
3.  Schuiven in tijd --- Mobiele pakketkluis
4.  Schuiven in functie --- Pakketboom en pakketpergola
5.  Schuiven in eigendom --- Gevelintegratie
6.  Schuiven in lucht --- Zwevende pakketkluis
7.  Schuiven in perceptie --- Spiegelpakketkluis

## Concepten

### Mobiele groene pakketkluis

-   Op parkeerplaatsen, evenementen en boulevards
-   Verplaatsbaar op wielen
-   Groene gevels en dakbeplanting
-   Afbeelding: `Afbeeldingen/groene_mobiele_pakketkluis.png`

### Ondergrondse pakketkluis

-   Compacte afhaalzuil
-   Ondergrondse opslag en lift
-   Koppeling met afvalcontainers
-   Afbeelding: `Afbeeldingen/ondergrondse_pakketkluis.png`

### Ondergrondse pakketgarage

-   In bestaande parkeergarages
-   Grote capaciteit
-   Afbeelding: `Afbeeldingen/Parkeergarage.png`

### Verticale pakketkluis

-   Volledige gevelhoogte
-   Intern transportsysteem
-   Afbeelding: `Afbeeldingen/verticale_pakketkluis.png`

### Zwevende pakketkluis

-   Onder bruggen en viaducten
-   Geen beslag op maaiveld
-   Afbeelding: `Afbeeldingen/zwevend_pakketpunt.png`

### Spiegelpakketkluis

-   Scheveningen, Kijkduin, Lange Voorhout
-   Reflecteert omgeving en functioneert als kunstobject
-   Afbeelding: `Afbeeldingen/spiegel_pakketpunt.png`

### Pop-up pakketpunt

-   Tijdelijk pakketpunt bij evenementen en tijdelijke locaties (bijv.
    De Parade in het Westbroekpark)
-   Thematische vormgeving passend bij het evenement
-   Snel op- en afbouwbaar
-   Afbeelding: `Afbeeldingen/popup_pakketpunt.png`

### Seizoensgebonden pakketpunt

-   Tijdelijke plaatsing in het seizoen, bijv. zomers op de boulevard
    van Scheveningen of Kijkduin
-   Mobiel en duurzaam: verplaatsbaar, groene gevel
-   Afbeelding: `Afbeeldingen/seizoensgebonden_pakketpunt.png`

### Earthship-pakketpunt

-   Gebouwd uit natuurlijke en circulaire materialen
-   Organische architectuur
-   Groen dak en passieve uitstraling
-   Afbeelding: `Afbeeldingen/earthship_pakketkluis.png`

### Architectonisch pakketpunt

-   Pakketkluis integraal opgenomen in het architectonisch ontwerp van
    nieuwbouw bij gebiedsontwikkeling
-   Onderdeel van gevel en plint vanaf de tekentafel, geen toevoeging
    achteraf
-   Afbeelding: `Afbeeldingen/architectonisch_pakketpunt_gebiedsontwikkeling.png`

### Park-pakketpunt

-   Esthetisch aantrekkelijk pakketpunt voor in een park
-   Ambachtelijk betegeld, functioneert als sieraad in de groene ruimte
-   Afbeelding: `Afbeeldingen/park_pakketpunt_betegeld.png`

### Trappen-pakketkluis

-   Pakketkluis verwerkt in de trappartij van een plein
-   Dubbel ruimtegebruik: de trappen dienen in de zomer als zitplek
-   Afbeelding: `Afbeeldingen/trappen_plein_zomer_pakketkluis.png`

## Applicatiemodi

### Conceptviewer

-   Conceptbibliotheek: toont alleen de afbeeldingen van de concepten;
    naam en uitleg zijn al in de afbeelding opgenomen
-   Koppeling naar de kaart: bij elk concept een knop "Toon mij waar in
    Den Haag dit mogelijk is", die de Kansenkaart opent gefilterd op de
    bijbehorende locaties van dat concept

### Kansenkaart

Datasets: - Parkeerplaatsen → mobiele pakketpunten - Ondergrondse
afvalcontainers → ondergrondse pakketkluizen - Parkeergarages →
pakketgarages - Winkelgevels → verticale pakketkluizen - Bruggen en
viaducten → zwevende pakketkluizen - Boulevards → spiegelpakketkluizen
en seizoensgebonden pakketpunten - Evenementenlocaties → pop-up
pakketpunten

Meerdere concepten mogen aan één locatie(type) gekoppeld zijn; de
koppeling is nadrukkelijk niet één-op-één. Zo hoort de mobiele groene
pakketkluis bij parkeerplaatsen, evenementenlocaties én boulevards.

Interactie: een klik op een kaartpunt toont een popup met de
conceptafbeelding. Bij meerdere gekoppelde concepten kan de gebruiker
in de popup door de conceptafbeeldingen bladeren. De popup bevat een
link "Bekijk deze plek in Street View" die Google Street View opent op
de coördinaten van het punt (geen API nodig, alleen een URL).

### Databronnen (openbare data)

| Dataset | Bron |
|---|---|
| Parkeerplaatsen | [Parkeerplekken Den Haag](https://ckan.dataplatform.nl/dataset/parkeerplekken) (Dataplatform Den Haag, o.a. GeoJSON) |
| Ondergrondse afvalcontainers | [Bakken Den Haag](https://den-haag-opendata.opendatasoft.com/explore/assets/bakken/view/) (ORAC's, Open Data Den Haag) |
| Parkeergarages | Parkeergarages-dataset op [Dataplatform Den Haag](https://denhaag.dataplatform.nl/), aangevuld met RDW Open Parkeerdata (capaciteit) |
| Winkelgevels | BAG-panden met gebruiksdoel winkelfunctie via [PDOK BAG](https://www.pdok.nl/ogc-webservices/-/article/basisregistratie-adressen-en-gebouwen-ba-1) |
| Bruggen en viaducten | OpenStreetMap via Overpass API (`man_made=bridge` / `bridge=yes` binnen gemeentegrens Den Haag) |
| Boulevards | Geen kant-en-klare dataset; handmatig intekenen of OpenStreetMap (Scheveningen, Kijkduin) |
| Evenementenlocaties | [Evenementen Den Haag](https://ckan.dataplatform.nl/dataset/evenementendenhaag) — evenementenvergunningen gemeente Den Haag (CSV, KML, GPKG, shapefile) |

### Voorbeeldlocaties

Locaties die in een conceptafbeelding figureren, zijn gegarandeerd
aanwezig in de bijbehorende datalaag. Levert de open bron ze niet, dan
worden ze handmatig als curated locatie toegevoegd. In elk geval:

-   Westbroekpark (De Parade) → evenementenlocaties, bij het pop-up
    pakketpunt

### Licenties en attributie

De viewer vermeldt de bronnen conform hun voorwaarden: "© OpenStreetMap
contributors (ODbL)" voor OSM-data en bronvermelding gemeente Den Haag
voor de gemeentelijke open data.

### Coördinatenstelsel

De bronnen gebruiken verschillende stelsels: gemeentelijke data komt in
RD New (EPSG:28992), OpenStreetMap in WGS84 (EPSG:4326). Alle data
wordt bij de data-voorbereiding eenmalig geconverteerd naar WGS84
(EPSG:4326) en opgeslagen als GeoJSON. Dit is de standaard voor
webkaartbibliotheken (MapLibre/Leaflet), waardoor de viewer zelf geen
conversies hoeft uit te voeren. Conversie gebeurt in de datapijplijn
met een bewezen transformatie (bijv. GDAL/ogr2ogr of pyproj).

## Techniek

-   **Platform:** webapp, plain HTML/JS (geen framework, geen
    build-stap)
-   **Kaartbibliotheek:** Leaflet
-   **Structuur:** concepten en datalagen zijn config-gedreven (één
    manifest, bijv. `concepten.json`, met per concept naam, afbeelding
    en datalaag), zodat nieuwe concepten toegevoegd kunnen worden
    zonder codewijziging; code modulair opgedeeld (kaart, bibliotheek,
    popup gescheiden)
-   **Data:** statische data-snapshot; alle bronnen worden in de
    datapijplijn eenmalig opgehaald, gefilterd op de gemeente Den Haag,
    geconverteerd naar WGS84 en als GeoJSON meegeleverd met de app.
    Geen live API-koppelingen in de viewer.
-   **Hosting:** Railway

## Toekomstige uitbreidingen (volgende fase)

-   **Locatievisualisatie:** de gebruiker klikt een locatie op de kaart
    aan en er wordt een 2D-afbeelding gegenereerd van het concept op
    die specifieke locatie (bijv. op basis van straatbeeld, zie
    Mapillary-integratie)
-   **Eigen concepten via LLM:** de gebruiker verzint met een
    LLM-koppeling een nieuw concept; het LLM genereert daarbij ook een
    bijpassende datalaag op de kaart (welk locatietype past bij dit
    concept en welke bron levert die locaties). Hoeft alleen lokaal
    (bij de beheerder) te werken, niet in de gehoste webapp; het
    resultaat wordt als nieuwe snapshot-laag meegeleverd
-   Mapillary-integratie
-   AI-locatieadvies
-   Datafiltering per bron: kansrijkheidscriteria per dataset (bijv.
    breedte, ligging, afstand tot woningen), zodat de kansenkaart geen
    puntenwolk wordt maar alleen kansrijke locaties toont
-   Scenariovergelijkingen
-   Participatie-export
