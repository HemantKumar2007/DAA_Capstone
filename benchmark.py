"""Benchmark the main algorithms on increasing input sizes."""
import random
import time
import csv
from pathlib import Path
from courier.algorithms import sort_parcels, knapsack_select, dijkstra
from courier.io_utils import load_graph

random.seed(7)
OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)

def measure(fn, repeats=3):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return sum(samples) / len(samples)

def main():
    graph = load_graph()
    rows = []
    for n in (10, 50, 100, 250, 500):
        parcels = [{
            "id": f"P{i}", "destination": "A",
            "priority": random.randint(1, 5),
            "deadline": random.randint(1, 30),
            "weight": random.randint(1, 10),
            "value": random.randint(10, 100)
        } for i in range(n)]
        sort_s = measure(lambda: sort_parcels(parcels))
        # Capacity kept fixed to make the DP comparison practical.
        dp_s = measure(lambda: knapsack_select(parcels, 50))
        dijkstra_s = measure(lambda: dijkstra(graph, "Depot"))
        rows.append({"input_size": n, "sorting_seconds": sort_s,
                     "knapsack_seconds": dp_s, "dijkstra_seconds": dijkstra_s})
    out = OUT / "benchmark_results.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Benchmark results saved to: {out}")
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()
