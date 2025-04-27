import heapq
import time
from .visualizer import SearchVisualizer


class UCS:
    def __init__(self, graph, canvas):
        self.visualizer = SearchVisualizer(graph, canvas)
        self.graph = graph

    def search(self, start, goal, delay=0.5):
        heap = [(0, start, [start])]
        heapq.heapify(heap)
        visited = set()

        while heap:
            cost, node, path = heapq.heappop(heap)

            # Update visualization
            self.visualizer.current_node = node
            self.visualizer.visited_nodes = list(visited)
            self.visualizer.current_path = path
            self.visualizer.update_display()

            if node == goal:
                return path

            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in visited:
                        edge_cost = self.graph.get_edge_data(node, neighbor).get('weight', 1)
                        new_cost = cost + edge_cost
                        heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))

            time.sleep(delay)  # Pause to see the progress

        return None  # No path found