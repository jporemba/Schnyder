import networkx as nx
import schnyder
import localroute
import sys
from multiprocessing import Pool

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
    routing_distance = dict()
    distortion = dict()
    for t in G.nodes:
        T = localroute.fixed_dest_routing_tree(G, woods, t)
        true_dist_to_t = dict(nx.single_target_shortest_path_length(G, t))
        nodes = [t]
        i = 0
        while len(nodes) > 0:
            i += 1
            next_nodes = []
            for node in nodes:
                next_nodes.extend(list(T.predecessors(node)))
            for s in next_nodes:
                routing_distance[(s, t)] = i
                distortion[(s, t)] = routing_distance[(s, t)] / true_dist_to_t[s]
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

def evaluate_test(test):
    G, W = parse_edgelist_to_woods(test)
    # print(G.edges)
    distortion = evaluate_routing_protocol_faster(G, W)
    # print(f'Min distortion: {min(distortion.values())}')
    # print(f'Max distortion: {max(distortion.values())}')
    return (min(distortion.values()), max(distortion.values()))

if __name__ == '__main__':
    flush = True
    tests = [f'eval-n{n}-{i}.edgelist' for n in [2000] for i in range(1, 10+1)]

    # Sequential
    # for test in tests:
    #     print(f'Test: {test}')
        
    #     mini, maxi = evaluate_test(test)
    #     print(f'Min distortion: {mini}')
    #     print(f'Max distortion: {maxi}')
    #     if flush:
    #         sys.stdout.flush()
    
    # Parallel
    with Pool(processes=5) as pool:
        results = pool.map(evaluate_test, tests)
    
    for i in range(0, len(tests)):
        print(f'Test: {tests[i]}')
        mini, maxi = results[i]
        print(f'Min distortion: {mini}')
        print(f'Max distortion: {maxi}')