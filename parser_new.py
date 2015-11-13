#!/usr/bin/env python
# encoding: utf-8

import sys
from graphviz import Digraph
from collections import defaultdict

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph

word_count = {}
#word_count = defaultdict(int)

total_count = 0

mapping = {'papieros.csv': 'papieros', 'fajka.csv': 'fajka', 'tyton.csv': 'tytoń', 'dym.csv': 'dym'}
for filename in ['papieros.csv', 'fajka.csv', 'tyton.csv', 'dym.csv']:
    word_count[mapping[filename]] = defaultdict(int)
    with open(filename, 'r') as f:
        for line in f:
            freq, word = line.strip().split(',')
            int_freq = int(freq)
            word_count[mapping[filename]][word] += int_freq
            total_count += int_freq

styles = {
    'graph': {
        'label': 'A Fancy Graph',
        'fontsize': '20',
        'fontcolor': 'white',
        'bgcolor': '#888888',
        'rankdir': 'BT',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'hexagon',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
    },
    'edges': {
        'style': 'dashed',
        'color': 'white',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '12',
        'fontcolor': 'white',
    }
}

# for root_word in ['papieros', 'fajka', 'tyton', 'dym']:
dot = Digraph(comment='Words', engine='neato')

for root_word in ['papieros', 'fajka', 'tytoń', 'dym']:

    dot.node(root_word.decode('utf-8'))
    for word in word_count[root_word]:
        dot.node(word.decode('utf-8'))
        wght = float(word_count[root_word][word]) / total_count
        leng = 6 - 4 * wght # This is good one :P
        dot.edge(root_word.decode('utf-8'), word.decode('utf-8'), label=str(wght)[:5], weight=str(wght), len=str(leng))

    dot = apply_styles(dot, styles)
    print dot.source

dot.render('all.gv', view=True)
