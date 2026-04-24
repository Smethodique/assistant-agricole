# Use the official Nginx image
FROM nginx:alpine

# Copy the static files from the src directory to the Nginx html directory
COPY frontend/src /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
