import networkx as nx
import time

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

def schnyder_direction_sig(woods, src, dest):
    r_direction = sign(woods.region_size_triangles_red(dest) - woods.region_size_triangles_red(src))
    g_direction = sign(woods.region_size_triangles_green(dest) - woods.region_size_triangles_green(src))
    b_direction = sign(woods.region_size_triangles_blue(dest) - woods.region_size_triangles_blue(src))
    return {'red': r_direction, 'green': g_direction, 'blue': b_direction}

def schnyder_direction_sig_pessimistic(woods, src, dest):
    r_direction = sign_pessimistic(woods.region_size_triangles_red(dest) - woods.region_size_triangles_red(src))
    g_direction = sign_pessimistic(woods.region_size_triangles_green(dest) - woods.region_size_triangles_green(src))
    b_direction = sign_pessimistic(woods.region_size_triangles_blue(dest) - woods.region_size_triangles_blue(src))
    return {'red': r_direction, 'green': g_direction, 'blue': b_direction}

pure_red = {'red': +1, 'green': -1, 'blue': -1}
pure_green = {'red': -1, 'green': +1, 'blue': -1}
pure_blue = {'red': -1, 'green': -1, 'blue': +1}

anti_red = {'red': -1, 'green': +1, 'blue': +1}
anti_green = {'red': +1, 'green': -1, 'blue': +1}
anti_blue = {'red': +1, 'green': +1, 'blue': -1}

def schnyder_next(G, woods, src, dest):
    src_neighbours = G.adj[src]
    # print(src_neighbours)
    if dest in src_neighbours:
        return dest
    else:
        sig = schnyder_direction_sig_pessimistic(woods, src, dest)
        # print(f'p-sig: {sig}')
        if sig == pure_red:
            return woods.red_parent(src)
        elif sig == pure_green:
            return woods.green_parent(src)
        elif sig == pure_blue:
            return woods.blue_parent(src)
        elif sig == anti_red:
            for neighbour in src_neighbours:
                sig_neighbour_dest = schnyder_direction_sig(woods, neighbour, dest)
                sig_src_neighbour = schnyder_direction_sig(woods, src, neighbour)
                if sig_neighbour_dest == anti_red and sig_src_neighbour['red'] == -1:
                    return neighbour
            raise Exception(f'No suitable neighbour found. P-sig: {sig}')
        elif sig == anti_green:
            for neighbour in src_neighbours:
                sig_neighbour_dest = schnyder_direction_sig(woods, neighbour, dest)
                sig_src_neighbour = schnyder_direction_sig(woods, src, neighbour)
                if sig_neighbour_dest == anti_green and sig_src_neighbour['green'] == -1:
                    return neighbour
            raise Exception(f'No suitable neighbour found. P-sig: {sig}')
        elif sig == anti_blue:
            for neighbour in src_neighbours:
                sig_neighbour_dest = schnyder_direction_sig(woods, neighbour, dest)
                sig_src_neighbour = schnyder_direction_sig(woods, src, neighbour)
                if sig_neighbour_dest == anti_blue and sig_src_neighbour['blue'] == -1:
                    return neighbour
            raise Exception(f'No suitable neighbour found. P-sig: {sig}')
        else:
            raise Exception(f'Pessimistic signature invalid. P-sig: {sig}')
        
def schnyder_local_route(G, woods, src, dest):
    current = src
    path = []
    while(current != dest):
        # time.sleep(1)
        # print(current)
        next = schnyder_next(G, woods, current, dest)
        path.append((current,next))
        current = next
    return path

def fixed_dest_routing_tree(G, woods, dest):
    T = nx.DiGraph()
    T.add_nodes_from(G.nodes)
    for node in G.nodes:
        if node != dest:
            next = schnyder_next(G, woods, node, dest)
            T.add_edge(node, next)
    return T