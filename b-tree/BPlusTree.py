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
        if leaf.get_key_by_index(i) == value:
            leaf.values[i] = value
        else:
            leaf.keys.insert(i, key)
            leaf.values.insert(i, value)
        return leaf

    def split_leaf(self, leaf: Leaf):
        # Criação do novo nó folha
        new_leaf = Leaf(self.order)

        # Meio do nó
        mid = math.ceil(leaf.keys_size / 2)

        # Popula o novo nó folha com os valores de key e value
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]

        # Atualiza os valores da folha que estava cheia
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]

        # Cria o no interno
        internal = Internal(self.order)
        # Adiciona a chave do meio do nó que estava cheio para ser a nova chave do nó interno
        internal.keys = [new_leaf.keys[0]]

        # Adição do nos folhas na lista de filhos de no interno
        internal.nodes = [leaf, new_leaf]

        leaf.next = new_leaf

        return internal

    def insert(self, key, value):
        # Percorrer a arvore procurando por onde o nó deve entrar
        # Quando achar vejo se está cheio
        # Se tiver cheio, faço o split recursivo
        # Se não tiver, adiciono na árvore
        """Insere um par (chave, valor) na árvore B+."""
        root = self.root
        # Caso 1, inserir em uma folha
        if isinstance(root, Leaf):
            leaf = self.insert_in_leaf(root, key, value)
            # Folha cheia
            if leaf.is_full:
                self.root = self.split_leaf(leaf)  # Root é nó interno
        else:
            parent_stack = []
            node = root
            while isinstance(node, Internal):
                parent_stack.append(node)
                i = 0
                while i < node.keys_size and key >= node.get_key_by_index(i):
                    i += 1
                node = node.nodes[i]
            leaf = node

        # def search(self, key):
        """Retorna o valor associado à chave, se existir."""
        # pass

        # def remove(self, key: int) -> bool:
        """Remove a chave informada da árvore."""
        # return True

        # def display(self):
        """Exibe a estrutura da árvore (nós internos e folhas)."""
        # pass
