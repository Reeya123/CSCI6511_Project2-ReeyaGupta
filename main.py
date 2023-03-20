##800.txt

from typing import List, Tuple
from collections import defaultdict


class MyGraph:
    def __init__(self, nodes: List[int]):
        self.nodes = nodes
        self.adj_list = defaultdict(list)

    def add_edge(self, u: int, v: int) -> dict:
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)


def parse_input_file() -> Tuple[MyGraph, int]:
    input_file = open("input.txt", "r")
    word = 'colors'
    nodes = []
    edges = []
    for line in input_file.readlines():
        if line.startswith('#'):
            continue  # we are skipping comments
        if word in line:
            num_colors = int(line.split()[2])
        else:
            adj = list(map(int, line.split(',')))
            nodes += adj
            edges.append(adj)
    graph = MyGraph(set(nodes))
    for u, v in edges:
        graph.add_edge(u, v)
    return graph, num_colors


def csp_coloring(graph: MyGraph, num_colors: int) -> dict:
    domains = {v: set(range(num_colors)) for v in graph.nodes}
    constraints = {(u, v): lambda x, y: x != y for u in graph.nodes for v in graph.adj_list[u]}

    def order_domain_values(variable: str) -> List[int]:
        return sorted(domains[variable], key=lambda val: sum(
            int(''.join(map(str, domains[neighbor]))) for neighbor in graph.adj_list[variable] if
            neighbor not in assignment))

    def select_unassigned_variable() -> str:
        return min(set(graph.nodes) - set(assignment), key=lambda var: len(domains[var]))

    def backtrack() -> dict:
        if len(assignment) == len(graph.nodes):
            return assignment
        var = select_unassigned_variable()
        for value in order_domain_values(var):
            if all(constraints[(var, neighbor)](value, assignment[neighbor]) for neighbor in graph.adj_list[var] if
                   neighbor in assignment):
                assignment[var] = value
                inferences = {(neighbor, var) for neighbor in graph.adj_list[var] if neighbor not in assignment}
                if ac3(inferences):
                    result = backtrack()
                    if result is not None:
                        return result
                del assignment[var]
                for neighbor in inferences:
                    domains[neighbor[0]].add(neighbor[1])
        return None

    def ac3(queue: set) -> bool:
        while queue:
            u, v = queue.pop()
            if remove_inconsistent_values(u, v):
                if not domains[u]:
                    return False
                queue |= {(u, neighbor) for neighbor in graph.adj_list[u] if neighbor != v}
        return True

    def remove_inconsistent_values(u: str, v: str) -> bool:
        removed = False
        for x in domains[u].copy():
            if all(not constraints[(u, v)](x, y) for y in domains[v]):
                domains[u].remove(x)
                removed = True
        return removed

    assignment = {}
    return backtrack()
if __name__ == '__main__':
    
    graph, num_colors = parse_input_file()
    solution = csp_coloring(graph, num_colors)
    print(solution)
    if solution is not None:
        print('Solution:')
        for vertex, color in solution.items():
            print(f'Vertex {vertex}: Color {color}')
    else:
        print('No solution could be found')
