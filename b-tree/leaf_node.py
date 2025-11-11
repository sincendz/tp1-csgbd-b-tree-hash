import math
from time import sleep


class Leaf:
    def __init__(self, order):
        self.values = []
        self.keys = []
        self.order = order
        self.next = None

    @property
    def is_full(self):
        return len(self.keys) > self.order - 1

    @property
    def leaf_has_the_minimum_keys(self):
        return len(self.keys) >= math.ceil( self.order / 2) - 1

    def get_key_by_index(self, i):
        return self.keys[i]

    @property
    def keys_size(self):
        return len(self.keys)
