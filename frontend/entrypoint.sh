#!/bin/sh

# Replace BACKEND_URL in the JavaScript file
sed -i "s|http://localhost:8000|${BACKEND_URL}|g" /usr/share/nginx/html/scripts.js

# Start nginx
exec nginx -g 'daemon off;'
