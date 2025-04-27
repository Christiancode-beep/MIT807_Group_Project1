import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class GraphCanvas(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.graph = nx.Graph()

        # Create matplotlib figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)
        self.setup_canvas()
        self.setup_toolbar()
        self.draw_empty_graph()

    def setup_canvas(self):
        """Initialize the matplotlib canvas"""
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def setup_toolbar(self):
        """Add matplotlib navigation toolbar"""
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def draw_empty_graph(self):
        """Draw placeholder when no nodes exist"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Add nodes to begin",
                     ha='center', va='center', fontsize=12)
        self.ax.set_axis_off()
        self.canvas.draw()

    def draw_graph(self):
        """Redraw the entire graph with current state"""
        self.ax.clear()

        if len(self.graph.nodes()) == 0:
            self.draw_empty_graph()
            return

        # Calculate layout
        self.pos = nx.spring_layout(self.graph)

        # Draw elements
        nx.draw_networkx_nodes(
            self.graph, self.pos, ax=self.ax,
            node_size=500,
            node_color='lightblue',
            alpha=0.9
        )

        nx.draw_networkx_edges(
            self.graph, self.pos, ax=self.ax,
            width=1.5,
            edge_color='gray',
            alpha=0.7
        )

        # Draw labels
        nx.draw_networkx_labels(
            self.graph, self.pos, ax=self.ax,
            font_size=10,
            font_color='black'
        )

        # Draw edge weights if they exist
        edge_weights = nx.get_edge_attributes(self.graph, 'weight')
        if edge_weights:
            nx.draw_networkx_edge_labels(
                self.graph, self.pos, ax=self.ax,
                edge_labels=edge_weights,
                font_size=8,
                label_pos=0.5
            )

        # Formatting
        self.ax.set_title("Graph Visualization", pad=20)
        self.ax.set_axis_off()
        self.ax.margins(0.1)
        self.fig.tight_layout()
        self.canvas.draw()

    def add_node(self, node):
        """Add a node to the graph and redraw"""
        if node and node not in self.graph.nodes():
            self.graph.add_node(node)
            self.draw_graph()
            return True
        return False

    def add_edge(self, from_node, to_node, weight=1.0):
        """Add a weighted edge to the graph and redraw"""
        if from_node in self.graph.nodes() and to_node in self.graph.nodes():
            self.graph.add_edge(from_node, to_node, weight=float(weight))
            self.draw_graph()
            return True
        return False

    def clear_graph(self):
        """Reset the graph to empty state"""
        self.graph.clear()
        self.draw_empty_graph()

    def get_node_list(self):
        """Return list of nodes in graph"""
        return list(self.graph.nodes())

    def get_edge_list(self):
        """Return list of edges with weights"""
        return list(self.graph.edges(data='weight'))