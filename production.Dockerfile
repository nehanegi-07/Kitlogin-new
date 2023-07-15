#
# This Dockerfile is used for self-hosted production builds.
#
# Note: for 'analytickit/analytickit-cloud' remember to update 'prod.web.Dockerfile' as appropriate
#

#
# Build the frontend artifacts
#
# Build the frontend artifacts and name it frontend
# FROM node:16.15-alpine3.14 AS frontend. 
FROM --platform=linux/amd64 node:16.15-alpine3.14 AS frontend

WORKDIR /code


COPY ./frontend/package.json ./frontend/yarn.lock ./


RUN yarn config set network-timeout 300000 && \
    yarn install --frozen-lockfile

COPY frontend/ frontend/
COPY ./bin ./bin/

# Install dependencies for building and running React scripts
#RUN yarn global add react-scripts@4.0.0

# Build the frontend
RUN yarn --cwd ./frontend install --force
RUN yarn --cwd ./frontend build

# Change ownership of the frontend files to root
USER root
RUN chown -R root:root /code/frontend
RUN chmod -R 777 /code/frontend


# Install python, make and gcc as they are needed for the yarn install
RUN apk --update --no-cache add \
    "make~=4.3" \
    "g++~=10.3" \
    "gcc~=10.3" \
    "python3~=3.9"


# Build the kitlogin image, incorporating the Django app along with the frontend,
# FROM python:3.8.12-alpine3.14
FROM --platform=linux/amd64 python:3.8.12-alpine3.14 AS backend



ENV PYTHONUNBUFFERED 1
ENV export PYTHONPATH ./kitlogin




WORKDIR /code

# Install OS dependencies needed to run analytickit
#
# Note: please add in this section runtime dependences only.
# If you temporary need a package to build a Python or npm
# dependency take a look at the sections below.
RUN apk --update --no-cache add \
    "libpq~=13" \
    "libxslt~=1.1" \
    "nodejs-current~=16" \
    "chromium~=93" \
    "chromium-chromedriver~=93" \
    "xmlsec~=1.2"


# Compile and install Python dependencies.
#
# Notes:
#
# - we explicitly COPY the files so that we don't need to rebuild
#   the container every time a dependency changes
#
# - we need few additional OS packages for this. Let's install
#   and then uninstall them when the compilation is completed.
COPY requirements.txt ./
RUN apk --update --no-cache --virtual .build-deps add \
    "bash~=5.1" \
    "g++~=10.3" \
    "gcc~=10.3" \
    "cargo~=1.52" \
    "git~=2" \
    "make~=4.3" \
    "libffi-dev~=3.3" \
    "libxml2-dev~=2.9" \
    "libxslt-dev~=1.1" \
    "xmlsec-dev~=1.2" \
    "postgresql-dev~=13" \
    "libmaxminddb~=1.5" \
    && \
    pip install -r requirements.txt --compile --no-cache-dir \
    && \
    apk del .build-deps

# Switch to root and install yarn so we can install runtime deps. Node that we
# still need yarn to run the plugin-server so we do not remove it.
USER root
RUN apk --update --no-cache add "yarn~=1"

# NOTE: we need make and g++ for node-gyp
# NOTE: npm is required for re2
RUN apk --update --no-cache add "make~=4.3" "g++~=10.3" "npm~=7" --virtual .build-deps \
    && yarn install --frozen-lockfile --production=true \
    && yarn cache clean \
    && apk del .build-deps

# We need bash to run the bin scripts
RUN apk --update --no-cache add "bash~=5.1"
COPY ./bin ./bin/

RUN addgroup -S kitlogin && \
    adduser -S kitlogin -G kitlogin

RUN chown kitlogin.kitlogin /code

USER kitlogin

# Add in Django deps and generate Django's static files
COPY manage.py manage.py
COPY sca ./sca
COPY checkout ./checkout
COPY login ./login
COPY dj_rest_auth ./dj_rest_auth
COPY kitlogin ./kitlogin
COPY db.sqlite3 db.sqlite3 

# Add  frontend from previous build
COPY --from=frontend /code/frontend/ frontend/
#COPY --from=frontend /code/frontend/dist /code/frontend/dist







ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_PATH=/usr/lib/chromium/ \
    CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Expose container port and run entry point script
EXPOSE 8000

# Expose the port from which we serve frontend which is default port, not sure why
EXPOSE 3000


# Start the frontend and backend servers 
CMD ["/bin/sh", "/code/bin/docker"]


