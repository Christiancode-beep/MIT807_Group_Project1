import time
from .visualizer import SearchVisualizer


class DFS:
    def __init__(self, graph, canvas):
        self.visualizer = SearchVisualizer(graph, canvas)
        self.graph = graph

    def search(self, start, goal, delay=0.5):
        stack = [(start, [start])]
        visited = set()

        while stack:
            node, path = stack.pop()

            # Update visualization
            self.visualizer.current_node = node
            self.visualizer.visited_nodes = list(visited)
            self.visualizer.current_path = path
            self.visualizer.update_display()

            if node == goal:
                return path

            if node not in visited:
                visited.add(node)
                # Reverse neighbors for left-to-right exploration in visualization
                neighbors = sorted(self.graph.neighbors(node), reverse=True)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))

            time.sleep(delay)  # Pause to see the progress

        return None  # No path found