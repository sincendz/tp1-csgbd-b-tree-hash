from BPlusTree import BPlusTree
import random

def main():
    # Cria uma árvore de ordem 4 (por exemplo)
    bpt = BPlusTree(order=4)

    #Caso a professora queira inserir valores aletorios,
    # eh so remover o comentario
    #a = [i for i in range(15)]
    #random.shuffle(a)
    # a = [1,2,3,4]
    # for ele in a:
    #     bpt.insert(int(ele),'')

    #Inserção dos valores
    print("Inserção de valores")
    while True:
        a = input("Digite um valor: ")
        if a == 'end':
            break
        bpt.insert(int(a),'')
        bpt.display()

    #Busca dos valores
    print("Busca por valores")
    while True:
        a = input("Digite um valor buscar: ")
        if a == 'end':
            break
        print(bpt.search(int(a)))

    #Remoção
    print("Remover valores")
    while True:
        a = input("Digite um valor remover: ")
        if a == 'end':
            break
        bpt.remove(int(a))
        bpt.display()

if __name__ == "__main__":
    main()
