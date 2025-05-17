const fetch = require('node-fetch');

module.exports = {
  name: "DSGVO-Agent",
  description: "Stellt DSGVO-Fragen an den FastAPI-Agenten.",
  version: "1.0.0",

  async execute(input) {
    try {
      const response = await fetch("http://host.docker.internal:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: input })
      });

      if (!response.ok) {
        return `Fehler beim Aufruf des DSGVO-Agenten: ${response.statusText}`;
      }

      const data = await response.json();
      return data.answer || "Keine Antwort erhalten.";
    } catch (err) {
      return `Fehler: ${err.message}`;
    }
  }
};
