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


    def remove_from_leaf(self, key, leaf, parent_stack):
        if key not in leaf.keys:
            return False

        key_index = leaf.keys.index(key) #index da chave na folha
        leaf.keys.pop(key_index)
        leaf.values.pop(key_index)

        # Caso 1: folha ainda tem o mínimo → apenas checar se a chave existe nos
        #nós internos
        if leaf.has_minimum_keys or leaf == self.root:
            parent_stack.pop()
            replace_to = leaf.keys[0]
            while parent_stack:
                parent = parent_stack.pop()
                if key in parent.keys:
                    idx = parent.keys.index(key)
                    parent.keys.insert(idx,replace_to)
                    break
            return True



        # Caso 2: folha ficou abaixo do mínimo → tentar redistribuição ou merge
        if len(parent_stack) <= 1:
            return True
        parent_stack.pop()
        parent = parent_stack[-1]

        idx = parent.nodes.index(leaf)
        print(key, f"idx: {idx}")
        left_sibling = parent.nodes[idx - 1] if idx > 0 else None
        right_sibling = parent.nodes[idx + 1] if idx < len(parent.nodes) - 1 else None

        # Tenta emprestar do irmão esquerdo
        if left_sibling and len(left_sibling.keys) > math.ceil(self.order / 2) - 1:
            borrowed_key = left_sibling.keys.pop(-1)
            borrowed_value = left_sibling.values.pop(-1)
            leaf.keys.insert(0, borrowed_key)
            leaf.values.insert(0, borrowed_value)
            parent.keys[idx - 1] = leaf.keys[0]
            return True

        # Tenta emprestar do irmão direito
        elif right_sibling and len(right_sibling.keys) > math.ceil(self.order / 2) - 1:
            print("vai pegar irmao direito")
            borrowed_key = right_sibling.keys.pop(0)
            borrowed_value = right_sibling.values.pop(0)
            print(f"Chave que vai pegar: {borrowed_key}")
            leaf.keys.append(borrowed_key)
            leaf.values.append(borrowed_value)
            parent.keys[idx] = right_sibling.keys[0]
            print(parent.keys, key, borrowed_key)
            #Aqui tem que fazer um search do index
            #Pegar o valor que está em leaf posição 0 e substituir onde tiver tbm
            replace_to = leaf.keys[0]
            print(replace_to, parent_stack[1].keys)
            while parent_stack:
                parent = parent_stack.pop()
                if key in parent.keys:
                    print("Achou")
                    idx = parent.keys.index(key)
                    parent.keys[idx]=replace_to
                    break
            return True

        # Nenhum irmão pode emprestar
        elif left_sibling:
            left_sibling.keys.extend(leaf.keys)
            left_sibling.values.extend(leaf.values)
            left_sibling.next = leaf.next
            parent.keys.pop(idx - 1)
            parent.nodes.pop(idx)
        elif right_sibling:
            leaf.keys.extend(right_sibling.keys)
            leaf.values.extend(right_sibling.values)
            leaf.next = right_sibling.next
            parent.keys.pop(idx)
            parent.nodes.pop(idx + 1)

        

        return True

    def remove(self, key: int):
        parent_stack = []
        node = self.root
        parent_stack.append(node)

        # Caminho até a folha
        while isinstance(node, Internal):
            i = 0
            while i < node.keys_size and key >= node.get_key_by_index(i):
                i += 1
            parent_stack.append(node.nodes[i])
            node = node.nodes[i]

        # Agora node é uma folha
        return self.remove_from_leaf(key, node, parent_stack)
