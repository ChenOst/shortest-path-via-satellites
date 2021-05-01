import matplotlib.pyplot as plt
import networkx as nx


def main():
    print("Hello from Main Function")
    G = nx.Graph()
    G.add_edge('A', 'B', weight=4)
    G.add_edge('B', 'D', weight=2)
    G.add_edge('A', 'C', weight=3)
    G.add_edge('C', 'D', weight=4)
    print(nx.shortest_path(G, 'A', 'D', weight='weight'))


if __name__ == "__main__":
    main()
