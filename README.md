# Optimization Game with Multiple Facilities and Warehouses

## Overview

In this interactive game, the objective is to guess the optimal location for a new facility based on a set of randomly generated warehouses and their respective demands. The game leverages the Gurobi optimizer to calculate the optimal locations for facilities, minimizing the total Euclidean distance between facilities and the warehouses they serve. The game visually represents warehouses, facilities, and optimal locations with different images to enhance the gaming experience. 

## Key Features

1. **Multiple Facilities & Warehouses**: The game supports a scenario with multiple facilities and warehouses, facilitating a complex and realistic simulation.
2. **Euclidean Distance Optimization**: The script uses the Gurobi optimizer to determine the optimal locations for facilities, minimizing the total Euclidean distance to the warehouses they service.
3. **Visual Insights**: Utilizes images to represent warehouses, facilities, and optimal locations, providing a graphical insight into the optimization problem.
4. **Interactive Gameplay**: Players can interactively guess the optimal location of a new facility. The score is calculated based on the proximity of the guess to the actual optimal location determined by the optimization algorithm.

## Usage

1. **Initializing the Game**: Execute the script to initialize the game. It will generate a random set of warehouse locations and their respective demands, and determine the optimal facility locations based on the current setup.
2. **Playing the Game**: Players can click on the plot to guess the optimal location for a new facility. The score, based on the proximity of the guess to the actual optimal location, will be displayed.
3. **Next Round**: Click on the plot again to initiate a new round with fresh warehouse locations and demands.

## Code Structure

- `game_state`: A dictionary holding the current state of the game, including warehouse locations, demands, and facility details.
- `initialize_game_state()`: A function to set up a new game state with random warehouse locations and demands.
- `find_optimal_facility_locations()`: A function that employs the Gurobi optimizer to find the optimal facility locations based on current warehouse locations and demands.
- `calculate_score(user_x, user_y, optimal_x, optimal_y)`: Computes the score based on the proximity of the user's guess to the optimal location.
- `draw_supply_lines(facility_index)`: A function to draw lines from a facility to the warehouses it supplies, with line darkness indicating the quantity of supply.
- `on_click(event)`: An event handler for click events, which manages the user's guesses and initiates new rounds.

### Customization

- Modify the number of facilities and the range of warehouses and demands in the `game_state` dictionary.
- Adjust the plot window and marker sizes in the `fig, ax = plt.subplots(figsize=(10,10))` line and the marker size parameters in the `ax.plot()` calls.

## Dependencies

- numpy
- gurobipy
- matplotlib

## Execution

To engage in the game, run the script in a Python environment where the required packages are installed. Make guesses by clicking on the plot. The game will automatically progress, providing feedback on your guesses.

## Legend Representation

- **Warehouse**: Represented by the image loaded from 'warehouse.png'. It marks the location of a warehouse on the plot.
- **Facility**: Depicted by the image loaded from 'facility.png'. It indicates the location of a facility on the plot.
- **Optimal Location**: Illustrated by the image loaded from 'optimal1.png'. It signifies the optimal location for a new facility in the game.
- **Supply Line**: The lines connecting facilities and warehouses denote the supply lines. A darker line implies a higher quantity of supply from the facility to the warehouse.
