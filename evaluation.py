import networkx as nx
import schnyder
import localroute

def evaluate_routing_protocol(G, woods):
    true_distance = dict()
    routing_distance = dict()
    distortion = dict()
    for s in G.nodes:
        for t in G.nodes:
            if s != t:
                true_distance[(s, t)] = nx.shortest_path_length(G, s, t)
                routing_distance[(s, t)] = len(localroute.schnyder_local_route(G, woods, s, t))
                distortion[(s, t)] = routing_distance[(s, t)] / true_distance[(s, t)]
            
    return distortion

def evaluate_routing_protocol_faster(G, woods):
    true_distance = dict()
    routing_distance = dict()
    distortion = dict()
    for t in G.nodes:
        T = localroute.fixed_dest_routing_tree(G, woods, t)
        nodes = [t]
        i = 0
        while len(nodes) > 0:
            i += 1
            next_nodes = []
            for node in nodes:
                next_nodes.extend(list(T.predecessors(node)))
            for s in next_nodes:
                true_distance[(s, t)] = nx.shortest_path_length(G, s, t)
                routing_distance[(s, t)] = i
                distortion[(s, t)] = routing_distance[(s, t)] / true_distance[(s, t)]
            nodes = next_nodes
    return distortion

def parse_edgelist_to_woods(filename):
    input = nx.read_edgelist(filename,nodetype=int,create_using=nx.DiGraph())
    # print(input.edges(data=True))
    
    red_edges = []
    blue_edges = []
    green_edges = []
    
    for edge in input.edges(data=True):
        (u, v, attr) = edge
        if attr['weight'] == 'red':
            red_edges.append(edge)
        elif attr['weight'] == 'blue':
            blue_edges.append(edge)
        elif attr['weight'] == 'green':
            green_edges.append(edge)
        else:
            raise Exception("Unexpected edge colour")
    
    G = nx.Graph()
    G.add_nodes_from(input.nodes)
    G.add_edges_from(input.edges)
    # Add back in the exterior edges, which sage removes for some reason
    G.add_edges_from([(-1, -2), (-2, -3), (-3, -1)])
    # -1 = green root, -2 = blue root, -3 = red root
    W = schnyder.Woods(G, -3, red_edges, -1, green_edges, -2, blue_edges)
    return (G, W)

if __name__ == '__main__':
    tests = [
        # 'eval-n100-1.edgelist',
        # 'eval-n100-2.edgelist',
        # 'eval-n100-3.edgelist',
        # 'eval-n500-1.edgelist',
        # 'eval-n500-2.edgelist',
        # 'eval-n500-3.edgelist',
        'eval-n1000-1.edgelist',
    ]

    for test in tests:
        print(f'Test: {test}')
        G, W = parse_edgelist_to_woods(test)
        # print(G.edges)
        distortion = evaluate_routing_protocol_faster(G, W)
        print(f'Min distortion: {min(distortion.values())}')
        print(f'Max distortion: {max(distortion.values())}')