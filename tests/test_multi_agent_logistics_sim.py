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


if __name__ == "__main__":
    unittest.main()
