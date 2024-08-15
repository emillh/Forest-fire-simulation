import visualiser_random_forest_graph as vis
import graph_helper as gh
import random
import networkx
import scipy
from typing import List, Tuple, Dict
import math
import time
import matplotlib.pyplot as plt
from collections import deque

class Graph:
    def __init__(self, edges=None, pos_nodes=None):
        """Initializes the Graph class, with edges and pos_nodes as optional parameters"""
        self.edges = edges if edges is not None else [] # List of tuples representing the edges
        self.positions = pos_nodes if pos_nodes is not None else {} #Dictionary mapping node ID's to position tuples
        self.color_map = {} #Dictionary mapping node ID's and colors
        self.adj_list = {} #Dictionary mapping node ID's to neighbors
        self.land_patches = {} #Dictionary mapping node ID's to land patches
        self.fire_fighters = {}
        self.fire_fighter_positions = []
        
        self.nodes = set()
        
        self.node_list = list()
        
        self.updates = [0] #Starts with 0 for the initial generation of the graph
        self.tree_patches = []
        self.rock_patches = []
        self.wild_fires = []
    
    def get_edges(self):
        """Retrieves all edges of the graph as a list of tuples."""
        return self.edges
    
    def get_positions(self):
        """Retrieves the positions of all nodes in the graph."""
        return self.positions
    
    def get_colormap(self):
        """Retrieves the color map used for nodes in the graph."""
        return self.color_map
    
    def get_adj_list(self):
        """Retrieves the adjacency list representation of the graph."""
        return self.adj_list
    
    def get_landpatches(self):
        """Retrieves land patches associated with the graph."""
        return self.land_patches
    
    def get_nodes(self):
        """Retrieves all nodes of the graph."""
        return self.nodes
    
    def get_fire_fighters(self):
        """Retrieves all fire fighters associated with the graph."""
        return self.fire_fighters
    
    def get_fire_fighter_positions(self):
        """Retrieves the positions of all fire fighters in the graph."""
        return self.fire_fighter_positions
    
    def create_node_list(self):
        """Creates and initializes a list of nodes for the graph"""
        for edge in self.edges:
            self.nodes.update(edge)
        self.node_list = list(self.nodes)
    
    def search_adj_list_neighbors(self, node_id):
        """ 
        Searches and retrieves the neighbors of a given node using the adjacency list.
        """
        return self.adj_list.get(node_id, [])
    
    def search_landpatches(self, node_id):
        """
        Searches and retrieves land patches associated with a given node.
        """
        return self.land_patches.get(node_id)
    
    def search_fire_fighters(self,fire_fighter_id):
        """
        Searches for and retrieves fire fighters based on their identifiers. Useful in simulations where fire fighters are tracked.
    
        """
        return self.fire_fighters.get(fire_fighter_id)

    def generate_graph(self, num_nodes:int):
       """ Generates a graph structure with a specified number of nodes"""
       self.edges, self.positions = gh.voronoi_to_edges(num_nodes)
    
    def generate_colormap(self):
        """
        Generates a color map for the nodes in the graph"""
        self.color_map = {}

        for node in self.get_landpatches():
            land = self.search_landpatches(node)
            if type(land) == Treepatch:
                if not land.get_is_on_fire():
                    self.color_map[node] = land.get_treestats()
                elif land.get_is_on_fire():
                    stats = land.get_treestats()
                    self.color_map[node] = stats - 256 #256 is the maximum treestat, therefore max will be 0 - 256 for the color -256
            elif type(land) == Rockpatch:
                pass
    
    def generate_adjacency_list(self):
        """Generates or the adjacency list of the graph based on its current nodes and edges."""
        for edge in self.edges:
            a, b = edge

            if a not in self.adj_list:
                self.adj_list[a] = []
            if b not in self.adj_list:
                self.adj_list[b] = []
            
            self.adj_list[a].append(b)
            self.adj_list[b].append(a)
    
    def generate_land_patches(self, probability_tree=0.8):
        """Generates land patches based on a given probability."""
        for node in self.nodes:
            patch = random.choices(["tree", "rock"], weights=[probability_tree, 1- probability_tree], k=1)[0]
            if patch == "tree":
                self.land_patches[node] = Treepatch(node, self, treestats=100)
            elif patch == "rock":
                self.land_patches[node] = Rockpatch(node, self)

    def generate_fire_fighters(self, amount_to_create:int, skill_level_lower=0.4,skill_level_higher=0.6):
        """Generates a specified number of fire fighters with skills ranging between given levels."""
        self.fire_fighters
        start_positions = random.sample(self.node_list,amount_to_create)
        for i in range(amount_to_create):
            self.fire_fighters[i] = FireFighter(i,self,start_positions[i],random.uniform(skill_level_lower,skill_level_higher))

    def update_colormap(self, node_id, color):
        """Updates the color of a specific node in the graph's color map."""
        self.color_map[node_id] = color

    def update_fire_fighter_positions(self):
        """Updates the positions of all fire fighters in the graph."""
        self.fire_fighter_positions = []
        for fire_fighter_id in self.fire_fighters:
            fire_fighter = self.search_fire_fighters(fire_fighter_id)
            self.fire_fighter_positions.append(fire_fighter.get_current_position())

    def add_edge(self, node1_id, node2_id):
        """ Adds an edge between two specified nodes in the graph, effectively connecting them."""
        # Add an edge to the graph
        self.edges.append((node1_id, node2_id))
        
    
    def initial_ignition(self, probability_ignition=0.1):
        """ Initiates ignition in the graph based on a probability."""
        for node in self.get_nodes():
            landpatch = self.search_landpatches(node)
            if isinstance(landpatch, Treepatch):
                chance_to_ignite = random.random()
                if chance_to_ignite <= probability_ignition:
                    landpatch.set_is_on_fire(True)
    
    def is_connected(self):
        """
        Checks if all nodes in the graph are connected.

        Args:
        graph (list of tuples): Each tuple represents an edge between two nodes.

        Returns:
        bool: True if the graph is connected, False otherwise. If False, the graph is modified to become connected.
        """
        if not self.nodes:  # Quick return if no nodes in the graph
            return True

        visited = set()
        queue = deque([next(iter(self.nodes))])  # Start BFS from an arbitrary node

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                # Add all unvisited neighbors to the queue
                neighbors = self.search_adj_list_neighbors(node)
                queue.extend([neighbor for neighbor in neighbors if neighbor not in visited])

        # If all nodes are visited, graph is connected
        if len(visited) == len(self.nodes):
            return True
        else:
            return False
    
    def load_graph(self, data_file: str):
        """
        Loads a graph from a specified file.

        The file is expected to contain lines with two comma-separated integers each, representing an edge in the graph.
        Lines starting with '#' are considered comments and ignored. Incomplete tuples and empty lines are skipped.

        Args:
        data_file (str): The path to the file containing the graph data.

        Returns:
        list: A list of tuples representing the edges of the graph.

        Example:
        >>> graph = load_graph('test_file.dat')
        >>> isinstance(graph, list)
        True
        >>> all(isinstance(edge, tuple) and len(edge) == 2 for edge in graph)
        True
        >>> len(graph)  # Number of complete tuples in the file
        2
        """
        with open(data_file, "r") as data:
            self.edges = []
            
            for line in data:
                if not line.strip() or line.strip().startswith("#"):
                    continue
                
                parts = line.strip().strip("()").split(",")

                if len(parts) == 2:
                    try:
                        self.edges.append((int(parts[0]), int(parts[1])))
                    except ValueError:
                        print("\n\nThere was an incomplete entry in your graph file.\nThe entry has been ignored, but if you want all entries in the graph, please go back and fix the wrong entry.")
                        time.sleep(2)
                        continue # If conversion to int fails, skip line
    
    def count_patches(self, node_id):
        """Counts and returns the number of trees, rocks and fires on a specific node and returns it."""
        current_land = self.search_landpatches(node_id)
        tree = 0
        rock = 0
        fire = 0
        if isinstance(current_land, Treepatch):
            tree = 1
            if current_land.get_is_on_fire():
                fire = 1
        elif isinstance(current_land, Rockpatch):
            rock = 1
        return tree, rock, fire
        
    def run_simulation(self, update_steps:int):
        """Runs a simulation on the graph for a specified number of update steps."""
        initial_tree_patches = 0
        initial_rock_patches = 0
        initial_wild_fires = 0
        
        #Get initial amount of trees, rocks and fires
        for node_id in self.get_nodes():
            current_land = self.search_landpatches(node_id)
            if isinstance(current_land, Treepatch):
                initial_tree_patches += 1
                if current_land.get_is_on_fire():
                        initial_wild_fires += 1
            elif isinstance(current_land, Rockpatch):
                    initial_rock_patches += 1
        
        self.tree_patches.append(initial_tree_patches)
        self.rock_patches.append(initial_rock_patches)
        self.wild_fires.append(initial_wild_fires)

        update_steps = update_steps

        visual = vis.Visualiser(self.get_edges(), pos_nodes=self.get_positions())
        visual.update_node_colours(self.get_colormap())
        visual.update_node_edges(self.get_fire_fighter_positions())

        for steps in range(update_steps):
            trees = 0
            rocks = 0
            fires = 0
            for node_id in self.get_nodes():
                change_land = self.search_landpatches(node_id)
                change_land.update_land()
                tree, rock, fire = self.count_patches(node_id)
                trees += tree
                rocks += rock
                fires += fire
            self.tree_patches.append(trees)
            self.rock_patches.append(rocks)
            self.wild_fires.append(fires)
            self.updates.append(steps + 1)

            for fire_fighter_id in self.get_fire_fighters():
                fire_fighter = self.search_fire_fighters(fire_fighter_id)
                fire_fighter.move()
            self.update_fire_fighter_positions()
            self.generate_colormap()
            
            visual.update_node_colours(self.get_colormap())
            visual.update_node_edges(self.get_fire_fighter_positions())

        visual.wait_close()
    
    def show_plot(self):
        """Shows the reporting part of the simulation, where statistics are shown."""
        plt.plot(self.updates, self.tree_patches, label="Tree Patches", color="green")
        plt.plot(self.updates, self.rock_patches, label="Rock Patches", color="gray")
        plt.plot(self.updates, self.wild_fires, label="Wild Fires", color="red")
        plt.xlabel("Update Steps")
        plt.ylabel("Count")
        plt.title("Simulation Over Time")
        plt.legend()
        plt.show()

