import networkx as nx
import time
from colour import Colour

def sign(a):
    if a > 0:
        return 1
    elif a == 0:
        return 0
    else:
        return -1
    
def sign_pessimistic(a):
    if a > 0:
        return 1
    else:
        return -1

def schnyder_direction_sig(S, src, dest):
    r_direction = sign(S.data.region_size_triangles(Colour.RED, dest) - S.data.region_size_triangles(Colour.RED, src))
    b_direction = sign(S.data.region_size_triangles(Colour.BLUE, dest) - S.data.region_size_triangles(Colour.BLUE, src))
    g_direction = sign(S.data.region_size_triangles(Colour.GREEN, dest) - S.data.region_size_triangles(Colour.GREEN, src))
    return {Colour.RED: r_direction, Colour.GREEN: g_direction, Colour.BLUE: b_direction}

def schnyder_direction_sig_pessimistic(S, src, dest):
    r_direction = sign_pessimistic(S.data.region_size_triangles(Colour.RED, dest) - S.data.region_size_triangles(Colour.RED, src))
    b_direction = sign_pessimistic(S.data.region_size_triangles(Colour.BLUE, dest) - S.data.region_size_triangles(Colour.BLUE, src))
    g_direction = sign_pessimistic(S.data.region_size_triangles(Colour.GREEN, dest) - S.data.region_size_triangles(Colour.GREEN, src))
    return {Colour.RED: r_direction, Colour.GREEN: g_direction, Colour.BLUE: b_direction}

pure_red = {Colour.RED: +1, Colour.GREEN: -1, Colour.BLUE: -1}
pure_blue = {Colour.RED: -1, Colour.GREEN: -1, Colour.BLUE: +1}
pure_green = {Colour.RED: -1, Colour.GREEN: +1, Colour.BLUE: -1}

pure_sig = {
    Colour.RED: pure_red,
    Colour.BLUE: pure_blue,
    Colour.GREEN: pure_green
}

anti_red = {Colour.RED: -1, Colour.GREEN: +1, Colour.BLUE: +1}
anti_blue = {Colour.RED: +1, Colour.GREEN: +1, Colour.BLUE: -1}
anti_green = {Colour.RED: +1, Colour.GREEN: -1, Colour.BLUE: +1}

anti_sig = {
    Colour.RED: anti_red,
    Colour.BLUE: anti_blue,
    Colour.GREEN: anti_green
}

def find_suitable_neighbour(G, S, src, dest, src_neighbours, colour):
    for neighbour in src_neighbours:
        sig_neighbour_dest = schnyder_direction_sig(S, neighbour, dest)
        sig_src_neighbour = schnyder_direction_sig(S, src, neighbour)
        if sig_neighbour_dest == anti_sig[colour] and sig_src_neighbour[colour] == -1:
            return neighbour
    raise Exception(f'No suitable neighbour found.')

def schnyder_next(G, S, src, dest):
    src_neighbours = G.adj[src]
    # print(src_neighbours)
    if dest in src_neighbours:
        return dest
    else:
        sig = schnyder_direction_sig_pessimistic(S, src, dest)
        # print(f'p-sig: {sig}')
        for colour in Colour:
            if sig == pure_sig[colour]:
                return S.woods.parent(colour, src)
            elif sig == anti_sig[colour]:
                return find_suitable_neighbour(G, S, src, dest, src_neighbours, colour)
        raise Exception(f'Pessimistic signature invalid. P-sig: {sig}')
        
def schnyder_local_route(G, S, src, dest):
    current = src
    path = []
    while(current != dest):
        # time.sleep(1)
        # print(current)
        next = schnyder_next(G, S, current, dest)
        path.append((current,next))
        current = next
    return path

def fixed_dest_routing_tree(G, S, dest):
    T = nx.DiGraph()
    T.add_nodes_from(G.nodes)
    for node in G.nodes:
        if node != dest:
            next = schnyder_next(G, S, node, dest)
            T.add_edge(node, next)
    return T