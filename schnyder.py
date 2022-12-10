import networkx as nx

from colour import *

class Woods:
    # It is optional to include the bounding triangle in the coloured edges - it will not affect anything.
    # However, they must still be present in G itself.

    def __init__(self, G, red_root, red_edges, green_root, green_edges, blue_root, blue_edges):
        self.G = G
        self.n = G.number_of_nodes()
        
        self.roots = {red_root, green_root, blue_root}
        
        self.red_root = red_root
        self.red_tree = nx.DiGraph()
        self.red_tree.add_nodes_from(G.nodes)
        self.red_tree.add_edges_from(red_edges)
        
        self.green_root = green_root
        self.green_tree = nx.DiGraph()
        self.green_tree.add_nodes_from(G.nodes)
        self.green_tree.add_edges_from(green_edges)
        
        self.blue_root = blue_root
        self.blue_tree = nx.DiGraph()
        self.green_tree.add_nodes_from(G.nodes)
        self.blue_tree.add_edges_from(blue_edges)
        
        self.tree_map = {
            Colour.RED: self.red_tree,
            Colour.BLUE: self.blue_tree,
            Colour.GREEN: self.green_tree
        }
        
        self.root_map = {
            Colour.RED: self.red_root,
            Colour.BLUE: self.blue_root,
            Colour.GREEN: self.green_root
        }
    
    def root(self, colour):
        return self.root_map[colour]
    
    def parent(self, colour, node):
        if node in self.roots:
            raise Exception(f'Cannot take {colour.name} parent of root {node}')
        parents = list(self.tree_map[colour].successors(node))
        assert len(parents) == 1, f'node {node} has {colour.name} parents {parents}'
        return parents[0]
    
    def children(self, colour, node):
        return list(self.tree_map[colour].predecessors(node))
    
    # Path nodes
    
    def path_nodes(self, colour, node):
        if node == self.root(col_prev(colour)) or node == self.root(col_next(colour)):
            raise Exception('Cannot find path for other coloured roots')
        current = node
        path = [current]
        while current not in self.roots:
            current = self.parent(colour, current)
            path.append(current)
        return path

def memoizer(map, fn, input):
    if input not in map:
        map[input] = fn(input)
    return map[input]

def memoizer2(map2, fn2, inputx, inputy):
    if inputy not in map2[inputx]:
        map2[inputx][inputy] = fn2(inputx, inputy)
    return map2[inputx][inputy]

# Class for computing schnyder coordinates
class Data:
    
    def __init__(self, woods):
        self.woods = woods
        
        self.subtree_size_map = {
            Colour.RED: dict(),
            Colour.BLUE: dict(),
            Colour.GREEN: dict()
        }
        
        self.region_size_nodes_map = {
            Colour.RED: dict(),
            Colour.BLUE: dict(),
            Colour.GREEN: dict()
        }
        
        self.path_length_map = {
            Colour.RED: dict(),
            Colour.BLUE: dict(),
            Colour.GREEN: dict()
        }
        
        self.subtree_size_path_sum_map = {
            (Colour.RED, Colour.BLUE): dict(),
            (Colour.RED, Colour.GREEN): dict(),
            (Colour.BLUE, Colour.RED): dict(),
            (Colour.BLUE, Colour.GREEN): dict(),
            (Colour.GREEN, Colour.RED): dict(),
            (Colour.GREEN, Colour.BLUE): dict(),
        }
        
        self.region_size_triangles_map = {
            Colour.RED: dict(),
            Colour.BLUE: dict(),
            Colour.GREEN: dict()
        }
    
    # Subtree size in number of nodes
    def subtree_size(self, colour, node):
        return memoizer2(self.subtree_size_map, self.compute_subtree_size, colour, node)
    
    def compute_subtree_size(self, colour, node):
        if node == self.woods.root(colour):
            return self.woods.n
        elif node in self.woods.roots:
            return 1
        else:
            # Internal node
            children = self.woods.children(colour, node)
            if len(children) == 0:
                return 1
            else:
                return sum([self.subtree_size(colour, child) for child in children]) + 1

    # Subtree path sums
    # First colour is subtree, second colour is path
    
    def subtree_size_path_sum(self, col_tree, col_path, node):
        return memoizer2(self.subtree_size_path_sum_map, self.compute_subtree_size_path_sum, (col_tree, col_path), node)
    
    def compute_subtree_size_path_sum(self, col_tuple, node):
        col_tree, col_path = col_tuple
        if node == self.woods.root(col_path):
            return self.subtree_size(col_tree, node)
        else:
            return self.subtree_size_path_sum(col_tree, col_path, self.woods.parent(col_path, node)) + self.subtree_size(col_tree, node)
    
    # Region size in number of nodes
    
    def region_size_nodes(self, colour, node):
        return memoizer2(self.region_size_nodes_map, self.compute_region_size_nodes, colour, node)
        
    def compute_region_size_nodes(self, colour, node):
        if node == self.woods.root(colour):
            return self.woods.n
        elif node in self.woods.roots:
            return 1
        else:
            col_prev_contribution = self.subtree_size_path_sum(colour, col_prev(colour), node)
            col_next_contribution = self.subtree_size_path_sum(colour, col_next(colour), node)
            return col_prev_contribution + col_next_contribution - self.subtree_size(colour, node)
    
    # Path length in number of edges
    
    def path_length(self, colour, node):
        return memoizer2(self.path_length_map, self.compute_path_length, colour, node)
    
    def compute_path_length(self, colour, node):
        if node == self.woods.root(colour):
            return 0
        else:
            return self.path_length(colour, self.woods.parent(colour, node)) + 1
    
    # Region size in number of triangles
    
    def region_size_triangles(self, colour, node):
        return memoizer2(self.region_size_triangles_map, self.compute_region_size_triangles, colour, node)
    
    def compute_region_size_triangles(self, colour, node):
        if node == self.woods.root(colour):
            return 2 * self.woods.n - 5
        elif node in self.woods.roots:
            return 0
        else:
            n_nodes = self.region_size_nodes(colour, node)
            exterior_cycle_length = self.path_length(col_prev(colour), node) + self.path_length(col_next(colour), node) + 1
            return 2 * n_nodes - 2 - exterior_cycle_length

class Schnyder:
    
    def __init__(self, G, red_root, red_edges, green_root, green_edges, blue_root, blue_edges):
        self.G = G
        self.woods = Woods(G, red_root, red_edges, green_root, green_edges, blue_root, blue_edges)
        self.data = Data(self.woods)