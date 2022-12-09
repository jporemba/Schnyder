import networkx as nx

from enum import Enum

# Colours
class Colour(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    
# Cyclic ordering on colours
    
col_next_map = {
    Colour.RED: Colour.BLUE,
    Colour.BLUE: Colour.GREEN,
    Colour.GREEN: Colour.RED
}

col_prev_map = {
    Colour.RED: Colour.GREEN,
    Colour.BLUE: Colour.RED,
    Colour.GREEN: Colour.BLUE
}
    
def col_next(colour):
    return col_next_map[colour]

def col_prev(colour):
    return col_prev_map[colour]

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
        
        self.region_size_nodes_red_map = dict()
        self.region_size_nodes_blue_map = dict()
        self.region_size_nodes_green_map = dict()
        
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
        
    def parent(self, colour, node):
        if node in self.roots:
            raise Exception(f'Cannot take {colour.name} parent of root {node}')
        parents = list(self.tree_map[colour].successors(node))
        assert len(parents) == 1, f'node {node} has {colour.name} parents {parents}'
        return parents[0]
    
    def red_parent(self, node):
        return self.parent(Colour.RED, node)
    
    def green_parent(self, node):
        return self.parent(Colour.GREEN, node)
    
    def blue_parent(self, node):
        return self.parent(Colour.BLUE, node)
    
    # Subtree size in number of nodes
    def subtree_size(self, colour, node):
        return memoizer2(self.subtree_size_map, self.compute_subtree_size, colour, node)
    
    def compute_subtree_size(self, colour, node):
        if node == self.root_map[colour]:
            return self.n
        elif node in self.roots:
            return 1
        else:
            # Internal node
            children = list(self.tree_map[colour].predecessors(node))
            if len(children) == 0:
                return 1
            else:
                return sum([self.subtree_size(colour, child) for child in children]) + 1
            
    def subtree_size_red(self, node):
        return self.subtree_size(Colour.RED, node)
    
    def subtree_size_blue(self, node):
        return self.subtree_size(Colour.BLUE, node)
    
    def subtree_size_green(self, node):
        return self.subtree_size(Colour.GREEN, node)
    
    # Path nodes
    
    def path_nodes(self, colour, node):
        if node == self.root_map[col_prev(colour)] or node == self.root_map[col_next(colour)]:
            raise Exception('Cannot find path for other coloured roots')
        current = node
        path = [current]
        while current not in self.roots:
            current = self.parent(colour, current)
            path.append(current)
        return path

    def path_nodes_red(self, node):
        return self.path_nodes(Colour.RED, node)
    
    def path_nodes_blue(self, node):
        return self.path_nodes(Colour.BLUE, node)
    
    def path_nodes_green(self, node):
        return self.path_nodes(Colour.GREEN, node)
    
    # Subtree path sums
    # First colour is subtree, second colour is path
    
    def subtree_size_path_sum(self, col_tree, col_path, node):
        return memoizer2(self.subtree_size_path_sum_map, self.compute_subtree_size_path_sum, (col_tree, col_path), node)
    
    def compute_subtree_size_path_sum(self, col_tuple, node):
        col_tree, col_path = col_tuple
        if node == self.root_map[col_path]:
            return self.subtree_size(col_tree, node)
        else:
            return self.subtree_size_path_sum(col_tree, col_path, self.parent(col_path, node)) + self.subtree_size(col_tree, node)
    
    def subtree_size_path_sum_red_blue(self, node):
        return self.subtree_size_path_sum(Colour.RED, Colour.BLUE, node)
        
    def subtree_size_path_sum_red_green(self, node):
        return self.subtree_size_path_sum(Colour.RED, Colour.GREEN, node)
    
    def subtree_size_path_sum_blue_red(self, node):
        return self.subtree_size_path_sum(Colour.BLUE, Colour.RED, node)

    def subtree_size_path_sum_blue_green(self, node):
        return self.subtree_size_path_sum(Colour.BLUE, Colour.GREEN, node)
    
    def subtree_size_path_sum_green_red(self, node):
        return self.subtree_size_path_sum(Colour.GREEN, Colour.RED, node)

    def subtree_size_path_sum_green_blue(self, node):
        return self.subtree_size_path_sum(Colour.GREEN, Colour.BLUE, node)
    
    # Region size in number of nodes
    
    def region_size_nodes(self, colour, node):
        return memoizer2(self.region_size_nodes_map, self.compute_region_size_nodes, colour, node)
        
    def compute_region_size_nodes(self, colour, node):
        if node == self.root_map[colour]:
            return self.n
        elif node in self.roots:
            return 1
        else:
            col_prev_contribution = self.subtree_size_path_sum(colour, col_prev(colour), node)
            col_next_contribution = self.subtree_size_path_sum(colour, col_next(colour), node)
            return col_prev_contribution + col_next_contribution - self.subtree_size(colour, node)
    
    def region_size_nodes_red(self, node):
        return self.region_size_nodes(Colour.RED, node)
    
    def region_size_nodes_blue(self, node):
        return self.region_size_nodes(Colour.BLUE, node)
    
    def region_size_nodes_green(self, node):
        return self.region_size_nodes(Colour.GREEN, node)
    
    # Path length in number of edges
    # TODO optimize
    
    def path_length(self, colour, node):
        return memoizer2(self.path_length_map, self.compute_path_length, colour, node)
    
    def compute_path_length(self, colour, node):
        return len(self.path_nodes(colour, node)) - 1
    
    def path_length_red(self, node):
        return self.path_length(Colour.RED, node)
    
    def path_length_blue(self, node):
        return self.path_length(Colour.BLUE, node)
    
    def path_length_green(self, node):
        return self.path_length(Colour.GREEN, node)
    
    # Region size in number of triangles
    
    def region_size_triangles(self, colour, node):
        if node == self.root_map[colour]:
            return 2 * self.n - 5
        elif node in self.roots:
            return 0
        else:
            n_nodes = self.region_size_nodes(colour, node)
            exterior_cycle_length = self.path_length(col_prev(colour), node) + self.path_length(col_next(colour), node) + 1
            return 2 * n_nodes - 2 - exterior_cycle_length
    
    def region_size_triangles_red(self, node):
        return self.region_size_triangles(Colour.RED, node)
    
    def region_size_triangles_blue(self, node):
        return self.region_size_triangles(Colour.BLUE, node)
    
    def region_size_triangles_green(self, node):
        return self.region_size_triangles(Colour.GREEN, node)

def memoizer(map, fn, input):
    if input not in map:
        map[input] = fn(input)
    return map[input]

def memoizer2(map2, fn2, inputx, inputy):
    if inputy not in map2[inputx]:
        map2[inputx][inputy] = fn2(inputx, inputy)
    return map2[inputx][inputy]