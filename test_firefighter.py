import visualiser_random_forest_graph as vis
import graph_helper as gh
import random
import networkx
import scipy
from typing import List, Tuple, Dict 
import math
import time
import matplotlib.pyplot as plt
import Classes
import unittest

class TestFireFighter(unittest.TestCase):

    def setUp(self):
        # Set up a FireFighter instance and any necessary surrounding environment
        self.num_surrounding_nodes = 1000
        edges = [(0, i) for i in range(1, self.num_surrounding_nodes + 1)]

        self.graph = Classes.Graph(edges)  # Set as an attribute of self

        # Presuming these methods exist and modify the graph's state
        self.graph.create_node_list()
        self.graph.generate_adjacency_list()
        self.graph.generate_land_patches(1)
        self.graph.generate_fire_fighters(1)

        # Setting fire to a patch and initializing a firefighter
        #self.fire_patch = self.graph.search_landpatches(2)
        #self.fire_patch.set_is_on_fire(True)
        self.fire_fighter = self.graph.search_fire_fighters(0)  # Set as an attribute of self
        self.graph.update_fire_fighter_positions()
        self.graph.generate_colormap()

    def test_move(self):
        for _ in range(10):
            # Reset fire fighter position to be 0
            self.fire_fighter.set_current_position(0)
            
            # Choose a random node to set on fire
            fire_node_index = random.randint(1, self.num_surrounding_nodes)
            fire_patch = self.graph.search_landpatches(fire_node_index)
            fire_patch.set_is_on_fire(True)

            # Record the initial position of the firefighter and land patch on fire
            initial_firefighter_position = self.fire_fighter.get_current_position()
            fire_patch_position = fire_node_index

            # Move the firefighter
            self.fire_fighter.move()

            # Record the new position of the firefighter
            new_firefighter_position = self.fire_fighter.get_current_position()

            # Assertions to ensure the firefighter attempts to move towards the fire
            self.assertEqual(new_firefighter_position, fire_patch_position,
                                f"Firefighter position {new_firefighter_position} should be equal to {fire_patch_position}")
            print(new_firefighter_position, fire_patch_position)
            
            # Reset the fire for the next iteration if needed
            fire_patch.set_is_on_fire(False)

if __name__ == '__main__':
    unittest.main()
