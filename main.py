# This Script uses the following dependancies
# pip install nums-from-string
# pip install datetime
#
# To Run this script type:
# python analyze_snowflake_logs.py <Log File Name>
#
# The default <Log File Name> is ./docker_snowflake.log
#
# Example:
# python analyze_snowflake_logs.py snow.log
#
# Written By Allstreamer_
# Licenced Under MIT
#
# Enhanced by MariusHerget
# Further enhanced by mrdrache333

import sys
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler

import nums_from_string


class TextHandler(BaseHTTPRequestHandler):
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

        # Read file
        lines_all = readFile()

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
            # Write the text message to the response body
            self.wfile.write(
                f"served_people{{time=\"{time}\"}} {stat['connections']}\n".encode() +
                f"upload_gb{{time=\"{time}\"}} {round(stat['upload_gb'], 4)}\n".encode() +
                f"download_gb{{time=\"{time}\"}} {round(stat['download_gb'], 4)}\n".encode()
            )


def readFile():
    # Read in log file as lines
    lines_all = []
    with open(logfile_path, "r") as file:
        lines_all = file.readlines()
    return lines_all


# Catch phrase for lines who do not start with a timestamp
def catchTimestampException(rowSubString, timestampFormat):
    try:
        return datetime.strptime(rowSubString, timestampFormat)
    except Exception as e:
        # print(e)
        return datetime.strptime("1970/01/01 00:00:00", "%Y/%m/%d %H:%M:%S")


# Filter the log lines based on a time delta in hours
def filterLinesBasedOnTimeDelta(log_lines, hours):
    now = datetime.now()
    length_timestamp_format = len(datetime.strftime(now, timestamp_format))
    return filter(lambda row: now - timedelta(hours=hours) <= catchTimestampException(row[0:length_timestamp_format],
                                                                                      timestamp_format) <= now,
                  log_lines)


# Convert traffic information (in B, KB, MB, or GB) to B (Bytes) and add up to a sum
def get_byte_count(log_lines):
    byte_count = 0
    for row in log_lines:
        symbols = row.split(" ")

        if symbols[2] == "B":
            byte_count += int(symbols[1])
        elif symbols[2] == "KB":
            byte_count += int(symbols[1]) * 1024
        elif symbols[2] == "MB":
            byte_count += int(symbols[1]) * 1024 * 1024
        elif symbols[2] == "GB":
            byte_count += int(symbols[1]) * 1024 * 1024 * 1024
    return byte_count


# Filter important lines from the log
# Extract number of connections, uploaded traffic in GB and download traffic in GB
def getDataFromLines(lines):
    # Filter out important lines (Traffic information)
    lines = [row.strip() for row in lines]
    lines = filter(lambda row: "In the" in row, lines)
    lines = [row.split(",", 1)[1] for row in lines]

    # Filter out all traffic log lines who did not had any connection
    lines = list(filter(lambda row: not nums_from_string.get_nums(row)[0] == 0, lines))

    # Extract number of connections as a sum
    connections = sum([nums_from_string.get_nums(row)[0] for row in lines])

    # Extract upload and download data
    lines = [row.split("Relayed")[1] for row in lines]
    upload = [row.split(",")[0].strip() for row in lines]
    download = [row.split(",")[1].strip()[:-1] for row in lines]

    # Convert upload/download data to GB
    upload_gb = get_byte_count(upload) / 1024 / 1024 / 1024
    download_gb = get_byte_count(download) / 1024 / 1024 / 1024

    # Return information as a dictionary for better structure
    return {'connections': connections, 'upload_gb': upload_gb, 'download_gb': download_gb}


# Format of your timestamps in the beginning of the log
# e.g. "2022/01/01 16:50:30 <LOG ENTRY>" => "%Y/%m/%d %H:%M:%S"
timestamp_format = "%Y/%m/%d %H:%M:%S"

# Log file path from arguments (default: ./docker_snowflake.log)
logfile_path = sys.argv[1] if len(sys.argv) > 1 else "./docker_snowflake.log"

# Start the HTTP server on port 8080
httpd = HTTPServer(("", 8080), TextHandler)
httpd.serve_forever()
