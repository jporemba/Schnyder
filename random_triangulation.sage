from sage.graphs.schnyder import minimal_schnyder_wood

G = graphs.RandomTriangulation(100, True, 3)
# filename = "test1.pajek"
# G.export_to_file(filename)
# G.plot(vertex_size=0, vertex_labels=False)

newG = minimal_schnyder_wood(G)
newG.edges(sort=True)
# newG.plot(color_by_label={'red':'red','blue':'blue','green':'green',None:'black'})
filename = "eval-n100-1.edgelist"
newG.export_to_file(filename, format='edgelist')