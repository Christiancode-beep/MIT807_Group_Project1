import tkinter as tk
from tkinter import ttk


class ControlPanel:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.create_widgets()

    def create_widgets(self):
        # Algorithm selection
        ttk.Label(self.parent, text="Algorithm:").pack(pady=(0, 5))
        self.algorithm_var = tk.StringVar()
        self.algorithm_menu = ttk.Combobox(self.parent, textvariable=self.algorithm_var,
                                           values=["DFS", "UCS", "Tabu Search"])
        self.algorithm_menu.pack(fill=tk.X, pady=(0, 10))
        self.algorithm_menu.current(0)

        # Parameters frame
        self.params_frame = ttk.LabelFrame(self.parent, text="Parameters")
        self.params_frame.pack(fill=tk.X, pady=5)

        # Start node
        ttk.Label(self.params_frame, text="Start Node:").grid(row=0, column=0, sticky=tk.W)
        self.start_entry = ttk.Entry(self.params_frame)
        self.start_entry.grid(row=0, column=1, sticky=tk.EW)

        # Goal node (for DFS/UCS)
        ttk.Label(self.params_frame, text="Goal Node:").grid(row=1, column=0, sticky=tk.W)
        self.goal_entry = ttk.Entry(self.params_frame)
        self.goal_entry.grid(row=1, column=1, sticky=tk.EW)

        # Tabu Search parameters
        ttk.Label(self.params_frame, text="Max Iterations:").grid(row=2, column=0, sticky=tk.W)
        self.max_iter_entry = ttk.Entry(self.params_frame)
        self.max_iter_entry.grid(row=2, column=1, sticky=tk.EW)
        self.max_iter_entry.insert(0, "100")

        ttk.Label(self.params_frame, text="Tabu List Size:").grid(row=3, column=0, sticky=tk.W)
        self.tabu_size_entry = ttk.Entry(self.params_frame)
        self.tabu_size_entry.grid(row=3, column=1, sticky=tk.EW)
        self.tabu_size_entry.insert(0, "10")

        # Run button
        self.run_button = ttk.Button(self.parent, text="Run Algorithm",
                                     command=self.on_run_clicked)
        self.run_button.pack(fill=tk.X, pady=10)

        # Graph controls
        self.graph_controls = ttk.LabelFrame(self.parent, text="Graph Controls")
        self.graph_controls.pack(fill=tk.X, pady=5)

        # Node controls
        ttk.Label(self.graph_controls, text="Node:").grid(row=0, column=0)
        self.node_entry = ttk.Entry(self.graph_controls)
        self.node_entry.grid(row=0, column=1)
        ttk.Button(self.graph_controls, text="Add Node",
                   command=self.on_add_node).grid(row=0, column=2)

        # Edge controls
        ttk.Label(self.graph_controls, text="From:").grid(row=1, column=0)
        self.from_entry = ttk.Entry(self.graph_controls)
        self.from_entry.grid(row=1, column=1)

        ttk.Label(self.graph_controls, text="To:").grid(row=1, column=2)
        self.to_entry = ttk.Entry(self.graph_controls)
        self.to_entry.grid(row=1, column=3)

        ttk.Label(self.graph_controls, text="Weight:").grid(row=1, column=4)
        self.weight_entry = ttk.Entry(self.graph_controls)
        self.weight_entry.grid(row=1, column=5)
        ttk.Button(self.graph_controls, text="Add Edge",
                   command=self.on_add_edge).grid(row=1, column=6)

    def on_run_clicked(self):
        algorithm = self.algorithm_var.get()
        params = {
            'start': self.start_entry.get(),
            'goal': self.goal_entry.get(),
            'max_iter': int(self.max_iter_entry.get()),
            'tabu_size': int(self.tabu_size_entry.get())
        }
        self.main_window.run_algorithm(algorithm, params)

    def on_add_node(self):
        node = self.node_entry.get()
        if node:
            self.main_window.graph_panel.add_node(node)

    def on_add_edge(self):
        from_node = self.from_entry.get()
        to_node = self.to_entry.get()
        weight = self.weight_entry.get() or "1"

        if from_node and to_node:
            try:
                weight = float(weight)
                self.main_window.graph_panel.add_edge(from_node, to_node, weight)
            except ValueError:
                tk.messagebox.showerror("Error", "Weight must be a number")