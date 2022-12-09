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
            Colour.RED: self.red_tree,
            Colour.BLUE: self.blue_tree,
            Colour.GREEN: self.green_tree
        }
        
        self.subtree_size_map = {
            Colour.RED: dict(),
            Colour.BLUE: dict(),
            Colour.GREEN: dict()
        }
        
        self.region_size_nodes_red_map = dict()
        self.region_size_nodes_blue_map = dict()
        self.region_size_nodes_green_map = dict()
        self.path_length_red_map = dict()
        self.path_length_blue_map = dict()
        self.path_length_green_map = dict()
        
        self.subtree_size_path_sum_red_blue_map = dict()
        self.subtree_size_path_sum_red_green_map = dict()
        self.subtree_size_path_sum_blue_red_map = dict()
        self.subtree_size_path_sum_blue_green_map = dict()
        self.subtree_size_path_sum_green_red_map = dict()
        self.subtree_size_path_sum_green_blue_map = dict()
        
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
    
    def subtree_size_path_sum_red_blue(self, node):
        return memoizer(self.subtree_size_path_sum_red_blue_map, self.compute_subtree_size_path_sum_red_blue, node)
    
    def compute_subtree_size_path_sum_red_blue(self, node):
        if node == self.blue_root:
            return self.subtree_size_red(node)
        else:
            return self.subtree_size_path_sum_red_blue(self.blue_parent(node)) + self.subtree_size_red(node)
        
    def subtree_size_path_sum_red_green(self, node):
        return memoizer(self.subtree_size_path_sum_red_green_map, self.compute_subtree_size_path_sum_red_green, node)

    def compute_subtree_size_path_sum_red_green(self, node):
        if node == self.green_root:
            return self.subtree_size_red(node)
        else:
            return self.subtree_size_path_sum_red_green(self.green_parent(node)) + self.subtree_size_red(node)
    
    def subtree_size_path_sum_blue_red(self, node):
        return memoizer(self.subtree_size_path_sum_blue_red_map, self.compute_subtree_size_path_sum_blue_red, node)
    
    def compute_subtree_size_path_sum_blue_red(self, node):
        if node == self.red_root:
            return self.subtree_size_blue(node)
        else:
            return self.subtree_size_path_sum_blue_red(self.red_parent(node)) + self.subtree_size_blue(node)

    def subtree_size_path_sum_blue_green(self, node):
        return memoizer(self.subtree_size_path_sum_blue_green_map, self.compute_subtree_size_path_sum_blue_green, node)

    def compute_subtree_size_path_sum_blue_green(self, node):
        if node == self.green_root:
            return self.subtree_size_blue(node)
        else:
            return self.subtree_size_path_sum_blue_green(self.green_parent(node)) + self.subtree_size_blue(node)
    
    def subtree_size_path_sum_green_red(self, node):
        return memoizer(self.subtree_size_path_sum_green_red_map, self.compute_subtree_size_path_sum_green_red, node)
    
    def compute_subtree_size_path_sum_green_red(self, node):
        if node == self.red_root:
            return self.subtree_size_green(node)
        else:
            return self.subtree_size_path_sum_green_red(self.red_parent(node)) + self.subtree_size_green(node)

    def subtree_size_path_sum_green_blue(self, node):
        return memoizer(self.subtree_size_path_sum_green_blue_map, self.compute_subtree_size_path_sum_green_blue, node)
    
    def compute_subtree_size_path_sum_green_blue(self, node):
        if node == self.blue_root:
            return self.subtree_size_green(node)
        else:
            return self.subtree_size_path_sum_green_blue(self.blue_parent(node)) + self.subtree_size_green(node)
    
    # Region size in number of nodes
    
    def region_size_nodes_red(self, node):
        return memoizer(self.region_size_nodes_red_map, self.compute_region_size_nodes_red, node)
    
    def compute_region_size_nodes_red(self, node):
        if node == self.red_root:
            return self.n
        elif node in self.roots:
            return 1
        else:
            blue_contribution = self.subtree_size_path_sum_red_blue(node)
            green_contribution = self.subtree_size_path_sum_red_green(node)
            return blue_contribution + green_contribution - self.subtree_size_red(node)
    
    def region_size_nodes_blue(self, node):
        return memoizer(self.region_size_nodes_blue_map, self.compute_region_size_nodes_blue, node)
    
    def compute_region_size_nodes_blue(self, node):
        if node == self.blue_root:
            return self.n
        elif node in self.roots:
            return 1
        else:
            red_contribution = self.subtree_size_path_sum_blue_red(node)
            green_contribution = self.subtree_size_path_sum_blue_green(node)
            return red_contribution + green_contribution - self.subtree_size_blue(node)
    
    def region_size_nodes_green(self, node):
        return memoizer(self.region_size_nodes_green_map, self.compute_region_size_nodes_green, node)
    
    def compute_region_size_nodes_green(self, node):
        if node == self.green_root:
            return self.n
        elif node in self.roots:
            return 1
        else:
            red_contribution = self.subtree_size_path_sum_green_red(node)
            blue_contribution = self.subtree_size_path_sum_green_blue(node)
            return red_contribution + blue_contribution - self.subtree_size_green(node)
    
    # Path length in number of edges
    
    def path_length_red(self, node):
        return memoizer(self.path_length_red_map, self.compute_path_length_red, node)
    
    def compute_path_length_red(self, node):
        return len(self.path_nodes_red(node)) - 1
    
    def path_length_blue(self, node):
        return memoizer(self.path_length_blue_map, self.compute_path_length_blue, node)
    
    def compute_path_length_blue(self, node):
        return len(self.path_nodes_blue(node)) - 1
    
    def path_length_green(self, node):
        return memoizer(self.path_length_green_map, self.compute_path_length_green, node)
    
    def compute_path_length_green(self, node):
        return len(self.path_nodes_green(node)) - 1
    
    # Region size in number of triangles
    
    def region_size_triangles_red(self, node):
        if node == self.red_root:
            return 2 * self.n - 5
        elif node in self.roots:
            return 0
        else:
            n_nodes = self.region_size_nodes_red(node)
            exterior_cycle_length = self.path_length_blue(node) + self.path_length_green(node) + 1
            return 2 * n_nodes - 2 - exterior_cycle_length
    
    def region_size_triangles_blue(self, node):
        if node == self.blue_root:
            return 2 * self.n - 5
        elif node in self.roots:
            return 0
        else:
            n_nodes = self.region_size_nodes_blue(node)
            exterior_cycle_length = self.path_length_red(node) + self.path_length_green(node) + 1
            return 2 * n_nodes - 2 - exterior_cycle_length
    
    def region_size_triangles_green(self, node):
        if node == self.green_root:
            return 2 * self.n - 5
        elif node in self.roots:
            return 0
        else:
            n_nodes = self.region_size_nodes_green(node)
            exterior_cycle_length = self.path_length_red(node) + self.path_length_blue(node) + 1
            return 2 * n_nodes - 2 - exterior_cycle_length

def memoizer(map, fn, input):
    if input not in map:
        map[input] = fn(input)
    return map[input]

def memoizer2(map2, fn2, inputx, inputy):
    if inputy not in map2[inputx]:
        map2[inputx][inputy] = fn2(inputx, inputy)
    return map2[inputx][inputy]