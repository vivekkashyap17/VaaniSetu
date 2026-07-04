# VaaniSetu frontend — build the Vite SPA, serve the static bundle via nginx.
FROM node:20-alpine AS build

WORKDIR /app

# Install deps first for better layer caching.
COPY package.json package-lock.json* ./
RUN npm ci

COPY . .

# Vite bakes VITE_* values into the bundle at build time, so they are passed
# as build args (the API base the browser will call, and the API key).
ARG VITE_API_BASE_URL=http://localhost:8000
ARG VITE_API_KEY=change-me
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_API_KEY=$VITE_API_KEY

RUN npm run build


FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
