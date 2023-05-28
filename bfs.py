from collections import deque

def bfs(graph, start):
    visited = [False] * len(graph.nodes)
    queue = deque([start])
    visited[start] = True
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph.neighbors(node):
            if not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True
    return result
