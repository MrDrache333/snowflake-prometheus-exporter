#!/usr/bin/python3
# This Script uses the following dependencies
# pip install nums-from-string
# pip install datetime
#
# To Run this script type:
# python main.py <Log File Name>
#
# The default <Log File Name> is ./docker_snowflake.log
#
# Example:
# python main.py snow.log
#
# Written By Allstreamer_
# Licenced Under MIT
#
# Enhanced by MariusHerget
# Further enhanced and modified by mrdrache333
# Further enhanced by francisco-core

import argparse
import sys
import re
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler

# Format of your timestamps in the beginning of the log
# e.g. "2022/01/01 16:50:30 <LOG ENTRY>" => "%Y/%m/%d %H:%M:%S"
TIMESTAMP_FORMAT = "%Y/%m/%d %H:%M:%S"

def nums_from_string(string):
    return [int(num) for num in re.findall(r"\d+", string)]

class TextHandler(BaseHTTPRequestHandler):
    logfile_path = None

    def do_GET(self):

        if self.path != "/metrics":
            # If the request path is not /metrics, return a 404 Not Found error
            self.send_error(404)
            return
        # Set the response status code to 200 OK
        self.send_response(200)

        # Set the content type to text/plain
        self.send_header("Content-type", "text/plain")

        # End the headers
        self.end_headers()

        # Return the metrics
        print_stats(
            self.logfile_path,
            lambda x: self.wfile.write(x.encode())  # encode response
        )


def print_stats(logfile_path: str, printer_func):
    # Read file
    lines_all = readFile(logfile_path)

    # Get the statistics for various time windows
    # e.g. all time  => getDataFromLines(lines_all, 24)
    # e.g. last 24h  => getDataFromLines(filterLinesBasedOnTimeDelta(lines_all, 24))
    # e.g. last Week => getDataFromLines(filterLinesBasedOnTimeDelta(lines_all, 24 * 7))
    stats = {
        'All time': getDataFromLines(lines_all),
        'Last 24h': getDataFromLines(filterLinesBasedOnTimeDelta(lines_all, 24)),
        'Last Week': getDataFromLines(filterLinesBasedOnTimeDelta(lines_all, 24 * 7)),
    }

    # Print all the results in the Prometheus metric format
    for time in stats:
        stat = stats[time]
        printer_func(
            f"served_people{{time=\"{time}\"}} {stat['connections']}\n" +
            f"upload_gb{{time=\"{time}\"}} {round(stat['upload_gb'], 4)}\n" +
            f"download_gb{{time=\"{time}\"}} {round(stat['download_gb'], 4)}\n"
        )

def readFile(logfile_path: str):
    # Read in log file as lines
    lines_all = []
    with open(logfile_path, "r") as file:
        lines_all = file.readlines()
    return lines_all


# Catchphrase for lines who do not start with a timestamp
def catchTimestampException(rowSubString, timestampFormat):
    try:
        return datetime.strptime(rowSubString, timestampFormat)
    except Exception:
        return datetime.strptime("1970/01/01 00:00:00", "%Y/%m/%d %H:%M:%S")


# Filter the log lines based on a time delta in hours
def filterLinesBasedOnTimeDelta(log_lines, hours):
    now = datetime.now()
    length_timestamp_format = len(datetime.strftime(now, TIMESTAMP_FORMAT))
    return filter(lambda row: now - timedelta(hours=hours) <= catchTimestampException(row[0:length_timestamp_format],
                                                                                      TIMESTAMP_FORMAT) <= now,
                  log_lines)


# Convert traffic information (in B, KB, MB, or GB) to B (Bytes) and add up to a sum
def get_byte_count(log_lines):
    byte_count = 0
    for row in log_lines:
        symbols = row.split(" ")

        # Use a dictionary to map units to their byte conversion values
        units = {
            "B": 1,
            "KB": 1024,
            "MB": 1024 * 1024,
            "GB": 1024 * 1024 * 1024
        }

        # Use the dictionary to get the byte conversion value for the current unit
        byte_count += int(symbols[1]) * units[symbols[2]]
    return byte_count


# Filter important lines from the log
# Extract number of connections, uploaded traffic in GB and download traffic in GB
def getDataFromLines(lines):
    # Filter out important lines (Traffic information)
    lines = [row.strip() for row in lines if "In the" in row]
    lines = [row.split(",", 1)[1] for row in lines]

    # Filter out all traffic log lines who did not had any connection
    lines = [row for row in lines if nums_from_string(row)[0] != 0]

    # Extract number of connections as a sum
    connections = sum([nums_from_string(row)[0] for row in lines])

    # Extract upload and download data
    lines = [row.split("Relayed")[1] for row in lines]
    upload = [row.split(",")[0].strip() for row in lines]
    download = [row.split(",")[1].strip()[:-1] for row in lines]

    # Convert upload/download data to GB
    upload_gb = get_byte_count(upload) / 1024 / 1024 / 1024
    download_gb = get_byte_count(download) / 1024 / 1024 / 1024

    # Return information as a dictionary for better structure
    return {'connections': connections, 'upload_gb': upload_gb, 'download_gb': download_gb}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--serve",
        dest="serve",
        action="store_true",
        help="Start http server directly on port 8080"
    )
    parser.add_argument(
        "--no-serve",
        dest="serve",
        action="store_false",
        help="Simply parse the input file"
    )
    parser.set_defaults(serve=True)

    # Log file path from arguments (default: ./docker_snowflake.log)
    parser.add_argument("logfile_path", default="./docker_snowflake.log")
    args = parser.parse_args()

    if args.serve:
        # Start the HTTP server on port 8080
        TextHandler.logfile_path = args.logfile_path
        httpd = HTTPServer(("", 8080), TextHandler)
        httpd.serve_forever()
    else:
        # Simply parse the file and print the resulting metrics
        print_stats(args.logfile_path, sys.stdout.write)
