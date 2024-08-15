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


if __name__ == "__main__":
    while True:
        print("\nWelcome to the program.\nThis program will simulate random forest fires on a random graph.\nType 1 or 2 and enter to make a choice.")
        graph = Classes.Graph()
        #Code to generate graph and adjacency list
        while True:
            print("\nFirst you will need to select how to create a graph:\n\n 1. Randomly generate graph\n 2. Load graph from file")
            user_input = input()

            if user_input == "1":
                try:
                    number_nodes_input = int(input("\nHow many nodes do you want in the graph?\nThe number of nodes will be around your chosen number.\nMinimum number must be 4, maximum should be under 300.\n"))

                    number_nodes = int(number_nodes_input)
                    if 4 <= number_nodes <= 300:
                        graph.generate_graph(number_nodes)
                        graph.create_node_list()
                        graph.generate_adjacency_list()
                        break
                    else:
                        print("\nNumber of nodes should be between 4 and 300.\nPlease try again.")
                        time.sleep(2)
                        continue
                except ValueError:
                    print("\nInvalid input.\nPlease enter a valid integer.\n")
                    time.sleep(2)
                    #continue
            
            elif user_input == "2":
                graph_file_input = input("\nWrite the name of your file.\n")
                try:
                    graph.load_graph(graph_file_input)
                    graph.create_node_list()
                    if len(graph.get_nodes()) < 4:
                        print("\nNumber of nodes was below 4, please check your graph or generate one instead.\n")
                        time.sleep(2)
                        continue
                    graph.generate_adjacency_list()
                    if gh.edges_planar(graph.get_edges()):
                        print("\nThe graph is planar.")
                    elif not gh.edges_planar(graph.get_edges()):
                        print("\nThe graph is not planar.\nPlease upload a planar and connected graph, or randomly generate one.")
                        time.sleep(2)
                        continue
                    if graph.is_connected():    
                        print("\nThe graph is connected.")
                    elif not graph.is_connected():
                        print("\nThe graph is not connected.\nPlease upload a planar and connected graph, or randomly generate one.")
                        time.sleep(2)
                        continue
                        
                    break
                except FileNotFoundError:
                    print("\nFile not found.\nPlease check the file name and path, and try again.\n")
                    time.sleep(2)
                    continue
                except Exception as e:
                    print(f"An error occurred while loading the file: {e}")
                    time.sleep(2)
                    continue

            else:
                print("\n\nInvalid input. Please enter 1 or 2.\n\n")
                time.sleep(2)
                continue
            
    
        #Code to generate fighters
        while True:
            print("\nYou can choose between generating fire fighters with default skill values between 0.4 and 0.6, or set their skill levels yourself.\n")
            user_input = input("\n1. Default values for fire fighters \n2. Generate and assign upper and lower skill level to fire fighters\n")
            
            if user_input == "1":
                print("\nSelect how many fire fighters to generate:\n")
                user_input = int(input())
                try:
                    amount_of_fire_fighters = int(user_input)
                    if amount_of_fire_fighters < 1 or amount_of_fire_fighters > 50:
                        print("\nAmount of fire fighters is recommended to be between 1 to 50.\nPlease try again.\n")
                        time.sleep(2)
                        continue
                    graph.generate_fire_fighters(amount_of_fire_fighters)
                except ValueError:
                    print("\nInvalid input.\nPlease enter a valid integer between 1 and 50, and not bigger than the amount of nodes.\n")
                    time.sleep(2)
                    continue
                break
            
            elif user_input == "2":
                print("\nSelect how many fire fighters to generate:\n")
                user_input = input()
                
                try:
                    amount_of_fire_fighters = int(user_input)
                    if amount_of_fire_fighters < 1 or amount_of_fire_fighters > 50:
                        print("\nAmount of fire fighters is recommended to be between 1 to 50.\nPlease try again.\n")
                        time.sleep(2)
                        continue
                except ValueError:
                    print("\nInvalid input.\nPlease enter a valid integer.\n")
                    time.sleep(2)
                    continue

                print("\nSelect the lower skill level for the fire fighters as a float from 0 to 1:\n")
                user_input = input()
                try:
                    lower_skill = float(user_input)
                    if lower_skill < 0.1 or lower_skill > 0.9:
                        print("\nLowest skill is recommended to be between 0.1 and 0.9\nPlease try again.\n")
                        time.sleep(2)
                        continue
                except ValueError:
                    print("\nInvalid input.\nPlease enter a valid float between 0.1 and 0.9\n")
                    time.sleep(2)
                    continue
                
                print("\nSelect the higher skill level for the fire fighters as a float from 0 to 1:\n")
                user_input = input()
                try:
                    higher_skill = float(user_input)
                    if higher_skill < 0.2 or higher_skill > 0.99:
                        print("\nHighest skill is recommended to be between 0.2 and 0.99\nPlease try again.\n")
                        time.sleep(2)
                        continue
                except ValueError:
                    print("\nInvalid input.\nPlease enter a valid float between 0.2 and 0.99\n")
                    time.sleep(2)
                    continue
                graph.generate_fire_fighters(amount_of_fire_fighters, lower_skill, higher_skill)
                break
        
        #Code to set probability of Trees and Rocks patches
        while True:
            print("\nSelect the probability that a land patch is a tree, with a float between 0 to 1.")
            print("The probability of a land patch to be a rock is 1 - the probability of it being a tree.")
            print("The option to make all nodes into trees is done by making the probability 1, while making all nodes into rocks is 0.\n")
            user_input = input()
            try:
                tree_probability = float(user_input)
                if tree_probability < 0 or tree_probability > 1:
                    print("\nThe probability to generate a tree must be between 0 and 1\nPlease try again.\n")
                    time.sleep(2)
                    continue
                graph.generate_land_patches(tree_probability)
                break
            except ValueError:
                print("\nInvalid input.\nPlease enter a valid float.\n")
                time.sleep(2)
                continue

        #Code to set probability for initial ignition
        while True:
            print("\nSelect the probability that a tree patch starts out on fire, with a float between 0 to 1.")
            print("The probability is checked for each tree in the graph.")
            print("Recommended to set to 0.1\n")
            user_input = input()
            try:
                ignite_probability = float(user_input)
                if ignite_probability < 0 or ignite_probability > 1:
                    print("\nThe probability to ignite a tree must be between 0 and 1\nPlease try again.\n")
                    time.sleep(2)
                    continue
                graph.initial_ignition(ignite_probability)
                break
            except ValueError:
                print("\nInvalid input.\nPlease enter a valid float.\n")
                time.sleep(2)
                continue
        
        #Code to set the amount of update steps for the simulation and run simulation
        while True:
            print("\nSelect the number of update steps for the simulation.")
            print("The recommended number is an integer between 2 and 100, but you can go beyond that to a maximum of 1000.")
            user_input = input()
            try:
                update_steps = int(user_input)
                if update_steps < 2 or update_steps > 1000:
                    print("\nPlease choose an integer between 2 and 1000\nPlease try again.\n")
                    time.sleep(2)
                    continue
                graph.run_simulation(update_steps)
                break
            except ValueError:
                print("\nInvalid input.\nPlease enter a valid integer.\n")
                time.sleep(2)
                continue
        
        #Code to make plot
        graph.show_plot()
        
        restart = None

        while restart == None:
            restart_choice = input("\nDo you want to run the program again?:\n1. Yes\n2. No\n")
            if restart_choice == "1":
                restart = True
            elif restart_choice == "2":
                restart = False
            else:
                print("\nPlease only enter 1 or 2.\n")
                time.sleep(2)
        
        if restart == True:
            continue
        elif restart == False:
            break
        