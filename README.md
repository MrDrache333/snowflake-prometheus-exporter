Snowflake-Prometheus-Exporter
----------------------
[![GitHub Docker Registry](https://github.com/MrDrache333/snowflake-prometheus-exporter/actions/workflows/build.yml/badge.svg)](https://github.com/MrDrache333/snowflake-prometheus-exporter/actions/workflows/build.yml)

## Introduction
The Tor Project is an important initiative that promotes user privacy and security on the Internet. Tor allows users to obfuscate their Internet activity and thus protect their privacy by routing their traffic through a global network of voluntary nodes. Tor is also used by people in countries with high Internet censorship to access censored websites and applications.

Another important aspect of Tor is that it provides a secure platform for whistleblowers and people who are being persecuted for their opinions or activities on the Internet. Tor allows these users to hide their identity and location to ensure their safety.

Overall, the Tor project helps make the Internet a safer and more private place for all users. We believe it is important to maintain and encourage support for the Tor Project to ensure that users continue to have access to a free and safe Internet.

## How the exporter works

This exporter is based on a Python script that serves an HTTP server. When it receives a GET request with the path /metrics, it reads a log file, filters the log lines based on time windows (e.g. last 24 hours), and calculates statistics (e.g. number of connections, total upload and download traffic) from the log lines. It then formats the statistics as text in the Prometheus metric format and sends them back to the client in the HTTP response. The log file and the time windows for filtering the log lines are configurable.

## Add Metrics to Already Installed Snowflake Server

> **Note**: If you don't have snowflake already running on the system, this "install" method is not for you. Look at the next section for instructions.

Install Prometheus Node Exporter in your system. On debian it's as follows:

```bash
sudo apt install prometheus-node-exporter
```

Then run the following script periodically at least once per hour:

```bash
sudo journalctl -o cat -u snowflake-proxy > /tmp/snowflake-logs.txt
python3 main.py --no-serve /tmp/snowflake-logs.txt  | sudo tee /var/lib/prometheus/node-exporter/snowflake.prom
```

All metrics should be available on port `9100`, including the snowflake ones.


## Installation (Snowflake + exporter)

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

#### Docker Tags

The `latest` tag refers to the most recent version of the Docker image that has been built and pushed to the Docker
registry. It is generally recommended to use the latest tag to ensure that you are using the most up-to-date version of
the image.

The `arm64` tag refers to a specific version of the Docker image that has been built for the ARM64 architecture. This
version of the image is optimized for use on devices with ARM64 processors, such as the Raspberry Pi.

## Visualize using Grafana

![](grafana-sample-dashboard.png)

To import a sample Grafana dashboard, follow these steps:

1. Download the sample dashboard file `grafana-sample-dashboard.json`.
2. Open your Grafana instance in a web browser.
3. Log in to Grafana with your username and password.
4. Click on the "plus" icon in the left sidebar to open the "Create" menu.
5. Select "Import" from the "Create" menu.
6. Click on the "Choose File" button and select the .json file that you downloaded in step 1.
7. Click on the "Load" button to begin the import process.
8. If prompted, select prometheus as the data source that you want to use with the dashboard.
9. Review the dashboard and click on the "Import" button to complete the process.

You should now see the imported dashboard listed in the "Dashboards" section of the left sidebar. You can click on the
dashboard to view it.

## License

This project is licensed under the MIT License

## Authors

The Script used is based
on [analyze_snowflake_logs.py](https://gist.github.com/MariusHerget/8e061217ad0fb5709ac498e082903bd7)
by [MariusHerget](https://gist.github.com/MariusHerget)
