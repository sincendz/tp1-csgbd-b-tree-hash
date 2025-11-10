class Leaf:
    def __init__(self, order):
        self.values = []
        self.keys = []
        self.order = order
        self.next = None

    @property
    def is_full(self):
        return len(self.keys) >= self.order - 1

    def get_key_by_index(self, i):
        if i >= len(self.keys):
            raise ValueError("Index passado é maior que o tamanho da lista!")
        return self.keys[i]

    @property
    def keys_size(self):
        return len(self.keys)
