from BPlusTree import BPlusTree

def main():
    # Cria uma árvore de ordem 4 (por exemplo)
    bpt = BPlusTree(order=4)

    # a = [0,1,2,3,60,70,5,6,7]
    a = [1,2,3,4]
    for ele in a:
        bpt.insert(ele,'')

    bpt.display()
    # bpt.insert(62,'')
    # bpt.display()
    # return

    while True:
        a = input()
        if a == 'end':
            break
        bpt.insert(int(a),'')
        bpt.display()
if __name__ == "__main__":
    main()
