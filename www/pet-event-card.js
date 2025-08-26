class PetEventCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      this.content = document.createElement("ha-card");
      this.content.header = "Pet Event Tracker";

      const style = document.createElement("style");
      style.textContent = `
        .buttons {
          display: flex;
          justify-content: space-around;
          padding: 16px;
        }
        button {
          font-size: 18px;
          border: none;
          border-radius: 12px;
          padding: 12px 20px;
          cursor: pointer;
        }
        .poop { background: #d2691e; color: white; }
        .pee { background: #f0e68c; color: black; }
      `;

      const container = document.createElement("div");
      container.classList.add("buttons");

      const poopBtn = document.createElement("button");
      poopBtn.innerHTML = "💩 Caca";
      poopBtn.classList.add("poop");
      poopBtn.addEventListener("click", () => {
        hass.callService("pet_event_tracker", "log_poop");
      });

      const peeBtn = document.createElement("button");
      peeBtn.innerHTML = "💧 Pis";
      peeBtn.classList.add("pee");
      peeBtn.addEventListener("click", () => {
        hass.callService("pet_event_tracker", "log_pee");
      });

      container.appendChild(poopBtn);
      container.appendChild(peeBtn);

      this.content.appendChild(style);
      this.content.appendChild(container);
      this.appendChild(this.content);
    }
  }

  setConfig(config) {}
  getCardSize() {
    return 2;
  }
}

customElements.define("pet-event-card", PetEventCard);
