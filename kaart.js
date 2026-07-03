/**
 * Leaflet-kaart: laadt de GeoJSON-datalagen (uit concepten.json) en filtert
 * ze op het gekozen concept. Elk kaartpunt toont bij klik een popup met de
 * conceptafbeelding(en) die aan zijn datalaag gekoppeld zijn (via popup.js).
 */
import { buildPopupContent } from "./popup.js";

// Vaste kleur + label per datalaag-bestand, puur voor leesbaarheid op de
// kaart (legenda + marker-kleur). Een nieuwe laag die hier niet in staat
// krijgt een neutrale kleur en een van de bestandsnaam afgeleid label, dus
// dit hoeft niet bijgewerkt te worden om een nieuw concept toe te voegen
// aan bestaande lagen.
const LAAG_STIJL = {
  "data/parkeerplaatsen.geojson": { kleur: "#2a78d6", label: "Parkeerplaatsen" },
  "data/afvalcontainers.geojson": { kleur: "#1baf7a", label: "Ondergrondse afvalcontainers" },
  "data/parkeergarages.geojson": { kleur: "#eda100", label: "Parkeergarages" },
  "data/winkelgevels.geojson": { kleur: "#008300", label: "Winkelgevels" },
  "data/bruggen.geojson": { kleur: "#4a3aa7", label: "Bruggen en viaducten" },
  "data/boulevards.geojson": { kleur: "#e34948", label: "Boulevards" },
  "data/evenementenlocaties.geojson": { kleur: "#e87ba4", label: "Evenementenlocaties" },
};
const STANDAARD_STIJL = { kleur: "#898781", label: null };

function stijlVoorLaag(pad) {
  return LAAG_STIJL[pad] || { kleur: STANDAARD_STIJL.kleur, label: bestandslabel(pad) };
}

function bestandslabel(pad) {
  const naam = pad.split("/").pop().replace(".geojson", "");
  return naam.charAt(0).toUpperCase() + naam.slice(1);
}

let map;
let concepten = [];
let laagNaarConcepten = {};
let laagCache = {};
let actieveLagen = [];
let statusEl;
let resetKnop;
let leegMeldingEl;

export async function initKaart(conceptenData) {
  concepten = conceptenData;
  laagNaarConcepten = bouwLaagIndex(concepten);

  map = L.map("kaart", { renderer: L.canvas() }).setView([52.0799, 4.3113], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>-auteurs (ODbL) &middot; data: gemeente Den Haag',
  }).addTo(map);

  statusEl = document.getElementById("kaart-status");
  resetKnop = document.getElementById("reset-kaart");
  leegMeldingEl = document.getElementById("kaart-leeg-melding");
  resetKnop.addEventListener("click", () => toonAlleLagen());
}

/**
 * Moet aangeroepen worden nadat de kaart-sectie zichtbaar is gemaakt (na
 * `hidden = false`), en vóórdat er lagen getoond/op bounds gepast worden.
 * De kaart is bij initKaart() nog verborgen (display:none), dus Leaflet
 * meet dan een 0x0 container; zonder deze aanroep gebruikt fitBounds()
 * die verouderde afmeting en komt de kaart op een verkeerde zoom/positie
 * terecht (Leaflets eigen window-resize-handler is 200ms getroteld en is
 * te laat voor een fitBounds die direct daarna wordt aangeroepen).
 */
export function verversKaartGrootte() {
  if (map) {
    map.invalidateSize();
  }
}

function bouwLaagIndex(concepten) {
  const index = {};
  for (const concept of concepten) {
    for (const laag of concept.datalagen) {
      if (!index[laag]) index[laag] = [];
      index[laag].push(concept);
    }
  }
  return index;
}

function alleUniekeLagen() {
  const set = new Set();
  concepten.forEach((c) => c.datalagen.forEach((l) => set.add(l)));
  return [...set];
}

async function laadLaag(pad) {
  if (!laagCache[pad]) {
    const resp = await fetch(pad);
    laagCache[pad] = await resp.json();
  }
  return laagCache[pad];
}

async function toonLagen(paden, statusTekst) {
  actieveLagen.forEach((l) => map.removeLayer(l));
  actieveLagen = [];

  const groepen = await Promise.all(
    paden.map(async (pad) => {
      const geojson = await laadLaag(pad);
      const { kleur } = stijlVoorLaag(pad);
      const geoLaag = L.geoJSON(geojson, {
        pointToLayer: (feature, latlng) =>
          L.circleMarker(latlng, {
            radius: 5,
            color: kleur,
            weight: 1,
            fillColor: kleur,
            fillOpacity: 0.75,
          }),
        onEachFeature: (feature, layer) => {
          const gekoppeldeConcepten = laagNaarConcepten[pad] || [];
          const { lat, lng } = layer.getLatLng();
          layer.bindPopup(() => buildPopupContent(gekoppeldeConcepten, lat, lng), { maxWidth: 260 });
        },
      });
      // Veel lagen hebben duizenden punten; clusteren houdt de kaart leesbaar
      // (in plaats van een dichte, ononderscheidbare vlek bij uitzoomen).
      const cluster = L.markerClusterGroup({
        maxClusterRadius: 45,
        iconCreateFunction: (cluster) =>
          L.divIcon({
            html: `<div style="background:${kleur}">${cluster.getChildCount()}</div>`,
            className: "cluster-stip",
            iconSize: L.point(32, 32),
          }),
      });
      cluster.addLayer(geoLaag);
      return cluster;
    })
  );

  groepen.forEach((laag) => {
    laag.addTo(map);
    actieveLagen.push(laag);
  });

  statusEl.textContent = statusTekst;
  resetKnop.hidden = paden.length === alleUniekeLagen().length;

  if (paden.length === 0) {
    leegMeldingEl.hidden = false;
    leegMeldingEl.textContent =
      "Voor dit concept is nog geen datalaag gekoppeld — er zijn nog geen locaties om op de kaart te tonen.";
    toonLegenda([]);
  } else {
    leegMeldingEl.hidden = true;
    toonLegenda(paden);
  }

  const groep = L.featureGroup(actieveLagen);
  if (groep.getLayers().length && groep.getBounds().isValid()) {
    map.fitBounds(groep.getBounds(), { maxZoom: 15, padding: [20, 20] });
  }
}

function toonLegenda(paden) {
  const bestaande = document.querySelector(".laag-legenda");
  if (bestaande) bestaande.remove();

  if (paden.length === 0) return;

  const legenda = L.control({ position: "bottomright" });
  legenda.onAdd = () => {
    const div = L.DomUtil.create("div", "laag-legenda");
    div.innerHTML = paden
      .map((pad) => {
        const { kleur, label } = stijlVoorLaag(pad);
        return `<div><span class="stip" style="background:${kleur}"></span>${label}</div>`;
      })
      .join("");
    return div;
  };
  legenda.addTo(map);
}

export async function toonAlleLagen() {
  await toonLagen(alleUniekeLagen(), "Kansenkaart: alle datalagen");
}

export async function toonKansenkaartVoorConcept(concept) {
  await toonLagen(concept.datalagen, `Kansenkaart voor: ${concept.naam}`);
}
