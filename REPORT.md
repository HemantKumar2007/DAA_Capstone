# Capstone Report: Mini-Courier Planner

## 1. Problem statement
The Mini-Courier Planner simulates a courier service. Given parcels, a vehicle capacity and a weighted road graph, it prioritizes parcels, chooses a high-value feasible load, computes shortest paths and creates an approximate tour.

## 2. Data design
Each parcel has:
- **ID:** unique parcel identifier.
- **Destination:** delivery point in the road graph.
- **Priority:** integer from 1 (low) to 5 (high).
- **Deadline:** smaller integer means an earlier deadline.
- **Weight:** capacity consumed by the parcel.
- **Value:** benefit assigned to delivering the parcel.

The road network is an undirected weighted graph stored as an adjacency list in `data/graph.json`.

## 3. Algorithm selection and integration
1. **Sorting:** parcels are ordered by priority descending, deadline ascending and value descending.
2. **Dynamic programming:** 0/1 knapsack computes the maximum total value that fits in the vehicle.
3. **Dijkstra:** computes shortest distances from the depot and is also run from every node to build a distance matrix.
4. **Nearest-neighbor TSP:** repeatedly visits the closest unvisited selected destination, then returns to the depot.

The application integrates the four components in `main.py`.

## 4. Testing
The project includes:
- A sample parcel dataset and road graph.
- Automated unit tests for sorting, knapsack, Dijkstra/path reconstruction and nearest-neighbor routing.
- A benchmark script that tests increasing parcel counts (10, 50, 100, 250 and 500).
- CSV runtime output and a chart-generation script.

Run the tests and benchmarks using the commands in `README.md`. Runtime measurements are hardware-dependent; the supplied sample chart is illustrative and should be regenerated on the system used for final submission.

## 5. Complexity analysis
- Sorting: O(n log n) time.
- 0/1 Knapsack: O(nW) time and O(nW) space for the full DP table.
- Dijkstra implementation used here: O(V² + E) time, with O(V) auxiliary space.
- Nearest-neighbor tour: O(k²) time after the all-pairs distance matrix is available; all-pairs Dijkstra adds O(V(V² + E)) with this implementation.

## 6. Limitations and future improvements
- The nearest-neighbor heuristic may not find the globally shortest tour.
- Road weights are sample distances, not live map data.
- A heap-based Dijkstra implementation can improve shortest-path performance on sparse graphs.
- A more advanced TSP heuristic or local-search improvement can reduce route length.
- Real deployments could include vehicle limits, multiple vehicles, traffic and time windows.

## 7. Conclusion
The project demonstrates how sorting, dynamic programming, graph shortest paths and an approximation algorithm can be combined into one working courier-planning prototype.
