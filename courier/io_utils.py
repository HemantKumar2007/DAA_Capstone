"""Input loading and validation helpers."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_parcels(path=None):
    path = Path(path) if path else ROOT / "data" / "parcels.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    parcels = []
    for row in rows:
        parcels.append({
            "id": row["id"],
            "destination": row["destination"],
            "priority": int(row["priority"]),
            "deadline": int(row["deadline"]),
            "weight": int(row["weight"]),
            "value": int(row["value"])
        })
    return parcels

def load_graph(path=None):
    path = Path(path) if path else ROOT / "data" / "graph.json"
    with path.open(encoding="utf-8") as handle:
        raw = json.load(handle)
    return {node: {neighbor: float(weight) for neighbor, weight in edges.items()}
            for node, edges in raw.items()}
