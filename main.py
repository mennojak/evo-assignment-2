import time
from models.graph import Graph 
from gls_algorithm import genetic_local_search
from evaluation import EvaluationResult

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

    # not used for report
    if choice == "1":
        colors = 28
        population_size = 50
        descent_cycles = 100
        print("start time:", time.ctime())
        best_solution, generation_results = genetic_local_search("data/flat300_26_0.col", colors, population_size, descent_cycles)
        print("end time:", time.ctime())
        evaluation = EvaluationResult(generation_results)
        evaluation.plot()

    # not used for report
    if choice == "2":
        graph = Graph()
        graph.create_from_file("data/flat300_26_0.col")
        colors = 26
        population_size = 50
        descent_cycles = 100
        print("TODO")
    
    if choice == "3":
        graph = Graph()
        graph.create_from_file("data/flat1000_76_0.col")
        colors = 100
        population_size = 50
        descent_cycles = 100
        print("TODO")

    if choice == "4":
        graph = Graph()
        graph.create_from_file("data/flat1000_76_0.col")
        colors = 83
        population_size = 50
        descent_cycles = 100
        print("TODO")
    
    if choice == "5":
        graph = Graph()
        graph.create_from_file("data/flat300_26_0.col")
        colors = 26
        population_size = int(input("Choose population size: "))
        descent_cycles = int(input("Choose descent cycles: "))

        print("TODO")
    
    if choice == "6":
        graph = Graph()
        graph.create_from_file("data/flat1000_76_0.col")
        colors = 83
        population_size = 50
        descent_cycles = 100
        print("TODO")

    if choice == "7":
        graph = Graph()
        graph.create_from_file("data/flat300_26_0.col")
        colors = 26
        population_size = int(input("Choose population size: "))
        descent_cycles = int(input("Choose descent cycles: "))
        ils = True
        print("TODO")

    if choice == "8":
        graph = Graph()
        graph.create_from_file("data/flat1000_76_0.col")
        colors = 83
        population_size = 50
        descent_cycles = 100
        ils = True
        print("TODO")

    if choice == "9":
        # TBD
        graph = Graph()
        graph.create_from_file("data/flat300_26_0.col")
        # graph = Graph()
        # graph.create_from_file("data/flat1000_76_0.col")
        colors = 26
        # colors = 83
        population_size = 0
        descent_cycles = 0    
        print("TODO")

if __name__ == "__main__":    
    main()