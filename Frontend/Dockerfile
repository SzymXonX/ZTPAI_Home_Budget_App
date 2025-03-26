FROM node:18-alpine

WORKDIR /app/react_app

# Kopiuj z zachowaniem prawidłowych uprawnień dla Linuxa
COPY ./react_app/package*.json ./
RUN npm install --silent

COPY ./react_app ./

# Napraw uprawnienia
RUN chown -R node:node /app/react_app
USER node

CMD ["npm", "start"]