class Landpatch:
    """The base class for the tree and rock patch, with basic functionality."""
    def __init__(self, id: int, graph: Graph):
        self.id = id
        self.graph = graph
        self.neighbors = graph.search_adj_list_neighbors(id) # This should be a list of neighbor IDs

    def get_neighbors(self):
        """Return the ID of the next neighbors to the present patch."""
        return self.neighbors
    
    def get_id(self):
        """Returns the id of this landpatch."""
        return self.id
    
    def search_neighbors_to_landpatch(self, id):
        """Returns the neighbors to this landpatch."""
        return graph.search_landpatches(id)


class Rockpatch(Landpatch):
    """Create a rockpatch, a subclass of the landpatch class."""
    def __init__(self, id: int, graph: Graph):
        super().__init__(id, graph)

    def mutate(self):
        """Create a treepatch and replace it in the landpatches dictionary, where this rockpatch used to be."""
        new_treepatch = Treepatch(self.id, self.graph)
        self.graph.land_patches[self.id] = new_treepatch
    
    def update_land(self):
        """Updates the rockpatch, which means seeing if it should randomly become a treepatch with a chance of 1%"""
        chance_to_convert = random.randint(1,100)
        if chance_to_convert == 1:
            self.mutate()


class Treepatch(Landpatch):
    """Creates a treepatch, which has special properties like tree stats, is on fire and has fire fighter."""
    def __init__(self, id: int, graph:Graph, treestats=100):
        super().__init__(id, graph)
        self.treestats = treestats  # Health of the Treepatch, default value is 100
        self.is_on_fire = False
        self.has_fire_fighter = False
        self.local_fire_fighter = None

    def update_land(self):
        """Updates the value of treestats due to fire or firefighter action, representing one step of time evolution."""
        if self.is_on_fire == False and self.treestats <= 246:
            self.treestats += 10

        elif self.is_on_fire == True and self.has_fire_fighter == False:
            self.treestats -= 20
            self.spread_fire()

        elif self.is_on_fire == True and self.has_fire_fighter == True:
            if self.local_fire_fighter is None:
                for fire_fighter_id in self.graph.get_fire_fighters():
                    current_fire_fighter = self.graph.search_fire_fighters(fire_fighter_id)
                    if current_fire_fighter.get_current_position() == self.get_id():
                        self.set_local_fire_fighter(current_fire_fighter)
                        break
            if self.local_fire_fighter:
                skill_boost = self.local_fire_fighter.get_skill_level() * 100
                self.treestats += skill_boost
                if self.treestats >= 150:
                    self.set_is_on_fire(False)
                    self.set_local_fire_fighter(None)
                    self.set_has_fire_fighter(False)
        
        if self.treestats <= 0:
            self.mutate()
            

    def mutate(self):
        """Create a rockpatch and replace it in the landpatches dictionary, where this treepatch used to be."""
        new_rockpatch = Rockpatch(self.id, self.graph)
        self.graph.land_patches[self.id] = new_rockpatch
        
    def get_is_on_fire(self):
        """Retrieves the boolean value of whether this treepatch is on fire."""
        return self.is_on_fire
    
    def get_treestats(self):
        """Retrieves the treestats of this treepatch"""
        return self.treestats
    
    def get_has_fire_fighter(self):
        """Retrieves whether this treepatch has a fire fighter present"""
        return self.has_fire_fighter
    
    def get_local_fire_fighter(self):
        """Retrieves the local fire fighter object"""
        return self.local_fire_fighter

    def set_is_on_fire(self, status:bool):
        """Sets the status of the treepatch to be on fire"""
        self.is_on_fire = status
    
    def set_has_fire_fighter(self, status:bool):
        """Sets the status of the treepatch to be true that it has a fire fighter"""
        self.has_fire_fighter = status
    
    def set_local_fire_fighter(self, local_fire_fighter):
        """Sets the local fire fighter to be the fire fighter given as argument"""
        self.local_fire_fighter = local_fire_fighter

    def spread_fire(self, probability_spread_fire=0.3):
        """Spreads fire to neighbor patches with a 30% chance"""
        for neighbor_id in self.get_neighbors():
            neighbor_land = self.graph.search_landpatches(neighbor_id)
            if isinstance(neighbor_land, Treepatch) and neighbor_land.get_is_on_fire() == False:
                fire_spread = random.choices([True, False], weights=[probability_spread_fire,1-probability_spread_fire],k=1)[0]
                if fire_spread:
                    neighbor_land.set_is_on_fire(True)
            

