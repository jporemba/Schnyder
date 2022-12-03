import networkx as nx
import schnyder
import localroute
import evaluation
import statistics

nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Trees 
red_root = 9
red_edges = [
    (1, 9),
    (8, 9),
    (5, 9),
    (6, 8),
    (7, 8),
    (4, 7),
    (3, 5)
]

green_root = 2
green_edges = [
    (3, 2),
    (5, 2),
    (9, 2),
    (4, 3),
    (7, 5),
    (8, 5),
    (6, 4)
]

blue_root = 1
blue_edges = [
    (8, 1),
    (6, 1),
    (4, 1),
    (3, 1),
    (2, 1),
    (7, 6),
    (5, 4)
]

# Coordinates
red_coords = {
    1: 0,
    2: 0,
    3: 1,
    4: 2,
    5: 4,
    6: 3,
    7: 7,
    8: 10,
    9: 13
}

green_coords = {
    1: 0,
    2: 13,
    3: 10,
    4: 5,
    5: 8,
    6: 2,
    7: 3,
    8: 1,
    9: 0
}

blue_coords = {
    1: 13,
    2: 0,
    3: 2,
    4: 6,
    5: 1,
    6: 8,
    7: 3,
    8: 2,
    9: 0
}

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(red_edges)
G.add_edges_from(green_edges)
G.add_edges_from(blue_edges)

if __name__ == '__main__':
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(red_edges)
    G.add_edges_from(green_edges)
    G.add_edges_from(blue_edges)

    print(G)

    W = schnyder.Woods(G, red_root, red_edges, green_root, green_edges, blue_root, blue_edges)
    print(f'Blue parent of 7: {W.blue_parent(7)}')

    # C = schnyder.Coords(G, red_coords, green_coords, blue_coords)

    # for node in G.nodes:
    #     print(f'{node}: {C.phi(node)}')

    path = localroute.schnyder_local_route(G, W, 5, 8)
    print(f'Path from 5 -> 8: {path}')

    path = localroute.schnyder_local_route(G, W, 3, 8)
    print(f'Path from 3 -> 8: {path}')

    path = localroute.schnyder_local_route(G, W, 2, 6)
    print(f'Path from 2 -> 6: {path}')

    path = localroute.schnyder_local_route(G, W, 4, 9)
    print(f'Path from 4 -> 9: {path}')

    path = localroute.schnyder_local_route(G, W, 3, 7)
    print(f'Path from 4 -> 9: {path}')

    path = localroute.schnyder_local_route(G, W, 6, 5)
    print(f'Path from 4 -> 9: {path}')

    distortion = evaluation.evaluate_routing_protocol(G, W)
    print(f'Min distortion: {min(distortion.values())}')
    print(f'Max distortion: {max(distortion.values())}')
    # for value in distortion.values():
    #     print(value)

    print(W.subtree_size_red(8))

    print(W.path_nodes_green(6))

    print("node counting:")

    print(W.region_size_nodes_red(7))
    print(W.region_size_nodes_blue(7))
    print(W.region_size_nodes_green(7))

    print("triangle counting:")

    print(W.region_size_triangles_red(7))
    print(W.region_size_triangles_red(8))

    print(W.region_size_triangles_blue(7))
    print(W.region_size_triangles_blue(8))

    print(W.region_size_triangles_green(7))
    print(W.region_size_triangles_green(8))

    print("testing")

    for node in G.nodes:
        # print(node)
        assert W.region_size_triangles_red(node) == red_coords[node]
        assert W.region_size_triangles_blue(node) == blue_coords[node]
        assert W.region_size_triangles_green(node) == green_coords[node]