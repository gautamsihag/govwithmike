# The python script below takes the piped stream from diff.py (which are time deltas)
# between events in the stream and adds it to redis with a unique identifier.
# the idea is based on:
# https://github.com/mikedewar/RealTimeStorytelling/blob/master/2/insert.py

import sys
from sys import stdin, stdout
import json
import redis

# Connect to the redis db
conn = redis.Redis()
while True:
    line = sys.stdin.readline()
    d = json.loads(line)
    delta = d["delta"]
    time = d["t"]
    # Add it to the database and let it expire after 120 seconds, to big smooth the function we
    # get.
    conn.setex(time, delta, 120)
    # Print to stdout as a confirmation.
    print (json.dumps({"time":time, "delta":delta}))
    stdout.flush()