import heapq
import tkinter as tk  # Added this import
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SearchVisualizer:
    def __init__(self, graph, canvas):
        self.graph = graph
        self.canvas = canvas
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.pos = nx.spring_layout(graph)
        self.current_node = None
        self.visited_nodes = []
        self.current_path = []

        # Embed matplotlib figure in Tkinter
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.canvas)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_display(self):
        self.ax.clear()

        # Draw all nodes and edges
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, node_size=500, node_color='lightblue')
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, width=1, alpha=0.5)

        # Highlight visited nodes
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=self.visited_nodes,
                               ax=self.ax, node_size=500, node_color='yellow')

        # Highlight current node
        if self.current_node:
            nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[self.current_node],
                                   ax=self.ax, node_size=500, node_color='red')

        # Highlight current path
        if self.current_path:
            path_edges = list(zip(self.current_path[:-1], self.current_path[1:]))
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=path_edges,
                                   ax=self.ax, width=2, edge_color='red')

        # Draw labels and weights
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax)
        edge_weights = nx.get_edge_attributes(self.graph, 'weight')
        if edge_weights:
            nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_weights, ax=self.ax)

        self.ax.set_title("Search Progress", fontsize=14)
        self.canvas_widget.draw()
        self.canvas.update()