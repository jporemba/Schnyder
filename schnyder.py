import networkx as nx

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
        
        self.subtree_size_red_map = dict()
        self.subtree_size_blue_map = dict()
        self.subtree_size_green_map = dict()
        self.region_size_nodes_red_map = dict()
        self.region_size_nodes_blue_map = dict()
        self.region_size_nodes_green_map = dict()
        self.path_length_red_map = dict()
        self.path_length_blue_map = dict()
        self.path_length_green_map = dict()
    
    def red_parent(self, node):
        if node in self.roots:
            raise Exception(f"Cannot take red parent of root {node}")
        parents = list(self.red_tree.successors(node))
        assert len(parents) == 1, f'node {node} has red parents {parents}'
        return parents[0]
    
    def green_parent(self, node):
        if node in self.roots:
            raise Exception(f"Cannot take green parent of root {node}")
        parents = list(self.green_tree.successors(node))
        assert len(parents) == 1, f'node {node} has green parents {parents}'
        return parents[0]
    
    def blue_parent(self, node):
        if node in self.roots:
            raise Exception(f"Cannot take blue parent of root {node}")
        parents = list(self.blue_tree.successors(node))
        assert len(parents) == 1, f'node {node} has blue parents {parents}'
        return parents[0]
            
    def subtree_size_red(self, node):
        if node not in self.subtree_size_red_map:
            self.subtree_size_red_map[node] = self.compute_subtree_size_red(node)
        return self.subtree_size_red_map[node]
            
    def compute_subtree_size_red(self, node): 
        if node == self.red_root:
            return self.n
        elif node in self.roots:
            return 1
        else:
            # Internal node
            children = list(self.red_tree.predecessors(node))
            if len(children) == 0:
                return 1
            else:
                return sum([self.subtree_size_red(child) for child in children]) + 1
    
    def subtree_size_blue(self, node):
        if node not in self.subtree_size_blue_map:
            self.subtree_size_blue_map[node] = self.compute_subtree_size_blue(node)
        return self.subtree_size_blue_map[node]
    
    def compute_subtree_size_blue(self, node): 
        if node == self.blue_root:
            return self.n
        elif node in self.roots:
            return 1
        else:
            # Internal node
            children = list(self.blue_tree.predecessors(node))
            if children == 0:
                return 1
            else:
                return sum([self.subtree_size_blue(child) for child in children]) + 1
    
    def subtree_size_green(self, node):
        if node not in self.subtree_size_green_map:
            self.subtree_size_green_map[node] = self.compute_subtree_size_green(node)
        return self.subtree_size_green_map[node]
    
    def compute_subtree_size_green(self, node): 
        if node == self.green_root:
            return self.n
        elif node in self.roots:
            return 1
        else:
            # Internal node
            children = list(self.green_tree.predecessors(node))
            if children == 0:
                return 1
            else:
                return sum([self.subtree_size_green(child) for child in children]) + 1
    
    def path_nodes_red(self, node):
        if node == self.blue_root or node == self.green_root:
            raise Exception("Cannot find path for other coloured roots")
        current = node
        path = [current]
        while current not in self.roots:
            current = self.red_parent(current)
            path.append(current)
        return path
    
    def path_nodes_blue(self, node):
        if node == self.red_root or node == self.green_root:
            raise Exception("Cannot find path for other coloured roots")
        current = node
        path = [current]
        while current not in self.roots:
            current = self.blue_parent(current)
            path.append(current)
        return path
    
    def path_nodes_green(self, node):
        if node == self.blue_root or node == self.red_root:
            raise Exception("Cannot find path for other coloured roots")
        current = node
        path = [current]
        while current not in self.roots:
            current = self.green_parent(current)
            path.append(current)
        return path
    
    def region_size_nodes_red(self, node):
        if node not in self.region_size_nodes_red_map:
            self.region_size_nodes_red_map[node] = self.compute_region_size_nodes_red(node)
        return self.region_size_nodes_red_map[node]
    
    def compute_region_size_nodes_red(self, node):
        if node == self.red_root:
            return self.n
        elif node in self.roots:
            return 1
        else:
            blue_contribution = sum(self.subtree_size_red(u) for u in self.path_nodes_blue(node))
            green_contribution = sum(self.subtree_size_red(u) for u in self.path_nodes_green(node))
            return blue_contribution + green_contribution - self.subtree_size_red(node)
    
    def region_size_nodes_blue(self, node):
        if node not in self.region_size_nodes_blue_map:
            self.region_size_nodes_blue_map[node] = self.compute_region_size_nodes_blue(node)
        return self.region_size_nodes_blue_map[node]
    
    def compute_region_size_nodes_blue(self, node):
        if node == self.blue_root:
            return self.n
        elif node in self.roots:
            return 1
        else:
            red_contribution = sum(self.subtree_size_blue(u) for u in self.path_nodes_red(node))
            green_contribution = sum(self.subtree_size_blue(u) for u in self.path_nodes_green(node))
            return red_contribution + green_contribution - self.subtree_size_blue(node)
    
    def region_size_nodes_green(self, node):
        if node not in self.region_size_nodes_green_map:
            self.region_size_nodes_green_map[node] = self.compute_region_size_nodes_green(node)
        return self.region_size_nodes_green_map[node]
    
    def compute_region_size_nodes_green(self, node):
        if node == self.green_root:
            return self.n
        elif node in self.roots:
            return 1
        else:
            red_contribution = sum(self.subtree_size_green(u) for u in self.path_nodes_red(node))
            blue_contribution = sum(self.subtree_size_green(u) for u in self.path_nodes_blue(node))
            return red_contribution + blue_contribution - self.subtree_size_green(node)
    
    # in number of edges
    def path_length_red(self, node):
        return len(self.path_nodes_red(node)) - 1
    
    def path_length_blue(self, node):
        return len(self.path_nodes_blue(node)) - 1
    
    def path_length_green(self, node):
        return len(self.path_nodes_green(node)) - 1
    
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