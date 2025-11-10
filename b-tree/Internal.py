class Internal:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.nodes = []

    def is_full(self):
        return len(self.keys) >= self.order - 1
