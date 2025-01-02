FROM node:18-slim

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 31332

ENV HOST=0.0.0.0
ENV PORT=31332

RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "31332"]