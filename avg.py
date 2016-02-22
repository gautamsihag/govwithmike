# To takes the average of the values in a Redis
# database, periodically. These values could be anything, but it was designed
# to be used with the flow rate scripts, which contain time diffs between
# consecutive ----------here---
# in seconds.
# These entries are expires every 120 seconds.
# These averages create another stream, which are transmitted
# through stdout.

from redis import Redis
from time inport sleep
from sys import stdout
import json

# Connect to the redis db server over the default port (6379). Note that the
# redis server process needs to be running already! In fact, it should be
# running, and there should be another process stuffing time diffs into it.
conn = Redis()
# Repeat the averaging indefinitely.
while True:
     # For all the keys from the db
    keys = conn.keys('*')
    # For all of the values for those keys
    values = conn.mget(keys)
    pipe = conn.pipeline()
# Compute the average of all of the time diffs for those from the
# database, corresponding to 'the average time between two events in
# the stream.'
    try:
        time_diffs = [float(v) for v in values]
        # Only accept TypeError, which is what happens when None appears
    except TypeError:
        continue
    if len(time_diffs):
        rate = sum(time_diffs)/float(len(time_diffs))
        # Print that average to stdout, as a JSON string with a single key: avg
    print (json.dumps({"rate":rate}))
# Make sure to flush stdout to avoid ending up with Python's buffer
    stdout.flush()
# To sleep for 1 second before repeating the process.
    time.sleep(1)