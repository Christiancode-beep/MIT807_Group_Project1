import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from search_algorithms.uninformed.dfs import DFS
from search_algorithms.uninformed.ucs import UCS
from search_algorithms.tabu_search.tabu import TabuSearch


class GraphCanvas(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.graph = nx.Graph()

        # Create matplotlib figure
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


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MIT807 AI Search Visualizer")
        self.geometry("1200x800")
        self.configure(bg='#f0f0f0')

        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create frames
        self.create_control_panel()
        self.create_visualization_panel()

        self.setup_style()

    def setup_style(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TCombobox', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'))

    def create_control_panel(self):
        """Left panel with controls"""
        control_frame = ttk.Frame(self, width=300, padding=(10, 10, 10, 10))
        control_frame.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)

        # Algorithm selection
        ttk.Label(control_frame, text="Algorithm:").pack(pady=(0, 5))
        self.algorithm_var = tk.StringVar(value="DFS")
        algo_menu = ttk.Combobox(control_frame, textvariable=self.algorithm_var,
                                 values=["DFS", "UCS", "Tabu Search"])
        algo_menu.pack(fill=tk.X, pady=(0, 15))

        # Algorithm parameters
        param_frame = ttk.LabelFrame(control_frame, text="Algorithm Parameters", padding=10)
        param_frame.pack(fill=tk.X, pady=5)

        # Start/Goal nodes (for DFS/UCS)
        ttk.Label(param_frame, text="Start Node:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.start_entry = ttk.Entry(param_frame)
        self.start_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)

        ttk.Label(param_frame, text="Goal Node:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.goal_entry = ttk.Entry(param_frame)
        self.goal_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)

        # Tabu Search parameters
        ttk.Label(param_frame, text="Max Iterations:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.max_iter_entry = ttk.Entry(param_frame)
        self.max_iter_entry.insert(0, "50")
        self.max_iter_entry.grid(row=2, column=1, sticky=tk.EW, pady=2)

        ttk.Label(param_frame, text="Tabu Size:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.tabu_size_entry = ttk.Entry(param_frame)
        self.tabu_size_entry.insert(0, "10")
        self.tabu_size_entry.grid(row=3, column=1, sticky=tk.EW, pady=2)

        # Speed control
        ttk.Label(param_frame, text="Animation Speed:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.speed_scale = ttk.Scale(param_frame, from_=0.1, to=1.0, value=0.5)
        self.speed_scale.grid(row=4, column=1, sticky=tk.EW, pady=2)

        param_frame.columnconfigure(1, weight=1)

        # Graph controls
        graph_frame = ttk.LabelFrame(control_frame, text="Graph Construction", padding=10)
        graph_frame.pack(fill=tk.X, pady=5)

        # Node controls
        ttk.Label(graph_frame, text="Node:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.node_entry = ttk.Entry(graph_frame)
        self.node_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)
        ttk.Button(graph_frame, text="Add Node", command=self.add_node).grid(row=0, column=2, padx=5)

        # Edge controls
        ttk.Label(graph_frame, text="From:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.from_entry = ttk.Entry(graph_frame)
        self.from_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)

        ttk.Label(graph_frame, text="To:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.to_entry = ttk.Entry(graph_frame)
        self.to_entry.grid(row=1, column=3, sticky=tk.EW, pady=2)

        ttk.Label(graph_frame, text="Weight:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.weight_entry = ttk.Entry(graph_frame)
        self.weight_entry.insert(0, "1.0")
        self.weight_entry.grid(row=2, column=1, sticky=tk.EW, pady=2)
        ttk.Button(graph_frame, text="Add Edge", command=self.add_edge).grid(row=2, column=2, columnspan=2)

        # Graph operations
        ttk.Button(graph_frame, text="Clear Graph", command=self.clear_graph).grid(row=3, column=0, columnspan=4,
                                                                                   pady=(10, 0))

        graph_frame.columnconfigure(1, weight=1)
        graph_frame.columnconfigure(3, weight=1)

        # Run button
        ttk.Button(control_frame, text="Run Algorithm",
                   command=self.run_algorithm, style='Accent.TButton').pack(pady=15)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(control_frame, textvariable=self.status_var,
                  relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, pady=(10, 0))

    def create_visualization_panel(self):
        """Right panel with graph visualization"""
        viz_frame = ttk.Frame(self, padding=(5, 5, 5, 5))
        viz_frame.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)

        # Create graph canvas
        self.graph_canvas = GraphCanvas(viz_frame)
        self.graph_canvas.pack(fill=tk.BOTH, expand=True)

    def add_node(self):
        node = self.node_entry.get()
        if node:
            if self.graph_canvas.add_node(node):
                self.status_var.set(f"Added node: {node}")
                self.node_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", f"Node {node} already exists")

    def add_edge(self):
        from_node = self.from_entry.get()
        to_node = self.to_entry.get()
        weight = self.weight_entry.get()

        if not from_node or not to_node:
            messagebox.showerror("Error", "Please specify both 'From' and 'To' nodes")
            return

        try:
            weight = float(weight)
            if self.graph_canvas.add_edge(from_node, to_node, weight):
                self.status_var.set(f"Added edge: {from_node} → {to_node} (weight: {weight})")
                self.from_entry.delete(0, tk.END)
                self.to_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "One or both nodes don't exist")
        except ValueError:
            messagebox.showerror("Error", "Weight must be a number")

    def clear_graph(self):
        self.graph_canvas.clear_graph()
        self.status_var.set("Graph cleared")

    def run_algorithm(self):
        algorithm = self.algorithm_var.get()
        delay = 1.1 - self.speed_scale.get()  # Convert to delay (0.1-1.0s)

        try:
            if algorithm in ["DFS", "UCS"]:
                start = self.start_entry.get()
                goal = self.goal_entry.get()

                if not start or not goal:
                    messagebox.showerror("Error", "Please specify both start and goal nodes")
                    return

                if start not in self.graph_canvas.graph.nodes() or goal not in self.graph_canvas.graph.nodes():
                    messagebox.showerror("Error", "Start or goal node not in graph")
                    return

                self.status_var.set(f"Running {algorithm} from {start} to {goal}...")
                self.update()

                if algorithm == "DFS":
                    dfs = DFS(self.graph_canvas.graph, self.graph_canvas)
                    path = dfs.search(start, goal, delay)
                else:  # UCS
                    ucs = UCS(self.graph_canvas.graph, self.graph_canvas)
                    path = ucs.search(start, goal, delay)

                if path:
                    self.status_var.set(f"{algorithm} found path: {' → '.join(path)}")
                else:
                    self.status_var.set(f"{algorithm} found no path")

            elif algorithm == "Tabu Search":
                try:
                    max_iter = int(self.max_iter_entry.get())
                    tabu_size = int(self.tabu_size_entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Iterations and Tabu Size must be integers")
                    return

                if len(self.graph_canvas.graph.nodes()) < 3:
                    messagebox.showerror("Error", "Tabu Search requires at least 3 nodes")
                    return

                self.status_var.set("Running Tabu Search...")
                self.update()

                tabu = TabuSearch(
                    graph=self.graph_canvas.graph,
                    canvas=self.graph_canvas,
                    max_iter=max_iter,
                    tabu_size=tabu_size
                )
                best_solution = tabu.search(delay)

                if best_solution:
                    cost = tabu.calculate_cost(best_solution)
                    self.status_var.set(f"Best solution found (cost: {cost:.2f}): {' → '.join(best_solution)}")
                else:
                    self.status_var.set("Tabu Search completed")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error during execution")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()