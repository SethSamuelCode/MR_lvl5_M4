FROM nginx:alpine
COPY ./frontend /usr/share/nginx/html
COPY ./frontend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 80
# Start Container with our entrypoint script
ENTRYPOINT ["/entrypoint.sh"]