"""Core algorithms used by the Mini-Courier Planner."""

def sort_parcels(parcels):
    """Sort by urgency first, then earliest deadline, then highest value."""
    return sorted(parcels, key=lambda p: (-p["priority"], p["deadline"], -p["value"]))


def knapsack_select(parcels, capacity):
    """
    0/1 knapsack using dynamic programming.
    Parcel weight is its space/weight requirement; value is delivery benefit.
    Returns (selected parcels, total value, total weight, DP table).
    """
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight = int(parcels[i - 1]["weight"])
        value = int(parcels[i - 1]["value"])
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]
            if weight <= cap:
                dp[i][cap] = max(dp[i][cap],
                                 value + dp[i - 1][cap - weight])

    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            selected.append(parcels[i - 1])
            cap -= int(parcels[i - 1]["weight"])
    selected.reverse()
    total_weight = sum(int(p["weight"]) for p in selected)
    return selected, dp[n][capacity], total_weight, dp


def dijkstra(graph, source):
    """Return shortest distances and predecessor map from source."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[source] = 0
    unvisited = set(graph)

    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        if distances[current] == float("inf"):
            break
        unvisited.remove(current)
        for neighbor, weight in graph[current].items():
            if neighbor in unvisited:
                candidate = distances[current] + weight
                if candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    previous[neighbor] = current
    return distances, previous


def reconstruct_path(previous, target):
    """Reconstruct a path using Dijkstra's predecessor map."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    return list(reversed(path))


def all_pairs_shortest_paths(graph):
    """Run Dijkstra from each vertex to build a distance matrix."""
    result = {}
    for source in graph:
        result[source] = dijkstra(graph, source)[0]
    return result


def nearest_neighbor_tsp(nodes, distances, start="Depot"):
    """
    Approximate a delivery tour with nearest-neighbor.
    nodes contains delivery points; start is the depot.
    """
    remaining = set(nodes)
    remaining.discard(start)
    route = [start]
    total = 0
    current = start
    while remaining:
        next_node = min(remaining, key=lambda node: distances[current][node])
        total += distances[current][next_node]
        route.append(next_node)
        remaining.remove(next_node)
        current = next_node
    if current != start:
        total += distances[current][start]
        route.append(start)
    return route, total
