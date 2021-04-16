import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time

input_data = pd.read_csv('Adjacency.csv', index_col=0)
G = nx.Graph(input_data.values)

s1= int(input('Enter a starting location: ' ))
d1=s2=2
d2=s3=15
d3=0

start = time.time()
path1=nx.shortest_path(G, source=s1, target=d1)
path2=nx.shortest_path(G, source=s2, target=d2)
path3=nx.shortest_path(G, source=s3, target=d3)
print('iron -> ',path1,'wood -> ',path2,'factory -> ',path3)

ln1=nx.shortest_path_length(G, source=s1, target=d1)
ln2=nx.shortest_path_length(G, source=s2, target=d2)
ln3=nx.shortest_path_length(G, source=s3, target=d3)
print('Total number of steps to complete the task = ',ln1+ln2+ln3)

nx.draw_spectral(G,with_labels = True)
#plt.show()

end = time.time()
print("Execution time => %s seconds" % (end - start))
