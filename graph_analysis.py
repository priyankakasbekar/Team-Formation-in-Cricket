import networkx as nx
import csv
import matplotlib.pyplot as plt
import operator
import random

nodes = []
edges = []
with open('/Users/vkannan/Documents/CS286 Social Networks/project/PlayervsPlayer_Countries/player_records_West Indies.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    for row in reader:
        nodes.append(row[0])
        edges.append(tuple(row[:2]))

G = nx.Graph() # Initialize a Graph object
G.add_nodes_from(nodes) # Add nodes to the Graph
G.add_edges_from(edges) # Add edges to the Graph
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), label=nodes)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', arrows=True)
# plt.show()

density = nx.density(G)
triadic_closure = nx.transitivity(G)
clustering_coefficient = nx.average_clustering(G)

#degree centrality
degree_dict = nx.degree_centrality(G)

#betweenness centrality
betweenness_dict = nx.betweenness_centrality(G)

#closeness centrality
closeness_dict = nx.closeness_centrality(G)

clustering_dict = nx.clustering(G)

average_path_length = nx.average_shortest_path_length(G)

print(nx.info(G))
print("Network density:", density)
print("Triadic closure:", triadic_closure)
print("Clustering coefficient:", clustering_coefficient)
print("Average path length:", average_path_length)
print("")
print("Node, Degree centrality, Betweenness centrality, Closeness centrality", "Clustering coefficient")

for n in G.nodes():
    print(n, degree_dict[n], betweenness_dict[n], closeness_dict[n], clustering_dict[n])

rnd_graph = nx.gnp_random_graph(108, 0.4)
APL = nx.average_shortest_path_length(rnd_graph)
density = nx.density(rnd_graph)
triadic_closure = nx.transitivity(rnd_graph)
clustering_coefficient = nx.average_clustering(rnd_graph)

print APL, density, triadic_closure, clustering_coefficient
