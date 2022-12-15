Snowflake + Prometheus
----------------------
[![GitHub Docker Registry](https://github.com/MrDrache333/snowflake-prometheus-exporter/actions/workflows/build.yml/badge.svg)](https://github.com/MrDrache333/snowflake-prometheus-exporter/actions/workflows/build.yml)

This Docker Compose file sets up two containers: a [Snowflake](https://www.torproject.org/projects/snowflake.html.en)
proxy and a [Prometheus](https://prometheus.io/) server. It also includes a third container, a Prometheus exporter for
Snowflake, which scrapes metrics from the Snowflake proxy and makes them available to the Prometheus server.

### Prerequisites

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

### Usage

1. Clone this repository and navigate to the directory:

```
git clone https://github.com/mrdrache333/snowflake-prometheus-exporter.git cd snowflake-prometheus-exporter
```

2. Run the containers using Docker Compose:

```
docker-compose up
```

3. Open a web browser and navigate to `http://localhost:9090` to access the Prometheus web UI.

### Configuration

The `docker-compose.yml` file includes several configurable options, such as the ports exposed by the containers and the
locations of the volume mounts. You can modify these options to fit your needs.

### License

This project is licensed under the MIT License
