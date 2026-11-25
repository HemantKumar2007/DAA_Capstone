# Mini-Courier Planner

**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**University:** K.R. Mangalam University, Gurugram, Haryana  
**Project:** Capstone Assignment — Mini-Courier Planner

## 1. Project objective
This Python application prioritizes parcels, selects the best parcel combination for a vehicle with limited capacity, computes shortest paths on a road graph, and creates an approximate delivery tour.

## 2. Algorithms implemented
| Component | Algorithm | Purpose | Complexity |
|---|---|---|---|
| Parcel prioritization | Python comparison sort (Timsort) | Priority descending, deadline ascending, value descending | O(n log n) time |
| Packing | 0/1 Knapsack using Dynamic Programming | Maximize total parcel value under capacity | O(nW) time and O(nW) space for the displayed table |
| Shortest path | Dijkstra (simple array/set implementation) | Shortest distance from depot to every graph node | O(V² + E) time |
| Delivery tour | Nearest-neighbor TSP approximation | Build a practical route visiting selected destinations | O(k²) after distance matrix is available |

Here, n = number of parcels, W = vehicle capacity, V = graph vertices, E = graph edges, and k = number of delivery locations.

## 3. Project structure
```text
Mini_Courier_Planner/
├── main.py
├── benchmark.py
├── generate_chart.py
├── courier/
│   ├── __init__.py
│   ├── algorithms.py
│   └── io_utils.py
├── data/
│   ├── parcels.csv
│   └── graph.json
├── tests/
│   └── test_algorithms.py
├── outputs/
│   ├── sample_run.txt
│   ├── benchmark_results.csv
│   └── runtime_chart.png
├── requirements.txt
└── REPORT.md
```

## 4. Requirements
- Python 3.9 or newer
- Matplotlib is needed only to generate the runtime chart. The planner itself uses Python standard-library modules.

Install optional chart dependency:
```bash
python -m pip install -r requirements.txt
```

## 5. Run in VS Code
1. Extract the ZIP file.
2. Open the extracted `Mini_Courier_Planner` folder in VS Code.
3. Open Terminal → New Terminal.
4. (Optional) Create and activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
5. Run:
```bash
python main.py
```
To change vehicle capacity:
```bash
python main.py --capacity 20
```
If Windows uses the Python launcher, `py main.py` also works.

## 6. Performance testing
Run:
```bash
python benchmark.py
python generate_chart.py
```
The benchmark measures sorting and knapsack for 10, 50, 100, 250 and 500 parcels. Dijkstra is measured on the supplied fixed road graph. Results are saved in `outputs/benchmark_results.csv`; the chart is saved in `outputs/runtime_chart.png`. Actual timings vary by computer.

## 7. Run unit tests
From the project root:
```bash
python -m unittest discover -s tests -v
```

## 8. Input format
- `data/parcels.csv`: id, destination, priority (1–5), deadline (smaller means sooner), weight and value.
- `data/graph.json`: weighted, undirected road graph represented as adjacency lists. Each road must be listed in both directions.

## 9. Design decisions and limitations
- Knapsack selection is based on maximum value within capacity. Sorting is shown separately to demonstrate parcel prioritization; sorting does not force the knapsack result.
- The selected destination set is deduplicated before route construction.
- The nearest-neighbor TSP method is a heuristic, not a guaranteed optimal TSP solver. It returns to the depot at the end.
- Road distances are illustrative units, not real-world kilometres or live traffic distances.
- The benchmark is a local demonstration and should be rerun on the submission computer for its actual runtime evidence.
