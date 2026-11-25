import unittest
from courier.algorithms import (
    sort_parcels, knapsack_select, dijkstra,
    reconstruct_path, nearest_neighbor_tsp
)

class AlgorithmTests(unittest.TestCase):
    def test_sorting(self):
        parcels = [
            {"id":"A","priority":1,"deadline":2,"value":5},
            {"id":"B","priority":3,"deadline":5,"value":2},
            {"id":"C","priority":3,"deadline":1,"value":7}
        ]
        self.assertEqual([p["id"] for p in sort_parcels(parcels)], ["C","B","A"])

    def test_knapsack(self):
        parcels = [
            {"id":"A","weight":2,"value":3},
            {"id":"B","weight":3,"value":4},
            {"id":"C","weight":4,"value":5}
        ]
        chosen, value, weight, _ = knapsack_select(parcels, 5)
        self.assertEqual(value, 7)
        self.assertEqual(weight, 5)
        self.assertEqual({p["id"] for p in chosen}, {"A","B"})

    def test_dijkstra_and_path(self):
        graph = {"Depot":{"A":2,"B":8}, "A":{"Depot":2,"B":3}, "B":{"Depot":8,"A":3}}
        distances, previous = dijkstra(graph, "Depot")
        self.assertEqual(distances["B"], 5)
        self.assertEqual(reconstruct_path(previous, "B"), ["Depot","A","B"])

    def test_nearest_neighbor(self):
        dist = {
            "Depot":{"A":2,"B":5}, "A":{"Depot":2,"B":3},
            "B":{"Depot":5,"A":3}
        }
        route, length = nearest_neighbor_tsp(["Depot","A","B"], dist)
        self.assertEqual(route, ["Depot","A","B","Depot"])
        self.assertEqual(length, 10)

if __name__ == "__main__":
    unittest.main()
