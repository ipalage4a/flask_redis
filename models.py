from functools import reduce
from app import redis_client

def get_links_from_set(from_key, to_key):
    if None not in [from_key, to_key] and from_key <= to_key:
        sets = [redis_client.smembers(f'time:{key}:links') for key in range(from_key, to_key + 1)]
        return list(reduce(lambda x, y: x.union(y), sets))
    else:
        return []

def put_links_in_set(_time, links):
    try:
        with redis_client.pipeline() as pipe:
            for key, link in enumerate(links):
                pipe.sadd(f'time:{_time}:links', link)
            pipe.execute()
        status = "ok"
    except Exception as error:
        status = repr(error)
    return status
