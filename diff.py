# This script takes the Unix-piped stream from meet2.py. 
# it calculates the time difference between the two
# earliest timestamps, outputs the result as a JSON to stdout.
# This script is a copy of:
# https://github.com/mikedewar/RealTimeStorytelling/blob/master/2/diff.py
import json
import sys
# to hold the value of the last event
last = 0
# repeat while true
while True:
    # load the JSON string, and then get the 'timestamp' key, which is a
    # Unix timestamp
    line = sys.stdin.readline()
    d = json.loads(line)
    # if the last doesnot have a values till now; this captures the first condition
    if last == 0 :
        # update the last with the current value
        last = d["t"]
        continue
    # calculating the absolute difference between the occurence of the 
    # events to store the values into redis
    delta = abs(d["t"] - last)
    # dump the diff to stdout as a JSON with key 'delta'
    print (json.dumps({"delta":delta, "t":d["t"]}))
    sys.stdout.flush()
    # update the timestamp value of the last event
    last = d["t"]