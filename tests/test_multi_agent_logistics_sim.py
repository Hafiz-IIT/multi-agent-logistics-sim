import unittest

from multi_agent_logistics_sim import Agent, Task, assign


class MultiAgentLogisticsTests(unittest.TestCase):
    def test_nearest_agent_selected(self):
        agents = [Agent("A", 0, 0, 5), Agent("B", 10, 0, 5)]
        result = assign(agents, [Task("T", 1, 0, 1)])
        self.assertEqual(result["assignments"]["T"], "A")

    def test_capacity_respected(self):
        agents = [Agent("A", 0, 0, 1)]
        result = assign(agents, [Task("T", 0, 0, 2)])
        self.assertEqual(result["unassigned"], ["T"])

    def test_capacity_updates_across_tasks(self):
        agents = [Agent("A", 0, 0, 3)]
        result = assign(agents, [Task("T1", 0, 0, 2), Task("T2", 0, 0, 2)])
        self.assertEqual(len(result["assignments"]), 1)
        self.assertEqual(len(result["unassigned"]), 1)

    def test_inputs_are_not_mutated(self):
        agents = [Agent("A", 0, 0, 3)]
        assign(agents, [Task("T1", 5, 5, 2)])
        self.assertEqual((agents[0].x, agents[0].y, agents[0].remaining_capacity), (0, 0, 3))

    def test_boolean_and_nonfinite_agent_task_values_rejected(self):
        with self.assertRaises(ValueError):
            Agent("A", True, 0, 5)
        with self.assertRaises(ValueError):
            Task("T", 0, 0, float("nan"))

    def test_distance_overflow_is_rejected_instead_of_assigning_infinite_cost(self):
        agents = [Agent("A", -1e308, 0, 5)]
        tasks = [Task("T", 1e308, 0, 1)]
        with self.assertRaises(OverflowError):
            assign(agents, tasks)

    def test_duplicate_ids_and_invalid_loads_are_rejected(self):
        with self.assertRaises(ValueError):
            assign([Agent("A", 0, 0, 5)], [Task("T", 0, 0, 1), Task("T", 1, 1, 1)])
        with self.assertRaises(ValueError):
            Task("bad", 0, 0, -1)


if __name__ == "__main__":
    unittest.main()
