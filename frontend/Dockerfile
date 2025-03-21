FROM node:lts as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build

FROM httpd:2.4 as production-stage
RUN apt-get update && apt-get install -y \
    wget

# Install Apache OpenIDC
RUN apt -qy install wget
RUN cd / \
    && wget https://github.com/OpenIDC/mod_auth_openidc/releases/download/v2.4.16.8/libapache2-mod-auth-openidc_2.4.16.8-1.bookworm_amd64.deb \
    && apt-get -qy install ./libapache2-mod-auth-openidc_2.4.16.8-1.bookworm_amd64.deb

COPY --from=build-stage /app/dist /usr/local/apache2/htdocs/
