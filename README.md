# Trabalho Prático 1 – Estruturas de Indexação: Hash Extensível e Árvore B+

## **Requisitos**

* **Python 3.x instalado** no sistema
* Não é necessário instalar bibliotecas externas

---

## **Como Executar o Projeto**

### **Executar a Árvore B+**

Dentro da pasta do projeto:

```bash
python b-tree/main.py
```

### **Executar o Hash Extensível**

```bash
python extensible-hash/ExtensibleHash.py
```

---

## **Como Usar Cada Programa**

Cada estrutura possui **3 loops (whiles)** no terminal, correspondentes às operações:

1. **Inserção**
2. **Busca**
3. **Remoção**

### **Funcionamento dos loops**

* Durante cada loop, você pode digitar quantos valores quiser.
* **Para sair de um loop e avançar para o próximo**, basta digitar:

```
end
```

### **Exibição da Estrutura**

Após **cada inserção ou remoção**, o sistema **mostra automaticamente** como a estrutura ficou:

* Na Árvore B+: exibe os nós atualizados
* Na Hash Extensível: exibe diretório, buckets e profundidades

---

## **Organização do Projeto**

```
/
├── b-tree/
│   ├── main.py
│   ├── ... (outros arquivos da Árvore B+)
│
└── extensible-hash/
    ├── ExtensibleHash.py
```

---

## **Descrição Resumida das Estruturas**

### **Árvore B+**

* Todas as chaves ficam nas folhas
* Nós internos armazenam apenas chaves de navegação

### **Hash Extensível**

* Utiliza hashing dinâmico com profundidades locais e globais
* Diretório dobra de tamanho conforme necessário
* Evita colisões por divisão de buckets




Após isso o programa avança para o próximo bloco de operações.

---

# Árvore B+ — Exemplo de Execução

### 🔹 **Código dos whiles (resumo do funcionamento):**

```python
print("Inserção de valores")
while True:
    a = input("Digite um valor: ")
    if a == 'end':
        break
    bpt.insert(int(a),'')
    bpt.display()

print("Busca por valores")
while True:
    a = input("Digite um valor buscar: ")
    if a == 'end':
        break
    print(bpt.search(int(a)))

print("Remover valores")
while True:
    a = input("Digite um valor remover: ")
    if a == 'end':
        break
    bpt.remove(int(a))
    bpt.display()
```

---

## **Exemplo — Inserção na Árvore B+**

Entrada:

```
Digite um valor: 3
```

Saída exibida:

```
Nível 0: (15 | 30 | 50) 
Nível 1: [3 | 5 | 10] [15 | 20] [30 | 40] [50 | 60]
```

---

## **Exemplo — Busca**

```
Digite um valor buscar: 15
```

*(Não mostra nada porque o método só retorna o valor associado à key — e aqui usamos strings vazias.)*

```
Digite um valor buscar: 0
-1
```

Valor `-1` significa que **a chave não foi encontrada na árvore**.

---

## **Exemplo — Remoção**

Entrada:

```
Digite um valor remover: 3
```

Saída:

```
Nível 0: (15 | 30 | 50) 
Nível 1: [5 | 10] [15 | 20] [30 | 40] [50 | 60]
```

---

# Hash Extensível — Exemplo de Execução

A Hash também tem 3 whiles: Inserção, Busca e Remoção.

A cada modificação, exibe o **diretório**, **profundidade dos buckets** e **os pares (chave, valor)** armazenados.

---

## **Exemplo de Inserção**

### Inserção 1:

```
Adicionar valor: 99
```

Saída:

```
0 : Bucket(ld=1, values=[(10, 'Livia'), (20, 'Livia'), (50, 'Livia')])
1 : Bucket(ld=1, values=[(5, 'Livia'), (15, 'Livia'), (99, 'Livia')])
```

### Inserção 2:

```
Adicionar valor: 40
```

Saída:

```
00 : Bucket(ld=2, values=[(20, 'Livia'), (40, 'Livia')])
01 : Bucket(ld=1, values=[(5, 'Livia'), (15, 'Livia'), (99, 'Livia')])
10 : Bucket(ld=2, values=[(10, 'Livia'), (50, 'Livia')])
11 : Bucket(ld=1, values=[(5, 'Livia'), (15, 'Livia'), (99, 'Livia')])
```

---

## **Exemplo — Busca**

### Valor inexistente

```
Buscar valor: 999
Procurando por chave: 999: None
```

### Valor existente

```
Buscar valor: 20
Procurando por chave: 20: Livia
```

---

## **Exemplo — Remoção**

Entrada:

```
Remover valor: 20
```

Saída:

```
Valor 20 foi removido: True
00 : Bucket(ld=2, values=[(40, 'Livia')])
01 : Bucket(ld=1, values=[(5, 'Livia'), (15, 'Livia'), (99, 'Livia')])
10 : Bucket(ld=2, values=[(10, 'Livia'), (50, 'Livia')])
11 : Bucket(ld=1, values=[(5, 'Livia'), (15, 'Livia'), (99, 'Livia')])
```
