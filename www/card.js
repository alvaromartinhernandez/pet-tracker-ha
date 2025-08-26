// pet-event-card.js
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
          margin-bottom: 16px;
        }
        button {
          font-size: 18px;
          border: none;
          border-radius: 12px;
          padding: 12px 20px;
          cursor: pointer;
          margin: 0 8px;
        }
        .poop { background: #d2691e; color: white; }
        .pee { background: #f0e68c; color: black; }
        .events-list {
          padding: 16px;
        }
        .event-item {
          display: flex;
          justify-content: space-between;
          padding: 8px;
          border-bottom: 1px solid #eee;
        }
        .event-type {
          font-weight: bold;
        }
        .event-time {
          color: #666;
        }
        .no-events {
          text-align: center;
          color: #999;
          padding: 20px;
        }
      `;

      const container = document.createElement("div");
      
      // Botones
      const buttonContainer = document.createElement("div");
      buttonContainer.classList.add("buttons");

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

      buttonContainer.appendChild(poopBtn);
      buttonContainer.appendChild(peeBtn);

      // Lista de eventos
      this.eventsContainer = document.createElement("div");
      this.eventsContainer.classList.add("events-list");

      container.appendChild(buttonContainer);
      container.appendChild(this.eventsContainer);

      this.content.appendChild(style);
      this.content.appendChild(container);
      this.appendChild(this.content);
    }

    // Actualizar lista de eventos
    this.updateEvents(hass);
  }

  updateEvents(hass) {
    const historySensor = hass.states["sensor.pet_historial"];
    if (historySensor && historySensor.attributes && historySensor.attributes.events) {
      const events = historySensor.attributes.events;
      
      if (events.length === 0) {
        this.eventsContainer.innerHTML = '<div class="no-events">No hay eventos en los últimos 7 días</div>';
        return;
      }

      let html = '';
      events.forEach(event => {
        const emoji = event.type === 'poop' ? '💩' : '💧';
        const typeText = event.type === 'poop' ? 'Caca' : 'Pis';
        html += `
          <div class="event-item">
            <span class="event-type">${emoji} ${typeText}</span>
            <span class="event-time">${event.date} ${event.time}</span>
          </div>
        `;
      });
      
      this.eventsContainer.innerHTML = html;
    } else {
      this.eventsContainer.innerHTML = '<div class="no-events">Cargando eventos...</div>';
    }
  }

  setConfig(config) {}
  
  getCardSize() {
    return 4;
  }
}

customElements.define("pet-event-card", PetEventCard);