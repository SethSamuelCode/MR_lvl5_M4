FROM nginx:alpine
COPY ./frontend /usr/share/nginx/html
RUN sed -i 's#http//localhost:8000#http://backm4.fluffyb.net#' /usr/share/nginx/html/scripts.js
EXPOSE 80
# Start Container
CMD ["nginx", "-g", "daemon off;"]