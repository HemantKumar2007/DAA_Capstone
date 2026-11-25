"""Create a runtime chart from outputs/benchmark_results.csv."""
import csv
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
csv_path = ROOT / "outputs" / "benchmark_results.csv"
if not csv_path.exists():
    raise SystemExit("Run 'python benchmark.py' first.")
with csv_path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
sizes = [int(r["input_size"]) for r in rows]
for key, label in [
    ("sorting_seconds", "Sorting"),
    ("knapsack_seconds", "Knapsack DP"),
    ("dijkstra_seconds", "Dijkstra")
]:
    values = [float(r[key]) for r in rows]
    plt.plot(sizes, values, marker="o", label=label)
plt.xlabel("Number of parcels (Dijkstra uses fixed graph)")
plt.ylabel("Average runtime (seconds)")
plt.title("Mini-Courier Planner: Runtime Comparison")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
out = ROOT / "outputs" / "runtime_chart.png"
plt.savefig(out, dpi=160)
print(f"Chart saved to: {out}")
