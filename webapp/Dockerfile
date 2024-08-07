FROM node:18 AS build
WORKDIR /app
RUN npm install -g serve

COPY package.json package-lock.json ./
RUN npm install
COPY . ./
RUN npm run build


ENV PORT 8080
EXPOSE 8080
CMD ["serve", "-s", "-l", "8080", "/app/build"]
