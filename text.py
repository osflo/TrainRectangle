import igraph

G=igraph.Graph()
G.add_vertices(6)
G.add_edges([(0,1), (2,3),(3,4),(2,5)])
V=G.clusters()
for cluster in V:
    print("....")
    for v in cluster:
        print(v)
print(V)