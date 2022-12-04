import networkx as nx

G = nx.Graph()

nodes = [
    'v1',
    'v2',
    'v3',
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k'
]

red_root = 'v1'

red_edges = [
    ('a', 'v1'),
    ('b', 'v1'),
    ('c', 'v1'),
    ('h', 'a'),
    ('i', 'a'),
    ('d', 'a'),
    ('e', 'b'),
    ('f', 'b'),
    ('g', 'c'),
    ('j', 'i'),
    ('k', 'd')
]

green_root = 'v3'
green_edges = [
    ('j', 'v3'),
    ('k', 'v3'),
    ('f', 'v3'),
    ('g', 'v3'),
    ('c', 'v3'),
    ('e', 'f'),
    ('b', 'c'),
    ('a', 'b'),
    ('d', 'b'),
    ('i', 'd'),
    ('h', 'i')
]

blue_root = 'v2'
blue_edges = [
    ('a', 'v2'),
    ('h', 'v2'),
    ('i', 'v2'),
    ('j', 'v2'),
    ('d', 'j'),
    ('k', 'j'),
    ('b', 'k'),
    ('e', 'k'),
    ('f', 'k'),
    ('c', 'f'),
    ('g', 'f')
]


