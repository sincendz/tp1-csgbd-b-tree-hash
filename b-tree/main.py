from BPlusTree import BPlusTree

def main():
    # Cria uma árvore de ordem 4 (por exemplo)
    bpt = BPlusTree(order=4)

    # Insere algumas chaves
    a = [
        (20, "A"),
        (10, "B"),
        (30, "C"),
        (40, "D"),
        (50, "E"),
        (60, "F"),
        (35, "G"),
        (25, "H"),
        (15, "E"),
        (5, "F"),
        (45, "G"),
        (55, "H"),
        (70, "E"),
        (80, "Mario"),
        (75, "G"),
        (85, "H"),
        (90, "E"),
        (95, "Fruta"),
    ]

    # for k, v in dados:
    for i, v in a:
        bpt.insert(i, v)

    print(bpt.remove(85))

    bpt.display()

if __name__ == "__main__":
    main()
