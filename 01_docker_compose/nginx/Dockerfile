FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
COPY site.conf /etc/nginx/conf.d/