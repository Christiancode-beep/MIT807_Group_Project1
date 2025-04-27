import random
import time
import numpy as np
from .visualizer import TabuVisualizer


class TabuSearch:
    def __init__(self, graph, canvas, max_iter=50, tabu_size=10):
        self.visualizer = TabuVisualizer(graph, canvas)
        self.graph = graph
        self.max_iter = max_iter
        self.tabu_size = tabu_size

    def initial_solution(self):
        """Generate random path visiting all nodes"""
        nodes = list(self.graph.nodes())
        random.shuffle(nodes)
        return nodes

    def calculate_cost(self, path):
        """Calculate total path cost"""
        total = 0
        for i in range(len(path) - 1):
            edge_data = self.graph.get_edge_data(path[i], path[i + 1])
            total += edge_data['weight'] if edge_data else 1
        # Return to start for TSP
        edge_data = self.graph.get_edge_data(path[-1], path[0])
        total += edge_data['weight'] if edge_data else 1
        return total

    def get_neighbors(self, solution):
        """Generate neighbors by swapping two cities"""
        neighbors = []
        for i in range(len(solution)):
            for j in range(i + 1, len(solution)):
                neighbor = solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
        return neighbors

    def search(self, delay=0.5):
        current = self.initial_solution()
        best = current.copy()
        tabu_list = []

        for iteration in range(self.max_iter):
            neighbors = self.get_neighbors(current)
            best_neighbor = None
            best_neighbor_cost = float('inf')

            for neighbor in neighbors:
                if neighbor not in tabu_list:
                    cost = self.calculate_cost(neighbor)
                    if cost < best_neighbor_cost:
                        best_neighbor = neighbor
                        best_neighbor_cost = cost

            if not best_neighbor:
                break

            current = best_neighbor
            tabu_list.append(current)

            if len(tabu_list) > self.tabu_size:
                tabu_list.pop(0)

            if self.calculate_cost(current) < self.calculate_cost(best):
                best = current.copy()

            # Update visualization
            self.visualizer.update(
                iteration=iteration,
                current_solution=current,
                best_solution=best,
                tabu_list=tabu_list,
                current_cost=self.calculate_cost(current),
                best_cost=self.calculate_cost(best)
            )

            time.sleep(delay)

        return best