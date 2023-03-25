import redis
import hashlib
import sys
import time

ns = sys.argv[1]
r = redis.Redis()

while True:
    file = r.brpoplpush(f"{ns}:job", f"{ns}:working", timeout=0)
    if not file:
        break

    with open(file, 'rb') as f:
        contents = f.read()
    sha1 = hashlib.sha1(contents).hexdigest()

    r.set(f"{ns}:res:{file}", sha1)
    r.lpush(f"{ns}:res", "")

    r.lrem(f"{ns}:working", 1, file)
