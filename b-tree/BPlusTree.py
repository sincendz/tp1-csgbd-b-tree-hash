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

    #Ok
    def insert_in_leaf(self, leaf: Leaf, key, value):
        i = 0
        #percorre a folha para encontrar a posição correta de inserir o novo elemento
        while i < leaf.keys_size and key >= leaf.get_key_by_index(i):
            i += 1
        #Checa se ele já existe
        if i < leaf.keys_size and leaf.get_key_by_index(i) == key:
            leaf.values[i] = value
        else:
            leaf.keys.insert(i, key)
            leaf.values.insert(i, value)
        return leaf

    def split_internal(self, node: Internal, parent_stack):
        #mid = math.ceil(node.keys_size / 2)
        #Quando número foi impar pega o elemento do meio
        mid = node.keys_size // 2

        #Chave que vai subir
        promoted_key = node.get_key_by_index(mid)

        left = Internal(self.order)
        right = Internal(self.order)

        #Nó esquerdo recebe os valores menores que mid
        left.keys = node.keys[:mid]
        left.nodes = node.nodes[: mid + 1]

        #Nó direito os valores maiores que mid,
        #mid não precisa ficar em nenhum dos dois
        #pq eh nó interno
        right.keys = node.keys[mid + 1 :]
        right.nodes = node.nodes[mid + 1 :]

        #Ok, show aqui
        if not parent_stack:
            new_root = Internal(self.order)
            new_root.keys = [promoted_key]
            new_root.nodes = [left, right]
            self.root = new_root
            return
        # Nó tem um pai
        parent = parent_stack.pop()
        #Acha onde estava o nó passado
        idx = parent.nodes.index(node)
        parent.nodes[idx] = left
        parent.nodes.insert(idx + 1, right)
        parent.keys.insert(idx, promoted_key)

        if parent.is_full:
            self.split_internal(parent, parent_stack)

    def insert_in_internal(self, internal: Internal, leaf: Leaf, parent_stack):
        i = 0
        new_key = leaf.keys[0] #chave que será adicionada para chegar no nó
        #Busca pela posição que a chave vai ficar
        while i < internal.keys_size and new_key > internal.get_key_by_index(i):
            i += 1
        #Adiciona o valor na posição correta
        internal.keys.insert(i, new_key)
        internal.nodes.insert(i + 1, leaf)
        if internal.is_full:
            #internal = node que estamos usando, parent_stack = 'pais do nó'
            #na parent stack não tem o nó interno pois foi feito um pop dele
            #na chamada dessa função insert_in_internal
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
        #Caso em que a folha não eh root
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
        node = self.root
        leaf = None
        #Busca a folha
        while isinstance(node,Internal):
            i = 0
            while i < node.keys_size and key >= node.get_key_by_index(i):
                i+=1
            node = node.nodes[i]
        leaf = node
        for i,_ in enumerate(leaf.keys):
            if(leaf.get_key_by_index(i) == key):
                return leaf.values[i]
        return -1

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

    def _rebalance_internal(self, parent_stack):
        node = parent_stack.pop()

        # Caso especial: se o nó for a raiz e não tiver chaves
        if node == self.root and len(node.keys) == 0:
            # A raiz só pode ter 0 chaves se tiver um único filho
            if len(node.nodes) == 1:
                self.root = node.nodes[0]
            return

        parent = parent_stack[-1] if parent_stack else None
        if not parent:
            return  # Nada a fazer se não houver pai

        idx = parent.nodes.index(node)
        left_sibling = parent.nodes[idx - 1] if idx > 0 else None
        right_sibling = parent.nodes[idx + 1] if idx < len(parent.nodes) - 1 else None

        # Tenta redistribuir com irmão à esquerda
        if left_sibling and len(left_sibling.keys) > math.ceil(self.order / 2) - 1:
            # Puxa chave do irmão esquerdo para o nó atual
            borrowed_key = left_sibling.keys.pop(-1)
            borrowed_child = left_sibling.nodes.pop(-1)

            # Atualiza a chave do pai
            parent_key = parent.keys[idx - 1]
            parent.keys[idx - 1] = borrowed_key

            # Insere chave e filho no início do nó atual
            node.keys.insert(0, parent_key)
            node.nodes.insert(0, borrowed_child)
            return

        # Tenta redistribuir com irmão à direita
        elif right_sibling and len(right_sibling.keys) >math.ceil(self.order / 2) - 1:
            borrowed_key = right_sibling.keys.pop(0)
            borrowed_child = right_sibling.nodes.pop(0)

            parent_key = parent.keys[idx]
            parent.keys[idx] = borrowed_key

            node.keys.append(parent_key)
            node.nodes.append(borrowed_child)
            return

        # Caso contrário, precisa fundir com um dos irmãos
        if left_sibling:
            # Junta o irmão esquerdo + chave do pai + o nó atual
            merge_key = parent.keys.pop(idx - 1)
            left_sibling.keys.append(merge_key)
            left_sibling.keys.extend(node.keys)
            left_sibling.nodes.extend(node.nodes)

            # Remove o ponteiro do nó fundido
            parent.nodes.pop(idx)
        elif right_sibling:
            merge_key = parent.keys.pop(idx)
            node.keys.append(merge_key)
            node.keys.extend(right_sibling.keys)
            node.nodes.extend(right_sibling.nodes)
            parent.nodes.pop(idx + 1)

        # Após o merge, pode ser necessário continuar subindo o rebalanceamento
        if len(parent.keys) < math.ceil(self.order / 2) - 1:
            self._rebalance_internal(parent_stack)

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
                    parent.keys[idx] = replace_to
                    break
            return True



        # Caso 2: folha ficou abaixo do mínimo → tentar redistribuição ou merge
        # parent = parent_stack[-2] if len(parent_stack) >= 2 else None
        # if not parent:
        #     return True  # era a raiz

        if len(parent_stack) <= 1:
            return True
        parent_stack.pop()
        parent = parent_stack[-1]
        

        idx = parent.nodes.index(leaf)
        left_sibling = parent.nodes[idx - 1] if idx > 0 else None
        right_sibling = parent.nodes[idx + 1] if idx < len(parent.nodes) - 1 else None

        # Tenta emprestar do irmão esquerdo
        if left_sibling and len(left_sibling.keys) > math.ceil(self.order / 2) - 1:
            print("oi")
            borrowed_key = left_sibling.keys.pop(-1)
            borrowed_value = left_sibling.values.pop(-1)
            print(key, borrowed_key)
            leaf.keys.insert(0, borrowed_key)
            leaf.values.insert(0, borrowed_value)
            parent.keys[idx - 1] = leaf.keys[0]
            # replace_to = leaf.keys[0]
            # while parent_stack:
            #     parent = parent_stack.pop()
            #     if key in parent.keys:
            #         idx = parent.keys.index(key)
            #         parent.keys[idx] = replace_to
            #         break
            # return True

        # Tenta emprestar do irmão direito
        elif right_sibling and len(right_sibling.keys) > math.ceil(self.order / 2) - 1:
            borrowed_key = right_sibling.keys.pop(0)
            borrowed_value = right_sibling.values.pop(0)
            leaf.keys.append(borrowed_key)
            leaf.values.append(borrowed_value)
            parent.keys[idx] = right_sibling.keys[0]
            #Aqui tem que fazer um search do index
            #Pegar o valor que está em leaf posição 0 e substituir onde tiver tbm
            replace_to = leaf.keys[0]
            while parent_stack:
                parent = parent_stack.pop()
                if key in parent.keys:
                    idx = parent.keys.index(key)
                    parent.keys[idx]=replace_to
                    break
            return True

        # Nenhum irmão pode emprestar → merge
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

        # Se o pai ficou abaixo do mínimo, ajustar recursivamente
        if not parent.has_minimum_keys:
            self._rebalance_internal(parent_stack)

        return True

    def remove(self, key: int):
        parent_stack = []
        node = self.root
        parent_stack.append(node)

        # Caminho até a folha
        while isinstance(node, Internal):
            i = 0
            # >=
            while i < node.keys_size and key > node.get_key_by_index(i):
                i += 1
            parent_stack.append(node.nodes[i])
            node = node.nodes[i]

        # Agora node é uma folha
        return self.remove_from_leaf(key, node, parent_stack)
