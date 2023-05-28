import heapq
import sys

sys.setrecursionlimit(10**6)  # Définit la limite de récursion sur une valeur élevée


def dijkstra(graph, start):
    num_nodes = len(graph)
    distances = [sys.maxsize] * num_nodes
    distances[start] = 0
    predecessors = [None] * num_nodes

    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor in range(num_nodes):
            if graph[current_node][neighbor] != 0:
                distance = current_distance + graph[current_node][neighbor]

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

    return distances, predecessors