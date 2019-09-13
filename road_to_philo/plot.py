import networkx as nx
from networkx.readwrite import json_graph
import pickle
import math
import json
import matplotlib.pyplot as plt
from os import path

DATA_PATH = path.join(path.dirname(path.dirname(__file__)), 'crawlerData')

with open(DATA_PATH, 'rb') as f:
    g = pickle.load(f)

fig = plt.figure(figsize=[100,100])
nx.spring_layout(g, k=0.15/math.sqrt(g.order()), iterations=20)
nx.draw(g, with_labels=True, node_color='#ADD8E6')

data = json_graph.node_link_data(g)
with open('graph.json', 'w') as f:
    json.dump(data,f)
plt.show()