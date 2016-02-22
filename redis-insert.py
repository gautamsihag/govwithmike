from sys import stdin, stdout
from uuid import uuid1
import json
import redis

conn = redis.Redis
while True:
    diff = json.loads(stdin.readline()).get('delta')
    conn.setex(str(uuid1()),diff,120)
    print(json.dumps({'delta':diff}))
    stdout.flush()