class FireFighter:
    """Creates a new fire fighter and gives it a starting position in the graph"""
    def __init__(self, id:int, graph:Graph, start_node_id:int, skill_level=0.5):
        self.id = id
        self.graph = graph
        self.current_position = start_node_id
        self.skill_level = skill_level
    
    def get_id(self):
        """Retrieves the id of this fire fighter"""
        return self.id
    
    def get_current_position(self):
        """Retrieves the current position of this fire fighter"""
        return self.current_position
    
    def set_current_position(self, new_position_id:int):
        """Sets the current position of this fire fighter"""
        self.current_position = new_position_id
    
    def get_skill_level(self):
        """Sets the skill level of this fire fighter"""
        return self.skill_level
    
    def move(self):
        """This moves the fire fighters to a neighboring node if there is fire on it, else it moves randomly"""
        current_land = self.graph.search_landpatches(self.get_current_position())
        neighbors = self.graph.search_adj_list_neighbors(self.get_current_position())
        if isinstance(current_land,Treepatch) and current_land.get_is_on_fire():
            current_land.set_has_fire_fighter(True)
        else:
            found_new_position = False
            for neighbor in neighbors:
                landpatch = self.graph.search_landpatches(neighbor)
                if isinstance(landpatch, Treepatch) and landpatch.get_is_on_fire() and landpatch.get_has_fire_fighter() == False and found_new_position == False:
                    self.current_position = landpatch.get_id()
                    found_new_position = True
                    break
                else:
                    continue
            if found_new_position == False:
                next_position = random.choices(neighbors)[0]
                self.current_position = next_position
