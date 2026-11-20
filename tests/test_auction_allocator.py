import unittest

from auction_allocator import auction_assign, bid
from multi_agent_logistics_sim import Agent, Task


class AuctionAllocatorTests(unittest.TestCase):
    def test_infeasible_agent_does_not_bid(self):
        self.assertIsNone(bid(Agent("A", 0, 0, 1), Task("T", 0, 0, 2)))

    def test_closer_agent_wins_when_capacity_equal(self):
        agents = [Agent("A", 0, 0, 5), Agent("B", 10, 0, 5)]
        result = auction_assign(agents, [Task("T", 1, 0, 1)])
        self.assertEqual(result["assignments"]["T"], "A")

    def test_unassigned_task_is_explicit(self):
        result = auction_assign([Agent("A", 0, 0, 1)], [Task("T", 0, 0, 2)])
        self.assertEqual(result["unassigned"], ["T"])

    def test_auction_does_not_mutate_input_agents(self):
        agents = [Agent("A", 0, 0, 5)]
        auction_assign(agents, [Task("T", 2, 0, 2)])
        self.assertEqual((agents[0].x, agents[0].remaining_capacity), (0, 5))

    def test_boolean_penalty_and_invalid_direct_bid_rejected(self):
        with self.assertRaises(ValueError):
            auction_assign([Agent("A", 0, 0, 5)], [Task("T", 0, 0, 1)], load_penalty=True)
        with self.assertRaises(TypeError):
            bid(None, Task("T", 0, 0, 1))

    def test_negative_load_penalty_is_rejected(self):
        with self.assertRaises(ValueError):
            auction_assign([Agent("A", 0, 0, 5)], [Task("T", 0, 0, 1)], load_penalty=-1)


if __name__ == "__main__":
    unittest.main()
