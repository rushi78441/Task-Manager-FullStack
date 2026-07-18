# --- Stage 1: Build the React application ---
FROM node:20-alpine AS build
WORKDIR /app

# Copy package management files first to cache dependencies
COPY package*.json ./
# Clean install ALL dependencies (including devDependencies like vite plugins)
RUN npm ci

# Copy the rest of the application files and build
COPY . .
RUN npm run build

# --- Stage 2: Serve the application using Nginx ---
FROM nginx:alpine

# Copy a basic Nginx config directly without needing an external file
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Copy Vite's default build output folder ('dist') to Nginx HTML dir
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]