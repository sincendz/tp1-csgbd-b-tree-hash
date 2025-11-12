class Bucket:
    def __init__(self, bucket_size, local_depth):
        self.values = []
        self.bucket_size = bucket_size
        self.local_depth = local_depth

    @property
    def is_full(self):
        return len(self.values) > self.bucket_size

    def __repr__(self):
        return f"Bucket(ld={self.local_depth}, values={self.values})"


class ExtensibleHash:
    def __init__(self, bucket_size: int):
        self.bucket_size = bucket_size
        self.global_depth = 2
        self.buckets = [Bucket(bucket_size, self.global_depth) for _ in range(2 ** self.global_depth)]

    def _hash(self, key):
        return hash(key) & ((1 << self.global_depth) - 1)

    def insert(self, key: int, value: any):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, _) in enumerate(bucket.values):
            if k == key:
                bucket.values[i] = (key, value)
                return

        bucket.values.append((key, value))

        if bucket.is_full:
            self._split_bucket(index)

    def _split_bucket(self, index):
        bucket = self.buckets[index]
        #Caso em que o bucket esta cheio
        #Precisa aumentar o tamanho do global death
        if(bucket.local_depth == self.global_depth):
            self.buckets += self.buckets.copy() #Dobrando o tamaho
            self.global_depth += 1

            mask = (1 << self.global_depth) - 1 #Nova mask com tamanho atualizado

            new_bucket = Bucket(self.bucket_size, self.global_depth)

            old_bucket_values = bucket.values.copy()
            bucket.values.clear()
            idx_new_bucket = 0
            for (k,v) in old_bucket_values:
                idx = hash(k) & mask
                if idx == index:
                    self.buckets[idx].values.append((k, v))
                else:
                    idx_new_bucket = idx
                    new_bucket.values.append((k, v))
            self.buckets[idx_new_bucket] = new_bucket



    def __repr__(self):
        s = f"Global depth = {self.global_depth}\n"
        for i, b in enumerate(self.buckets):
            s += f"{i:0{self.global_depth}b}: {b}\n"
        return s


# Teste
h = ExtensibleHash(3)

h.insert(4, "Pão")
h.insert(24, "Leite")
h.insert(16, "Café")
h.insert(6, "Açúcar")
h.insert(22, "Queijo")
h.insert(10, "Manteiga")
h.insert(7, "Presunto")
h.insert(31, "Presunto")
h.insert(9, "Presunto")
h.insert(20, "Presunto")
h.insert(26, "Presunto")
print(h)