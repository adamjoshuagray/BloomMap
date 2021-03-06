# file: BloomMap.py
# Written by Adam J. Gray 2015.
# This file contains a quick and dirty implementation of
# a Bloom-filtered map.
# Obviously this could be implemented more efficiently.
#
# More info on Bloom filters can be obtained at:
# https://en.wikipedia.org/wiki/Bloom_filter

from random import *

# This is the underlying has function.
# It should not be called directly, instead a set of these functions.
# with different parameterizations can be generated by generate_hashes.
def _hash(string, salt, m):
    r = Random()
    r.seed(string + salt)
    return r.randint(0, m-1)

# This generates a list of hashes with given paramters.
# m     - The number of bits that the hash function can reference.
# k     - The number of hash functions to generate.
def generate_hashes(m, k):
    return map(lambda i: (lambda s: _hash(s, str(i), m)), range(k))

# This contains the info for a Bloom filter
# m         - The number of bits in the Bloom filter
# hashes    - A list of hash functions which map a string uniformally at random
#             onto the set of integers { j \in Z : 0 <= j < m }
class BloomInfo:
    def __init__(self, m, hashes):
        self.m      = m
        self.hashes = hashes

# This defines the basic functionality of a Bloom map.
# Notes:
# Items can be added to the map, but not removed.
# Technically the underlying_map does not have to be a Python
# dict but it must implement the underlying_map[j] = some_value
# setter routine and the get function the same as a regular Python dict
class BloomMap:
    # Initializes the BloomMap.
    # info              - The Bloom filter info. This should be of type BloomInfo
    # underlying_map    - The actual map (dict) underlying the BLoom map.
    #                     See notes in class comments about requirements for the
    #                     implementation of underlying_map.
    # mask [optional]   - The boolean mask which encodes which items have already
    #                     been set. If this is not set the a new mask will be created
    #                     One should make sure that underlying_map and mask already
    #                     in aggreement with each other.
    def __init__(self, info, underlying_map, mask = None):
        self.info               = info
        self.underlying_map     = underlying_map
        if mask is None:
            self.mask           = [False] * info.m
        elif len(mask) == info.m:
            assert(len(mask) == info.m)
            self.mask           = mask

    # Checks if a given key is in the map and returns that value if it is, otherwise
    # this returns None.
    # key   - The string key of the object to lookup.
    def get(self, key):
        exists = reduce(lambda a, b: a and b, map(lambda f: self.mask[f(key)], self.info.hashes))
        if not exists:
            return None
        else:
            return self.underlying_map.get(key)

    # Sets a value in the map.
    # key   - The string key of the object to use.
    # value - The actual object to store in the map.
    def set(self, key, value):
        self.underlying_map[key] = value
        map(lambda f: self.mask[f(key)] = True, self.info.hashes)
