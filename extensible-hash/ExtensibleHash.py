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
    def __init__(self, bucket_size: int, global_depth: int = 2):
        self.bucket_size = bucket_size
        self.global_depth = global_depth
        self.buckets = [Bucket(bucket_size, self.global_depth) for _ in range(2 ** self.global_depth)]

    def _hash(self, key):
        shift = (1 << self.global_depth)
        return key % shift

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
            #Bucket cheio passa a ter um novo tamanho de local_depth
            bucket.local_depth = self.global_depth

            #Pegar os valores do index passado e passalos na nova
            #função de hash para colocalos no local correto
            #Valores do bucket que passatam na nova função
            values_bucket = bucket.values.copy()
            #Novo bucket para guardar os novos valores
            new_bucket = Bucket(self.bucket_size, bucket.local_depth)
            #Limpar os valores do bucket cheio
            bucket.values.clear()
            #Para cada key nos valores do bucket cheio acha uma nova posição para ele
            idx_new_bucket = 0
            for (k,v) in values_bucket:
                idx = self._hash(k)
                #Caso os novo mapemaento seja igual ao antigo
                #Adiciona no mesmo lugar
                if idx == index:
                    self.buckets[idx].values.append((k, v))
                else: # Adição no novo bucket
                    idx_new_bucket = idx
                    new_bucket.values.append((k, v))
            #Com o novo bucket populado, faz o insert
            self.buckets[idx_new_bucket] = new_bucket
        else:
            #Caso em que o global depth é maior que o local,
            #ou seja, existem posições livres


            #Criação de um novo bucket para os novos valores
            new_bucket = Bucket(self.bucket_size, bucket.local_depth)
            values_bucket = bucket.values.copy()
            bucket.values.clear()
            new_index = 0
            for (k,v) in values_bucket:
                idx =self._hash(k)
                if idx == index:
                    self.buckets[idx].values.append((k, v))
                else:
                    new_bucket.values.append((k, v))
                    new_index = idx
            self.buckets[new_index] = new_bucket
            #Ao final atualizar o valor de bucket para 3
            bucket.local_depth = self.global_depth

    def search(self, key: int) -> any:
        """Retorna o valor associado à chave, se existir."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for (k,v) in bucket.values:
            if k == key:
                return v


    def remove(self, key: int) -> bool:
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k,v) in enumerate(bucket.values):
            if k == key:
                bucket.values.pop(i)
                return True
        return  False

    def display(self):
        for i , bucket in enumerate(self.buckets):
            binary = bin(i)[2:]
            if len(binary) < self.global_depth:
                binary = "0"*(self.global_depth - len(binary)) + binary
            print(f"{binary} : {bucket}" )

# Teste
h = ExtensibleHash(3,1)

#Adicao de valores
print("Adição de valores")
while True:
    a = input("Adicionar valor: ")
    if a == "end":
        break
    h.insert(int(a),"Livia")
    h.display()


#Busca por valores
print("Busca por valores: ")
while True:
    key = input("Buscar valor: ")
    if key == "end":
        break
    print(f"Procurando por chave: {key}: {h.search(int(key))}")

print("Remover os valores: ")
h.display()
while True:
    key = input("Remover valor: ")
    if key == "end":
        break
    print(f"Valor {key} foi removido: {h.remove(int(key))}")
    h.display()