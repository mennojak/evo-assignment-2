from models.graph import Graph 

def main():
    print("Select experiment:")
    print("1 - flat300 with 28 colors- section 2")
    print("2 - flat300 with 26 colors - section 2")
    print("3 - flat1000 with 100 colors- section 3")
    print("4 - flat1000 with 83 colors - section 3")
    print("5 - flat300 with 26 colors varying population size and descent cycles - section 4.1")
    print("6 - flat1000 with 83 colors, population size and descent cycles based on experiment 5 - section 4.2")
    print("7 - flat300 with 26 colors test ILS using Vertex descent - section 4.3")
    print("8 - flat1000 with 83 colors test ILS using Vertex descent (only if experiment 7 successful) - section 4.3")
    print("9 - Custom experiment: TBD - section 4.4")


    choice = input("Enter 1-9: ")

    if choice == "1":
        graph = Graph("data/flat300_26_0.col")
        colors = 28
        population_size = 50
        descent_cycles = 100
        print("TODO")

    if choice == "2":
        graph = Graph("data/flat300_26_0.col")
        colors = 26
        population_size = 50
        descent_cycles = 100
        print("TODO")
    
    if choice == "3":
        graph = Graph("data/flat1000_76_0.col")
        colors = 100
        population_size = 50
        descent_cycles = 100
        print("TODO")

    if choice == "4":
        graph = Graph("data/flat1000_76_0.col")
        colors = 83
        population_size = 50
        descent_cycles = 100
        print("TODO")
    
    if choice == "5":
        graph = Graph("data/flat300_26_0.col")
        colors = 26
        population_size = int(input("Choose population size: "))
        descent_cycles = int(input("Choose descent cycles: "))

        print("TODO")
    
    if choice == "6":
        graph = Graph("data/flat1000_76_0.col")
        colors = 83
        population_size = 50
        descent_cycles = 100
        print("TODO")

    if choice == "7":
        graph = Graph("data/flat300_26_0.col")
        colors = 26
        population_size = int(input("Choose population size: "))
        descent_cycles = int(input("Choose descent cycles: "))
        ils = True
        print("TODO")

    if choice == "8":
        graph = Graph("data/flat1000_76_0.col")
        colors = 83
        population_size = 50
        descent_cycles = 100
        ils = True
        print("TODO")

    if choice == "9":
        # TBD
        graph = Graph("data/flat300_26_0.col")
        # graph = Graph("data/flat1000_76_0.col")
        colors = 26
        # colors = 83
        population_size = 0
        descent_cycles = 0    
        print("TODO")

if __name__ == "__main__":    
    main()