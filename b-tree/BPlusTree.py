import math
from leaf_node import Leaf
from internal_node import Internal
from collections import deque


class BPlusTree:
    def __init__(self, order):
        if order < 3:
            raise ValueError("O valor de order tem que ser maior ou igual a 3!")
        self.order = order
        self.root = Leaf(order)

    def insert_in_leaf(self, leaf: Leaf, key, value):
        i = 0
        while i < leaf.keys_size and key >= leaf.get_key_by_index(i):
            i += 1
        if i < leaf.keys_size and leaf.get_key_by_index(i) == key:
            leaf.values[i] = value
        else:
            leaf.keys.insert(i, key)
            leaf.values.insert(i, value)
        return leaf

    def split_internal(self, node: Internal, parent_stack):
        mid = math.ceil(node.keys_size / 2)

        promoted_key = node.get_key_by_index(mid)

        left = Internal(self.order)
        right = Internal(self.order)

        left.keys = node.keys[:mid]
        left.nodes = node.nodes[: mid + 1]

        right.keys = node.keys[mid + 1 :]
        right.nodes = node.nodes[mid + 1 :]

        if not parent_stack:
            new_root = Internal(self.order)
            new_root.keys = [promoted_key]
            new_root.nodes = [left, right]
            self.root = new_root
            return

        parent = parent_stack.pop()
        idx = parent.nodes.index(node)
        parent.nodes[idx] = left
        parent.nodes.insert(idx + 1, right)
        parent.keys.insert(idx, promoted_key)

        if parent.is_full:
            self.split_internal(parent, parent_stack)

    def insert_in_internal(self, internal: Internal, leaf: Leaf, parent_stack):
        i = 0
        new_key = leaf.keys[0]
        while i < internal.keys_size and new_key > internal.get_key_by_index(i):
            i += 1
        internal.keys.insert(i, new_key)
        internal.nodes.insert(i + 1, leaf)
        if internal.is_full:
            self.split_internal(internal, parent_stack)

    def split_leaf(self, leaf: Leaf, parent_stack):
        new_leaf = Leaf(self.order)
        mid = math.ceil(leaf.keys_size / 2)

        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]

        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]

        new_leaf.next = leaf.next
        leaf.next = new_leaf
        # Folha é root
        if not parent_stack:
            internal = Internal(self.order)
            internal.keys = [new_leaf.keys[0]]
            internal.nodes = [leaf, new_leaf]
            self.root = internal
            return
        parent = parent_stack.pop()
        self.insert_in_internal(parent, new_leaf, parent_stack)

    def insert(self, key, value):
        """Insere um par (chave, valor) na árvore B+."""
        root = self.root
        # Caso 1, inserir em uma folha
        if isinstance(root, Leaf):
            leaf = self.insert_in_leaf(root, key, value)
            # Folha cheia
            if leaf.is_full:
                self.split_leaf(leaf, [])
        else:
            # Caso em que o root é um nó interno
            parent_stack = []  # Caminho do nó até a folha
            node = root
            while isinstance(node, Internal):
                parent_stack.append(node)
                i = 0
                while i < node.keys_size and key > node.get_key_by_index(i):
                    i += 1
                node = node.nodes[i]
            leaf = node
            self.insert_in_leaf(leaf, key, value)
            if leaf.is_full:
                self.split_leaf(leaf, parent_stack)

    def search(self, key):
        root = self.root
        while True:
            i = 0
            while i < root.keys_size and key > root.get_key_by_index(i):
                i += 1
            if isinstance(root, Leaf):
                if i >= root.keys_size:
                    return -1
                if root.get_key_by_index(i) == key:
                    return root.values[i]
                return -1
            root = root.nodes[i]

    def display(self):
        """Exibe a estrutura da árvore (nós internos e folhas)."""
        if not self.root:
            print("Árvore vazia.")
            return

        queue = deque()
        queue.append((self.root, 0))  # (nó, nível)
        current_level = 0

        print(f"Nível {current_level}:", end=" ")

        while queue:
            node, level = queue.popleft()

            # Se mudou de nível
            if level > current_level:
                current_level = level
                print(f"\nNível {current_level}:", end=" ")

            # Mostra o nó atual
            if isinstance(node, Leaf):
                print(f"[{' | '.join(map(str, node.keys))}]", end=" ")
            elif isinstance(node, Internal):
                print(f"({' | '.join(map(str, node.keys))})", end=" ")

                # Adiciona os filhos na fila
                for child in node.nodes:
                    queue.append((child, level + 1))

        print("\n")


    def adjust_internal_index(self, index_to_search ,new_index_key, parent_stack):
        while parent_stack:
            node = parent_stack.pop()
            #Caso o elemento que vou remover esteja em um nó interno
            if index_to_search in node.keys:
                idx = node.keys.index(index_to_search)
                node.keys.pop(idx)
                node.keys.insert(idx, new_index_key)
                if not node.internal_has_the_minimum_keys:
                    #Aqui vem merda
                    pass

    def remove_from_leaf(self, key, node, parent_stack):
        if key in node.keys:  # Busca pela chave
            # Achou o elemento, agora é hora de excluir ele da folha
            key_index = node.keys.index(key)
            node.keys.pop(key_index)
            node.values.pop(key_index)

            new_internal_velue = -1
            if node.keys_size > 0:
                new_internal_velue = node.get_key_by_index(0)
            else:
                next_node = node.next
                node.keys.append(next_node.keys[0]) #Adicionando o menor valor do next node no node atual
                node.values.append(next_node.values[0])
                next_node.keys.pop(0)
                next_node.values.pop(0)
                new_index = next_node.keys[0]

                #Tira a folha da stack
                parent_stack.pop()
                parent_node = parent_stack.pop()
                #Lembrar de botar na lista
                parent_stack.append(parent_node)
                idx_parent_node_new_value = parent_node.nodes.index(node)
                parent_node.keys[idx_parent_node_new_value] = new_index

                new_internal_velue = node.keys[0]
                #Adiciona leaf
                parent_stack.append(node)
            # Valor retirado da folha e tem mais valores que o minimo
            if (node.leaf_has_the_minimum_keys):
                # Procura no nos internos se o nó que vai ser retirado existe
                #new_internal_value represta o valor pelo que o nó será substituido nos index
                parent_stack.pop()
                self.adjust_internal_index(key, new_internal_velue, parent_stack);
            else:
                print("Chegou na merda")
                # Aqui vem merda
                pass
            return True
        else:
            # Chave de busca não encontrada
            return False

    def remove(self, key: int):
        # Nó com caminho até a folha
        parent_stack = []
        node = self.root
        parent_stack.append(node)

        # Caminho até a folha que contem o nó
        while True:
            # index dos nodes
            i = 0
            while i < node.keys_size and key >= node.get_key_by_index(i):
                i += 1
            # Caso o no seja um interno
            if isinstance(node, Internal):
                node = node.nodes[i]
                parent_stack.append(node)
            else:
                # Chegou em uma folha
                return self.remove_from_leaf(key,node,parent_stack)

