from BPlusTree import BPlusTree

def main():
    # Cria uma árvore de ordem 4 (por exemplo)
    bpt = BPlusTree(order=4)

    a = [0,1,2,3,60,70,5,6,7]
    # a = [1,2,3,4]
    for ele in a:
        bpt.insert(int(ele),'')

    bpt.display()
    # bpt.insert(62,'')
    # bpt.display()
    # return

    # print("Inserção de valores")
    # while True:
    #     a = input("Digite um valor: ")
    #     if a == 'end':
    #         break
    #     bpt.insert(int(a),'')
    #     bpt.display()

    print("Busca por valores")
    while True:
        a = input("Digite um valor buscar: ")
        if a == 'end':
            break
        print(bpt.search(int(a)))

if __name__ == "__main__":
    main()
