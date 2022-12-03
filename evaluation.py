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
