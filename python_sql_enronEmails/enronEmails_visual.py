# prepare for Python version 3x features and functions
from __future__ import division, print_function
import networkx as nx
import matplotlib.pyplot as plt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print(os.getcwd())
os.path.exists('./plot_input.csv')

f = open('plot_input.csv', 'rb')

g = nx.read_edgelist(f, create_using = nx.DiGraph(), delimiter = ',', nodetype = str)
f.close()

# print graph attributes
print('This is a directed network/graph (True or False): ', g.is_directed())
print('Number of nodes: ', nx.number_of_nodes(g))
print('Number of edges: ', nx.number_of_edges(g))
print('Network density: ', round(nx.density(g), 4))
# determine the total number of links for the network 

# plot the degree distribution 
fig = plt.figure()
plt.hist(nx.degree(g).values())
plt.axis([0, 8, 0, 8])
plt.xlabel('Node Degree')
plt.ylabel('Frequency')
plt.show()
    
# examine alternative layouts for plotting the network 
# plot the network/graph with default layout 
fig = plt.figure()
nx.draw_networkx(g, node_size = 200, font_color='blue', edge_color = 'red',  node_color = 'yellow')

# spring layout
fig = plt.figure()
nx.draw_networkx(g, node_size = 200, node_color = 'yellow', font_color='blue', edge_color = 'red',\
    pos = nx.spring_layout(g))
plt.show()

# circlular layout
fig = plt.figure()
nx.draw_networkx(g, node_size = 200, node_color = 'yellow', font_color='blue', edge_color = 'red', \
    pos = nx.circular_layout(g))
plt.show()

# shell/concentric circles layout
fig = plt.figure()
nx.draw_networkx(g, node_size = 200, node_color = 'yellow', font_color='blue', edge_color = 'red', \
    pos = nx.shell_layout(g))
plt.show()

# pick the visualization that you prefer and route that to external pdf file
fig = plt.figure()
nx.draw_networkx(g, node_size = 200, node_color = 'yellow', font_color='blue', edge_color = 'red', \
    pos = nx.shell_layout(g))
plt.savefig('sample_plot.pdf', bbox_inches = 'tight', dpi = None,
    facecolor = 'w', edgecolor = 'b', orientation = 'portrait', 
    papertype = None, format = None, pad_inches = 0.25, frameon = None)