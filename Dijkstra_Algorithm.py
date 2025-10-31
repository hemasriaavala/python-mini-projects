from collections import defaultdict
import heapq

class Graph:
    def __init__(self):
        # Initialize a default dictionary to store the graph
        # Each vertex maps to a list of tuples (neighbor, weight)
        self.graph = defaultdict(list)
    
    def add_edge(self, src, dest, weight):
        # Add edges to the graph (undirected)
        self.graph[src].append((dest, weight))
        self.graph[dest].append((src, weight))

def dijkstra(graph, start_vertex):
    """
    Implements Dijkstra's shortest path algorithm
    Args:
        graph: Graph object containing the adjacency list
        start_vertex: Starting vertex for path finding
    Returns:
        distances: Dictionary containing shortest distances to all vertices
        paths: Dictionary containing the path to reach each vertex
    """
    # Initialize distances dictionary with infinity for all vertices
    distances = {vertex: float('infinity') for vertex in graph.graph}
    distances[start_vertex] = 0
    
    # Dictionary to store the path to reach each vertex
    paths = {vertex: [] for vertex in graph.graph}
    paths[start_vertex] = [start_vertex]
    
    # Priority queue to store vertices and their distances
    # Format: (distance, vertex)
    pq = [(0, start_vertex)]
    
    while pq:
        # Get vertex with minimum distance
        current_distance, current_vertex = heapq.heappop(pq)
        
        # If we found a longer path, skip
        if current_distance > distances[current_vertex]:
            continue
            
        # Check all neighbors of current vertex
        for neighbor, weight in graph.graph[current_vertex]:
            distance = current_distance + weight
            
            # If we found a shorter path to neighbor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # Update path to neighbor
                paths[neighbor] = paths[current_vertex] + [neighbor]
                heapq.heappush(pq, (distance, neighbor))
    
    return distances, paths

# Example usage
if __name__ == "__main__":
    # Create a new graph
    g = Graph()
    
    # Add edges (representing connections between vertices with weights)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 2)
    g.add_edge(1, 2, 1)
    g.add_edge(1, 3, 5)
    g.add_edge(2, 3, 8)
    g.add_edge(2, 4, 10)
    g.add_edge(3, 4, 2)
    
    # Find shortest paths from vertex 0
    start_vertex = 0
    distances, paths = dijkstra(g, start_vertex)
    
    # Print results
    for vertex in distances:
        print(f"Shortest distance from vertex {start_vertex} to vertex {vertex} is {distances[vertex]}")
        print(f"Path: {' -> '.join(map(str, paths[vertex]))}")
        print()