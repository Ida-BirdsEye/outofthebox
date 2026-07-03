/**
 * Bouwt de popup-inhoud voor een kaartpunt: de conceptafbeelding(en) die aan
 * de datalaag van dat punt gekoppeld zijn, plus een link naar Google Street
 * View op exact die locatie. Bij meerdere gekoppelde concepten kan de
 * gebruiker met pijlknoppen door de afbeeldingen bladeren.
 */
export function buildPopupContent(concepten, lat, lon) {
  const container = document.createElement("div");
  container.className = "popup-concepten";

  if (!concepten || concepten.length === 0) {
    const leegtekst = document.createElement("p");
    leegtekst.className = "popup-leeg";
    leegtekst.textContent = "Geen concept gekoppeld aan deze locatie.";
    container.appendChild(leegtekst);
  } else {
    let index = 0;

    const img = document.createElement("img");
    img.className = "popup-afbeelding";
    container.appendChild(img);

    const titel = document.createElement("p");
    titel.className = "popup-titel";
    container.appendChild(titel);

    if (concepten.length > 1) {
      const nav = document.createElement("div");
      nav.className = "popup-nav";

      const vorige = document.createElement("button");
      vorige.type = "button";
      vorige.textContent = "←";
      vorige.setAttribute("aria-label", "Vorig concept");

      const teller = document.createElement("span");
      teller.className = "popup-teller";

      const volgende = document.createElement("button");
      volgende.type = "button";
      volgende.textContent = "→";
      volgende.setAttribute("aria-label", "Volgend concept");

      const toon = () => {
        img.src = concepten[index].afbeelding;
        img.alt = concepten[index].naam;
        titel.textContent = concepten[index].naam;
        teller.textContent = `${index + 1} / ${concepten.length}`;
      };

      vorige.addEventListener("click", () => {
        index = (index - 1 + concepten.length) % concepten.length;
        toon();
      });
      volgende.addEventListener("click", () => {
        index = (index + 1) % concepten.length;
        toon();
      });

      nav.append(vorige, teller, volgende);
      container.appendChild(nav);
      toon();
    } else {
      img.src = concepten[0].afbeelding;
      img.alt = concepten[0].naam;
      titel.textContent = concepten[0].naam;
    }
  }

  if (lat != null && lon != null) {
    const streetviewLink = document.createElement("a");
    streetviewLink.className = "popup-streetview";
    streetviewLink.href = `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lon}`;
    streetviewLink.target = "_blank";
    streetviewLink.rel = "noopener noreferrer";
    streetviewLink.textContent = "Bekijk in Google Street View ↗";
    container.appendChild(streetviewLink);
  }

  return container;
}
