Snowflake-Prometheus-Exporter
----------------------
[![GitHub Docker Registry](https://github.com/MrDrache333/snowflake-prometheus-exporter/actions/workflows/build.yml/badge.svg)](https://github.com/MrDrache333/snowflake-prometheus-exporter/actions/workflows/build.yml)

## Introduction
The Tor Project is an important initiative that promotes user privacy and security on the Internet. Tor allows users to obfuscate their Internet activity and thus protect their privacy by routing their traffic through a global network of voluntary nodes. Tor is also used by people in countries with high Internet censorship to access censored websites and applications.

Another important aspect of Tor is that it provides a secure platform for whistleblowers and people who are being persecuted for their opinions or activities on the Internet. Tor allows these users to hide their identity and location to ensure their safety.

Overall, the Tor project helps make the Internet a safer and more private place for all users. We believe it is important to maintain and encourage support for the Tor Project to ensure that users continue to have access to a free and safe Internet.

## How the exporter works

This exporter is based on a Python script that serves an HTTP server. When it receives a GET request with the path /metrics, it reads a log file, filters the log lines based on time windows (e.g. last 24 hours), and calculates statistics (e.g. number of connections, total upload and download traffic) from the log lines. It then formats the statistics as text in the Prometheus metric format and sends them back to the client in the HTTP response. The log file and the time windows for filtering the log lines are configurable.

## Installation

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
docker-compose up -d
```

3. Open a web browser and navigate to `http://localhost:9090` to access the Prometheus web UI.

### Configuration

The `docker-compose.yml` file includes several configurable options, such as the ports exposed by the containers and the
locations of the volume mounts. You can modify these options to fit your needs.

### License

This project is licensed under the MIT License

### Authors

The Script used is based
on [analyze_snowflake_logs.py](https://gist.github.com/MariusHerget/8e061217ad0fb5709ac498e082903bd7)
by [MariusHerget](https://gist.github.com/MariusHerget)
