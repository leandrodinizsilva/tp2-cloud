FROM node:22-slim

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 31337

ENV HOST=0.0.0.0
ENV PORT=31337

RUN VITE_PORT=31337 npm run dev

# RUN npm install -g serve
# CMD ["serve", "-s", "build", "-l", "31337"]