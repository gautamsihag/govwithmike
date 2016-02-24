import sys
from sys import stdin, stdout
import json
import redis

conn = redis.Redis()
while True:
    line = sys.stdin.readline()
    d = json.loads(line)
    delta = d["delta"]
    time = d["t"]
    conn.setex(time, delta, 120)
    print (json.dumps({"time":time, "delta":delta}))
    stdout.flush()