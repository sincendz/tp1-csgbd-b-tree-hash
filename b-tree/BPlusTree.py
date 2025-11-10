import math
from leaf_node import Leaf
from internal_node import Internal


class BPlusTree:
    def __init__(self, order):
        if order < 3:
            raise ValueError("O valor de order tem que ser maior ou igual a 3!")
        self.order = order
        self.root = Leaf(order)

    def insert_in_leaf(self, leaf: Leaf, key, value):
        i = 0
        while i < leaf.keys_size and key > leaf.get_key_by_index(i):
            i += 1
        if leaf.get_key_by_index(i) == key:
            leaf.values[i] = value
        else:
            leaf.keys.insert(i, key)
            leaf.values.insert(i, value)
        return leaf

    def split_internal(self, node: Internal, parent_stack):
        mid = math.ceil( node.keys_size / 2)
        promoted_key = node.get_key_by_index(mid)

        left = Internal(self.order)
        right = Internal(self.order)

        left.keys = node.keys[:mid]
        left.nodes = node.nodes[: mid + 1]

        right.keys = node.keys[mid + 1:]
        right.nodes = node.nodes[mid + 1:]

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

    def split_leaf(self, leaf: Leaf, parent_stack=[]):
        new_leaf = Leaf(self.order)
        mid = math.ceil(leaf.keys_size / 2)

        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]

        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]

        leaf.next = new_leaf
        # Folha é root
        if not parent_stack:
            internal = Internal(self.order)
            internal.keys = [new_leaf.keys[0]]
            internal.nodes = [leaf, new_leaf]
            leaf.next = new_leaf
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
                self.split_leaf(leaf)
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

    # def search(self, key):
    """Retorna o valor associado à chave, se existir."""
    # pass

    # def remove(self, key: int) -> bool:
    """Remove a chave informada da árvore."""
    # return True

    # def display(self):
    """Exibe a estrutura da árvore (nós internos e folhas)."""
    # pass
