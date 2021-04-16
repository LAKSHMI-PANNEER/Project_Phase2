import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

input_data = pd.read_csv('Adjacency.csv', index_col=0)
G = nx.Graph(input_data.values)

s = int(input('Enter the source node: ' ))
d = int(input('Enter the destination node: ' ))

path=nx.shortest_path(G, source=s, target=d)
print('shortest path from source to destination:',path)

ln=nx.shortest_path_length(G, source=s, target=d)
print('number of steps to reach destination = ',ln)

nx.draw_spectral(G,with_labels = True)
plt.show()

'''
sources = [21,15]
destinations = [15,5]
res = []
for s in sources:
    for d in destinations:
        res.append((s, d, nx.shortest_path(G, source=s, target=d)))
        print(res)
       
'''
