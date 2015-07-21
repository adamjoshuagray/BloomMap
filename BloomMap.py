from random import *

def _hash(string, salt, m):
    r = Random()
    r.seed(string + salt)
    return r.randint(0, m-1)

def generate_hashes(m, k):
    return map(lambda i: (lambda s: _hash(s, str(i), m)), range(k))

class BloomInfo:
    def __init__(self, m, hashes):
        self.m      = m
        self.hashes = hashes

class BloomMap:
    def __init__(self, info, underlying_map, mask = None):
        self.info               = info
        self.underlying_map     = underlying_map
        if mask is None:
            self.mask           = [False] * info.m
        elif len(mask) == info.m:
            assert(len(mask) == info.m)
            self.mask           = mask

    def get(self, key):
        exists = reduce(lambda a, b: a and b, map(lambda f: self.mask[f(key)], self.info.hashes))
        if not exists:
            return None
        else:
            return self.underlying_map.get(key)

    def set(self, key, value):
        self.underlying_map[key] = value
        map(lambda f: self.mask[f(key)] = True, self.info.hashes)
