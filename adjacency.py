import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

input_data = pd.read_csv('Adjacency.csv', index_col=0)
#print(input_data.values)
G = nx.Graph(input_data.values)

labeldict = {}
labeldict[0] = "e"
labeldict[1] = "m1"
labeldict[2] = "f1"
labeldict[3] = "m2"
labeldict[4] = "m3"
labeldict[5] = "b"

labeldict[6] = "m4"
labeldict[7] = "m5"
labeldict[8] = "m6"
labeldict[9] = "m7"
labeldict[10] = "m8"
labeldict[11] = "m9"

labeldict[12] = "m10"
labeldict[13] = "d1"
labeldict[14] = "m11"
labeldict[15] = "a1"
labeldict[16] = "m12"
labeldict[17] = "s"

labeldict[18] = "m13"
labeldict[19] = "m14"
labeldict[20] = "m15"
labeldict[21] = "m16"
labeldict[22] = "m17"
labeldict[23] = "m18"

labeldict[24] = "m19"
labeldict[25] = "d2"
labeldict[26] = "m20"
labeldict[27] = "m21"
labeldict[28] = "m22"
labeldict[29] = "a2"

labeldict[30] = "c"
labeldict[31] = "m23"
labeldict[32] = "f2"
labeldict[33] = "m24"
labeldict[34] = "m25"
labeldict[35] = "m26"

nx.draw_spectral(G, labels=labeldict, with_labels = True, nodelist=[0,5,17,30], node_size=500, node_color='orange',font_size=10)
nx.draw_spectral(G, labels=labeldict, with_labels = True, nodelist=[2,13,15,25,29,32], node_size=500, node_color='yellow',font_size=10)
nx.draw_spectral(G, labels=labeldict, with_labels = True, nodelist=[1,3,4,6,7,8,9,10,11,12,14,16,18,19,20,21,22,23,24,26,27,28,31,33,34,35], node_size=500, node_color='#11cc77',font_size=10)

#print(list(G.nodes))
#print(list(G.edges))
#nx.draw_spectral(G,with_labels = True)

plt.draw()
plt.show()
#plt.savefig("mine_layout.png")
