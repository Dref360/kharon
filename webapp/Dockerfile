FROM node:18 AS build
WORKDIR /app
RUN npm install -g serve

COPY package.json package-lock.json ./
RUN npm install
COPY . ./
RUN npm run build


FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/log/app_engine


EXPOSE 8080 80
CMD ["nginx", "-g", "daemon off;"]