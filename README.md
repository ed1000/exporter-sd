# osm-exporter-sd

Prometheus HTTP Service Discovery for OSM Exporters

## Build docker

To build the docker container:

`docker build . -f Dockerfile.local -t opensourcemano/osm-exporter-sd:local`

## Run docker container

To run the docker container:

`docker run -p 8000:8000 opensourcemano/osm-exporter-sd:local`

### Environment variables

The docker container supports 3 environment variables:
- **DB_URL**: the URL for the database to be used
- **LCM_PASSWORD**: the password to be used by LCM to access the service
- **PROMETHEUS_PASSWORD**: the password to be used by Prometheus to access the service

