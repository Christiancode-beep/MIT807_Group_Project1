import tkinter as tk  # Added this import
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TabuVisualizer:
    def __init__(self, graph, canvas):
        self.graph = graph
        self.canvas = canvas
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.pos = nx.spring_layout(graph)

        # Embed in Tkinter
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.canvas)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update(self, iteration, current_solution, best_solution, tabu_list, current_cost, best_cost):
        self.ax.clear()

        # Draw the complete graph
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, node_size=400, node_color='lightblue')
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, width=1, alpha=0.3)

        # Highlight current solution (red)
        current_edges = list(zip(current_solution, current_solution[1:] + [current_solution[0]]))
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=current_edges,
                               ax=self.ax, width=2, edge_color='red', alpha=0.7)

        # Highlight best solution (green)
        best_edges = list(zip(best_solution, best_solution[1:] + [best_solution[0]]))
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=best_edges,
                               ax=self.ax, width=3, edge_color='green', alpha=0.9)

        # Draw tabu solutions (gray)
        for solution in tabu_list:
            edges = list(zip(solution, solution[1:] + [solution[0]]))
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=edges,
                                   ax=self.ax, width=1, edge_color='gray', alpha=0.2)

        # Draw labels
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax)
        edge_weights = nx.get_edge_attributes(self.graph, 'weight')
        if edge_weights:
            nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_weights, ax=self.ax)

        # Add info text
        info_text = f"Iteration: {iteration}\nCurrent Cost: {current_cost:.2f}\nBest Cost: {best_cost:.2f}"
        self.ax.text(0.02, 0.98, info_text, transform=self.ax.transAxes,
                     verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))

        self.ax.set_title("Tabu Search - Traveling Salesman Problem", fontsize=12)
        self.canvas_widget.draw()
        self.canvas.update()