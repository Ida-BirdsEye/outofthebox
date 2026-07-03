/**
 * Conceptbibliotheek: toont per concept de afbeelding met titel en een
 * korte omschrijving. Per concept een knop die de kansenkaart opent,
 * gefilterd op de datalagen van dat concept.
 *
 * Twee weergavemodi:
 *  - Overzicht: het bestaande grid met alle concepten.
 *  - Presentatie: de concepten 1-voor-1, met vorige/volgende (ook via
 *    pijltjestoetsen), zelfde bladerpatroon als popup.js.
 */
export function initBibliotheek(concepten, onToonKaart) {
  const container = document.getElementById("bibliotheek");
  container.innerHTML = "";

  const wissel = document.createElement("div");
  wissel.className = "bib-moduswissel";
  wissel.setAttribute("role", "group");
  wissel.setAttribute("aria-label", "Weergave");

  const overzichtKnop = document.createElement("button");
  overzichtKnop.type = "button";
  overzichtKnop.className = "modus-knop actief";
  overzichtKnop.textContent = "Overzicht";
  overzichtKnop.setAttribute("aria-pressed", "true");

  const presentatieKnop = document.createElement("button");
  presentatieKnop.type = "button";
  presentatieKnop.className = "modus-knop";
  presentatieKnop.textContent = "Presentatie";
  presentatieKnop.setAttribute("aria-pressed", "false");

  wissel.append(overzichtKnop, presentatieKnop);

  const grid = bouwGrid(concepten, onToonKaart);
  const presentatie = bouwPresentatie(concepten, onToonKaart);

  container.append(wissel, grid.el, presentatie.el);

  let modus = "overzicht";

  function zetModus(nieuweModus) {
    modus = nieuweModus;
    grid.el.hidden = modus !== "overzicht";
    presentatie.el.hidden = modus !== "presentatie";
    overzichtKnop.classList.toggle("actief", modus === "overzicht");
    overzichtKnop.setAttribute("aria-pressed", String(modus === "overzicht"));
    presentatieKnop.classList.toggle("actief", modus === "presentatie");
    presentatieKnop.setAttribute("aria-pressed", String(modus === "presentatie"));
    if (modus === "presentatie") {
      presentatie.toonHuidige();
    }
  }

  overzichtKnop.addEventListener("click", () => zetModus("overzicht"));
  presentatieKnop.addEventListener("click", () => zetModus("presentatie"));

  document.addEventListener("keydown", (event) => {
    if (modus !== "presentatie" || container.hidden) return;
    if (event.key === "ArrowLeft") presentatie.vorige();
    else if (event.key === "ArrowRight") presentatie.volgende();
  });
}

function bouwGrid(concepten, onToonKaart) {
  const el = document.createElement("div");
  el.className = "concept-grid";

  for (const concept of concepten) {
    const kaart = document.createElement("article");
    kaart.className = "concept-kaart";

    const img = document.createElement("img");
    img.src = concept.afbeelding;
    img.alt = concept.naam;
    img.loading = "lazy";

    const tekst = document.createElement("div");
    tekst.className = "concept-kaart-tekst";

    const titel = document.createElement("h3");
    titel.className = "concept-titel";
    titel.textContent = concept.naam;

    tekst.append(titel);

    const knop = document.createElement("button");
    knop.type = "button";
    knop.textContent = "Toon mij waar in Den Haag dit mogelijk is";
    knop.addEventListener("click", () => onToonKaart(concept));

    kaart.append(img, tekst, knop);
    el.appendChild(kaart);
  }

  return { el };
}

function bouwPresentatie(concepten, onToonKaart) {
  const el = document.createElement("div");
  el.className = "concept-presentatie";
  el.hidden = true;

  // De presentatie begint met het logo van de app als titelslide, gevolgd
  // door de concepten zelf.
  const slides = [
    {
      afbeelding: "Afbeeldingen/logo-app.png",
      naam: "De out-of-the-box pakketpunten viewer",
      omschrijving: "",
      isIntro: true,
    },
    ...concepten,
  ];

  const slide = document.createElement("div");
  slide.className = "presentatie-slide";
  const img = document.createElement("img");
  img.className = "presentatie-afbeelding";
  slide.appendChild(img);

  const titel = document.createElement("h3");
  titel.className = "presentatie-titel";

  const omschrijving = document.createElement("p");
  omschrijving.className = "presentatie-omschrijving";

  const nav = document.createElement("div");
  nav.className = "presentatie-nav";

  const vorigeKnop = document.createElement("button");
  vorigeKnop.type = "button";
  vorigeKnop.textContent = "←";
  vorigeKnop.setAttribute("aria-label", "Vorige");

  const teller = document.createElement("span");
  teller.className = "presentatie-teller";
  teller.setAttribute("aria-live", "polite");

  const volgendeKnop = document.createElement("button");
  volgendeKnop.type = "button";
  volgendeKnop.textContent = "→";
  volgendeKnop.setAttribute("aria-label", "Volgende");

  nav.append(vorigeKnop, teller, volgendeKnop);

  const ctaKnop = document.createElement("button");
  ctaKnop.type = "button";
  ctaKnop.className = "presentatie-cta";
  ctaKnop.textContent = "Toon mij waar in Den Haag dit mogelijk is";

  el.append(slide, titel, omschrijving, nav, ctaKnop);

  let index = 0;

  function toonHuidige() {
    const huidige = slides[index];
    img.classList.add("presentatie-afbeelding--wisselt");
    img.onload = () => img.classList.remove("presentatie-afbeelding--wisselt");
    img.src = huidige.afbeelding;
    img.alt = huidige.naam;
    img.classList.toggle("presentatie-afbeelding--logo", Boolean(huidige.isIntro));
    titel.textContent = huidige.naam;
    omschrijving.textContent = huidige.omschrijving || "";
    teller.textContent = `${index + 1} / ${slides.length}`;
    ctaKnop.hidden = Boolean(huidige.isIntro);
  }

  function vorige() {
    index = (index - 1 + slides.length) % slides.length;
    toonHuidige();
  }

  function volgende() {
    index = (index + 1) % slides.length;
    toonHuidige();
  }

  vorigeKnop.addEventListener("click", vorige);
  volgendeKnop.addEventListener("click", volgende);
  ctaKnop.addEventListener("click", () => onToonKaart(slides[index]));

  return {
    el,
    toonHuidige: () => {
      index = 0;
      toonHuidige();
    },
    vorige,
    volgende,
  };
}
