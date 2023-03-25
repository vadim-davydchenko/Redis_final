import redis
import sys

ns = sys.argv[1]

r = redis.Redis()

files = sys.argv[2:]

r.lpush(ns + ':job', *files)

while True:
    remaining = r.lrange(ns + ':job', 0, -1)
    if not remaining:
        break
    
    for file in remaining:
        res = r.mget(ns + ':res:' + file)
        
        if not any(res):
            res = r.blpop(ns + ':res', timeout=3)
            if not res:
                print('No results available for file:', file)
                continue
            else:
                _, result_file, result_value = res
                if result_file != ns + ':res:' + file:
                    print('Unexpected result file:', result_file)
                    continue
                else:
                    print(file, result_value)
                    r.lrem(ns + ':job', 1, file)
        else:
            print(file, res[0])
            r.lrem(ns + ':job', 1, file)
