"""Run the Mini-Courier Planner from the project root."""
import argparse
import time
from courier.algorithms import (
    sort_parcels, knapsack_select, dijkstra,
    reconstruct_path, all_pairs_shortest_paths, nearest_neighbor_tsp
)
from courier.io_utils import load_parcels, load_graph

def run(capacity=15, verbose=True):
    parcels = load_parcels()
    graph = load_graph()

    t0 = time.perf_counter()
    prioritized = sort_parcels(parcels)
    sort_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    selected, value, weight, dp = knapsack_select(prioritized, capacity)
    knapsack_time = time.perf_counter() - t0

    destinations = sorted({p["destination"] for p in selected})
    if "Depot" not in graph:
        raise ValueError("The graph must contain a Depot node.")
    missing = [d for d in destinations if d not in graph]
    if missing:
        raise ValueError(f"Destinations missing from graph: {missing}")

    t0 = time.perf_counter()
    distances, previous = dijkstra(graph, "Depot")
    shortest_path_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    matrix = all_pairs_shortest_paths(graph)
    route, route_distance = nearest_neighbor_tsp(
        ["Depot"] + destinations, matrix, "Depot"
    )
    tsp_time = time.perf_counter() - t0

    result = {
        "prioritized": prioritized,
        "selected": selected,
        "total_value": value,
        "total_weight": weight,
        "capacity": capacity,
        "route": route,
        "route_distance": route_distance,
        "distances": distances,
        "previous": previous,
        "timings": {
            "Sorting": sort_time,
            "Knapsack DP": knapsack_time,
            "Dijkstra": shortest_path_time,
            "TSP approximation": tsp_time
        }
    }
    if verbose:
        print("\n========== MINI-COURIER PLANNER ==========")
        print(f"Vehicle capacity: {capacity}")
        print("\n1) PARCEL PRIORITIZATION")
        for p in prioritized:
            print(f"  {p['id']} -> {p['destination']}: priority={p['priority']}, "
                  f"deadline={p['deadline']}, weight={p['weight']}, value={p['value']}")
        print("\n2) OPTIMAL PACKING (0/1 KNAPSACK)")
        for p in selected:
            print(f"  Selected: {p['id']} -> {p['destination']} "
                  f"(weight {p['weight']}, value {p['value']})")
        print(f"  Total packed weight: {weight}/{capacity}")
        print(f"  Maximum packing value: {value}")
        print("\n3) SHORTEST PATHS FROM DEPOT (DIJKSTRA)")
        for node in sorted(graph):
            print(f"  Depot -> {node}: {distances[node]}")
        print("\n4) DELIVERY TOUR (NEAREST-NEIGHBOR TSP APPROXIMATION)")
        print("  Route: " + " -> ".join(route))
        print(f"  Total route distance: {route_distance}")
        print("\n5) ALGORITHM RUNTIME")
        for name, seconds in result["timings"].items():
            print(f"  {name}: {seconds:.8f} seconds")
        print("\nNote: runtime depends on hardware and input size.")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini-Courier Planner")
    parser.add_argument("--capacity", type=int, default=15,
                        help="Maximum vehicle capacity (default: 15)")
    args = parser.parse_args()
    if args.capacity < 0:
        parser.error("capacity must be non-negative")
    run(args.capacity)
