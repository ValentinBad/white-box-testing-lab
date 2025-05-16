import ast
import networkx as nx
from matplotlib import pyplot as plt

with open("auth.py", "r") as f:
    code = f.read()

tree = ast.parse(code)
func = tree.body[0]  # перша функція у файлі

G = nx.DiGraph()
prev_nodes = []
counter = 0

for stmt in func.body:
    label = ast.unparse(stmt)
    node = f"n{counter}"
    G.add_node(node, label=label)
    for prev in prev_nodes:
        G.add_edge(prev, node)
    prev_nodes = [node]
    counter += 1

# Вивести всі прості шляхи
paths = list(nx.all_simple_paths(G, source="n0", target=prev_nodes[0]))
print("Шляхи виконання (all_simple_paths):")
for path in paths:
    print(path)

# Записати у .dot файл
nx.nx_pydot.write_dot(G, "cfg.dot")

# Розрахунок цикломатичної складності
M = G.number_of_edges() - G.number_of_nodes() + 2
print("Циклматична складність:", M)
