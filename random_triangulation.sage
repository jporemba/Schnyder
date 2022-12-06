from sage.graphs.schnyder import minimal_schnyder_wood

def generate(n, name):
    G = graphs.RandomTriangulation(n, True, 3)
    # G.plot(vertex_size=0, vertex_labels=False)

    newG = minimal_schnyder_wood(G)
    newG.edges(sort=True)
    # newG.plot(color_by_label={'red':'red','blue':'blue','green':'green',None:'black'})
    filename = f'{name}.edgelist'
    newG.export_to_file(filename, format='edgelist')

n = 2500
limit = 10
for i in range(1, limit + 1):
    generate(n, f'eval-n{n}-{i}')