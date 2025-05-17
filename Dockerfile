FROM node:18

# Set working directory
WORKDIR /app

# Clone neueste AnythingLLM-Version von GitHub
RUN git clone https://github.com/Mintplex-Labs/anything-llm.git .

# Installiere Node-Pakete inkl. node-fetch (für Custom Skills wichtig)
RUN npm install && npm install node-fetch

# Expose UI-Port (aktuell 3001 in neuer Version)
EXPOSE 3001

# Starte die App
CMD ["npm", "run", "start"]
