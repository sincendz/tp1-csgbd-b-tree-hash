from BPlusTree import BPlusTree

def main():
    # Cria uma árvore de ordem 4 (por exemplo)
    bpt = BPlusTree(order=4)

    # Insere algumas chaves
    # a = [
    #     (20, "A"),
    #     (10, "B"),
    #     (30, "C"),
    #     (40, "D"),
    #     (50, "E"),
    #     (60, "F"),
    #     (35, "G"),
    #     (25, "H"),
    #     (15, "E"),
    #     (5, "F"),
        # (45, "G"),
        # (55, "H"),
        # (70, "E"),
        # (80, "Mario"),
        # (75, "G"),
        # (85, "H"),
        # (90, "E"),
        # (95, "Fruta"),
    # ]

    a = [ 5 , 10 , 15, 20 , 25, 30 , 35 , 40, 50 , 60 ]

    # for k, v in dados:
    for i in a:
        bpt.insert(i, "v")

    bpt.remove(25)
    bpt.remove(30)

    #bpt.display()

    # bpt.remove(5)
    # bpt.remove(10)
    # bpt.remove(15)
    # bpt.remove(25)
    # bpt.remove(35)
    # bpt.remove(30)
    # bpt.remove(85)
    # bpt.remove(90)
    # bpt.remove(60)
    # bpt.remove(70)
    # bpt.remove(95)
    # bpt.remove(45)
    # bpt.remove(50)
    bpt.display()

if __name__ == "__main__":
    main()
