import tkinter as tk
from tkinter import ttk
import networkx as nx
from search_algorithms.uninformed.dfs import DFS
from search_algorithms.uninformed.ucs import UCS
from search_algorithms.tabu_search.tabu import TabuSearch

class GraphPanel:
    def __init__(self, parent):
        self.parent = parent
        self.graph = nx.Graph()
        self.create_widgets()

    def create_widgets(self):
        # Text area for graph info
        self.info_text = tk.Text(self.parent, state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True)

        # Update graph info
        self.update_info()

    def add_node(self, node):
        self.graph.add_node(node)
        self.update_info()

    def add_edge(self, from_node, to_node, weight):
        self.graph.add_edge(from_node, to_node, weight=weight)
        self.update_info()

    def update_info(self):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Nodes: " + ", ".join(self.graph.nodes()) + "\n\n")
        self.info_text.insert(tk.END, "Edges:\n")
        for edge in self.graph.edges(data=True):
            self.info_text.insert(tk.END, f"{edge[0]} -> {edge[1]} (weight: {edge[2].get('weight', 1)})\n")
        self.info_text.config(state=tk.DISABLED)

    def run_algorithm(self, algorithm, params):
        if algorithm == "DFS":
            dfs = DFS(self.graph)
            dfs.search(params['start'], params['goal'])
        elif algorithm == "UCS":
            ucs = UCS(self.graph)
            ucs.search(params['start'], params['goal'])
        elif algorithm == "Tabu Search":
            tabu = TabuSearch(self.graph, params['max_iter'], params['tabu_size'])
            tabu.search(params['start'])