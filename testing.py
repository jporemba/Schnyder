import unittest
import schnyder
import localroute
import example1 as ex1
import example2 as ex2
import evaluation

class TestSchnyderData(unittest.TestCase):
    
    def setUp(self):
        self.woods = schnyder.Woods(ex1.G, ex1.red_root, ex1.red_edges, ex1.green_root, ex1.green_edges, ex1.blue_root, ex1.blue_edges)

    def test_parent(self):
        assert self.woods.red_parent(8) == 9
        assert self.woods.blue_parent(7) == 6
        assert self.woods.green_parent(7) == 5

    def test_path(self):
        assert self.woods.path_nodes_red(3) == [3, 5, 9]
        assert self.woods.path_nodes_blue(5) == [5, 4, 1]
        assert self.woods.path_nodes_green(8) == [8, 5, 2]

    def test_path_length(self):
        assert self.woods.path_length_red(4) == 3
        assert self.woods.path_length_blue(5) == 2
        assert self.woods.path_length_green(3) == 1
    
    def test_subtree_size(self):
        assert self.woods.subtree_size_red(8) == 4
        assert self.woods.subtree_size_blue(6) == 2
        assert self.woods.subtree_size_green(3) == 3
    
    def test_region_size_nodes(self):
        assert self.woods.region_size_nodes_red(7) == 7
        assert self.woods.region_size_nodes_blue(7) == 5
        assert self.woods.region_size_nodes_green(7) == 5
    
    def test_region_size_triangles(self):
        for node in ex1.G.nodes:
            assert self.woods.region_size_triangles_red(node) == ex1.red_coords[node]
            assert self.woods.region_size_triangles_blue(node) == ex1.blue_coords[node]
            assert self.woods.region_size_triangles_green(node) == ex1.green_coords[node]

def is_valid_walk(G, s, t, path):
    if len(path) == 0:
        return s == t
    else:
        if s not in path[0]:
            return False
        if t not in path[-1]:
            return False
        current = s
        for edge in path:
            if edge not in G.edges:
                return False
            if current not in edge:
                return False
            next = set(edge).difference({current}).pop()
            current = next            
    return True

class TestRouting(unittest.TestCase):
    
    def setUp(self):
        self.W1 = schnyder.Woods(ex1.G, ex1.red_root, ex1.red_edges, ex1.green_root, ex1.green_edges, ex1.blue_root, ex1.blue_edges)
        self.W2 = schnyder.Woods(ex2.G, ex2.red_root, ex2.red_edges, ex2.green_root, ex2.green_edges, ex2.blue_root, ex2.blue_edges)
        
    def test_no_explode(self):
        for s in ex1.G.nodes:
            for t in ex1.G.nodes:
                localroute.schnyder_local_route(ex1.G, self.W1, s, t)
        for s in ex2.G.nodes:
            for t in ex2.G.nodes:
                localroute.schnyder_local_route(ex2.G, self.W2, s, t)
    
    def test_meta_valid_paths(self):
        valid_path = [(2, 3), (3, 4), (4, 7), (7, 8), (8, 1), (1, 9)]
        invalid_path_1 = [(2, 3), (3, 9)]
        invalid_path_2 = [(2, 3), (1, 9)]
        assert is_valid_walk(ex1.G, 2, 9, valid_path)
        assert not is_valid_walk(ex1.G, 2, 9, invalid_path_1)
        assert not is_valid_walk(ex1.G, 2, 9, invalid_path_2)
    
    def test_valid_paths(self):
        for s in ex1.G.nodes:
            for t in ex1.G.nodes:
                routing_path = localroute.schnyder_local_route(ex1.G, self.W1, s, t)
                assert is_valid_walk(ex1.G, s, t, routing_path)
        for s in ex2.G.nodes:
            for t in ex2.G.nodes:
                routing_path = localroute.schnyder_local_route(ex2.G, self.W2, s, t)
                assert is_valid_walk(ex2.G, s, t, routing_path)

class TestRoutingFile(unittest.TestCase):
    
    def setUp(self):
        self.subtests = []
        for i in [1, 2, 3, 4]:
            G, W = evaluation.parse_edgelist_to_woods(f'unittest{i}.edgelist')
            self.subtests.append((G, W))
        
    def test_valid_paths(self):
        for subtest in self.subtests:
            G, W = subtest
            for s in G.nodes:
                for t in G.nodes:
                    # print(f's: {s}, t: {t}')
                    routing_path = localroute.schnyder_local_route(G, W, s, t)
                    assert is_valid_walk(G, s, t, routing_path)

class TestEval(unittest.TestCase):
    
    def setUp(self):
        self.subtests = []
        for i in [1, 2, 3, 4]:
            G, W = evaluation.parse_edgelist_to_woods(f'unittest{i}.edgelist')
            self.subtests.append((G, W))
            
    def test_evaluate_routing_protocol_faster(self):
        for subtest in self.subtests:
            G, W = subtest
            distortion1 = evaluation.evaluate_routing_protocol(G, W)
            distortion2 = evaluation.evaluate_routing_protocol_faster(G, W)
            assert len(distortion1) == len(distortion2)
            assert distortion1 == distortion2, f'\nd1: {distortion1}\nd2: {distortion2}'

if __name__ == '__main__':
    unittest.main()