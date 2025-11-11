from BPlusTree import BPlusTree

def main():
    # Cria uma árvore de ordem 4 (por exemplo)
    bpt = BPlusTree(order=4)

    # Insere algumas chaves
    a = [
        (20, "A"), (10, "B"), (30, "C"), (40, "D"),
        (50, "E"), (60, "F"), (35, "G"), (25, "H"),
        (15, "E"), (5, "F"), (45, "G"), (55, "H"),
        (70, "E"), (80, "F"), (75, "G"), (85, "H"),
        (90, "E"), (95, "F")
    ]

    #a = [20,10,30,40,50,60,35,3,25,15,45]
    #for k, v in dados:
    for i, _ in a:
        #i = input("Enter a number: ")
        bpt.insert(i, "a")
        bpt.display()

if __name__ == "__main__":
    main()
