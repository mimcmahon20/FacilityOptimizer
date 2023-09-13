##FUNCTIONING MULTIPLE FACILITIES, MULTIPLE WAREHOUSES, EUCLIDEAN DISTANCE, OPTIMIZATION
import numpy as np
from gurobipy import Model, GRB

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.lines import Line2D


#image loading/logic
def getImage(path, zoom):
    return OffsetImage(plt.imread(path), zoom=zoom)
warehouse_img = getImage('warehouse.png', 0.02)
facility_img = getImage('facility.png', 0.025)
optimal_img = getImage('optimal1.png', 0.03)
optimal_img_small = getImage('optimal1.png', 0.025)



# Variable to keep track of the game state
game_state = {
    "click_count": 0, 
    "number_of_facilities": 3,
    "warehouse_locations": None, 
    "demands": None,
    "facility_locations": None,
    "facility_supply_distribution": None,
    "facility_service_details": None
}

# Function to initialize a new game state
def initialize_game_state():
    warehouse_num = np.random.randint(16, 22)
    game_state["warehouse_locations"] = np.random.rand(warehouse_num, 2) * 100
    game_state["demands"] = np.random.randint(10, 101, warehouse_num)
    game_state["click_count"] = 0
    
    # Clear the existing plot and set limits
    ax.clear()
    ax.set_xlim(-10, 110)
    ax.set_ylim(-10, 110)
    
    ax.set_facecolor('#f0f0f0')
    ax.set_xticks([])
    ax.set_yticks([])
    
    
    
#     cmap = plt.get_cmap("YlOrRd")  # Yellow to Red colormap
#     for i, (x, y) in enumerate(game_state["warehouse_locations"]):
#         demand = game_state["demands"][i]
#         color = cmap((demand - 10) / 90)  # Normalize the demand to range [0, 1]
#         ax.plot(x, y, 's', color=color)  # Plot warehouse with color based on demand

    # Displays the warehouses
    for x, y in game_state["warehouse_locations"]:
        ax.add_artist(AnnotationBbox(warehouse_img, (x, y), frameon=False))

        
    
    # Display demands under the warehouses
    for i, (x, y) in enumerate(game_state["warehouse_locations"]):
        ax.text(x, y - 2, str(game_state["demands"][i]), color='black', fontsize=10, ha='center', va='top')
    
    # Call the new optimization function to find facility locations and supply distribution
    find_optimal_facility_locations()
    
    
    for j, (fx, fy) in enumerate(game_state["facility_locations"][1:]):  # Skip the first facility
        ax.add_artist(AnnotationBbox(facility_img, (fx, fy), frameon=False))
          
    
        # Create a new axes at the top left corner of the window
    legend_ax = fig.add_axes([0.01, 0.8, 0.5, 0.2])
    legend_ax.axis('off')

    # Create legend elements using the imported images
    legend_elements = [
        (warehouse_img, 'Warehouse'),
        (facility_img, 'Facility'),
        (optimal_img_small, 'Optimal Location')
    ]

    # Add the images and labels to the legend in two columns
    legend_ax.add_artist(AnnotationBbox(legend_elements[0][0], (0.05, 0.9), frameon=False))
    legend_ax.text(0.15, 0.9, legend_elements[0][1], verticalalignment='center')

    legend_ax.add_artist(AnnotationBbox(legend_elements[1][0], (0.05, 0.6), frameon=False))
    legend_ax.text(0.15, 0.6, legend_elements[1][1], verticalalignment='center')

    legend_ax.add_artist(AnnotationBbox(legend_elements[2][0], (0.55, 0.9), frameon=False))
    legend_ax.text(0.65, 0.9, legend_elements[2][1], verticalalignment='center')

    # Add a text label to describe the supply line representation
    legend_ax.text(0.55, 0.6, 'Supply Line (Darker = More Supply)', color='black', verticalalignment='center')

        
    
    plt.draw()

# New optimization function: find_optimal_facility_locations (as defined earlier in our conversation)
def find_optimal_facility_locations():
    # Accessing game_state without global keyword
    warehouse_locations = game_state["warehouse_locations"]
    demands = game_state["demands"]
    num_facilities = game_state["number_of_facilities"]
    # Calculate total demand and facility supply capacity
    total_demand = sum(demands)
    facility_supply_capacity = total_demand / num_facilities

    # Create a Gurobi model
    m = Model()

    # Define a grid of potential facility locations
    grid_size = 10
    facility_potential_locations = [(x, y) for x in range(0, 101, grid_size) for y in range(0, 101, grid_size)]


    # Pre-calculate distances from potential facility locations to warehouses
    distances = [[((wx - fx)**2 + (wy - fy)**2)**0.5 for wx, wy in warehouse_locations] for fx, fy in facility_potential_locations]

    # plot a red point at each potential facility location
    for x, y in facility_potential_locations:
        ax.plot(x, y, 'ro', markersize=2)

    # Define Variables
    facility_vars = [m.addVar(vtype=GRB.BINARY, name=f"f_{j}") for j in range(len(facility_potential_locations))]
    supply_vars = [[m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"s_{i}_{j}") for j in range(len(facility_potential_locations))] for i in range(len(warehouse_locations))]

    # Define Objective Function
    obj = sum(supply_vars[i][j] * distances[j][i] for i in range(len(warehouse_locations)) for j in range(len(facility_potential_locations)))
    m.setObjective(obj, GRB.MINIMIZE)

    # Define Constraints
    for i in range(len(warehouse_locations)):
        m.addConstr(sum(supply_vars[i][j] for j in range(len(facility_potential_locations))) == demands[i])

    for j in range(len(facility_potential_locations)):
        m.addConstr(sum(supply_vars[i][j] for i in range(len(warehouse_locations))) <= facility_supply_capacity * facility_vars[j])

    # Facility selection constraint: exactly num_facilities should be selected
    m.addConstr(sum(facility_vars) == num_facilities)

    # Optimize Model
    m.optimize()

    # Extract Results and Update game_state
    facility_locations = [(x, y) for j, (x, y) in enumerate(facility_potential_locations) if facility_vars[j].X > 0.5]
    game_state["facility_locations"] = facility_locations

    facility_supply_distribution = [[supply_vars[i][j].X for j in range(len(facility_potential_locations))] for i in range(len(warehouse_locations))]
    
    game_state["facility_supply_distribution"] = facility_supply_distribution
    
    # Update game_state with facility service details
    facility_service_details = []
    for j, (x, y) in enumerate(facility_locations):
        servicing_details = [(i, facility_supply_distribution[i][facility_potential_locations.index((x, y))]) for i in range(len(warehouse_locations)) if facility_supply_distribution[i][facility_potential_locations.index((x, y))] > 0]
        facility_service_details.append(servicing_details)
    game_state["facility_service_details"] = facility_service_details


    # Print the results in the specified format
    for j, (x, y) in enumerate(facility_locations):
        servicing_details = [(i, facility_supply_distribution[i][facility_potential_locations.index((x, y))]) for i in range(len(warehouse_locations)) if facility_supply_distribution[i][facility_potential_locations.index((x, y))] > 0]
        print(f"Facility {j+1} location: ({x}, {y}) servicing: {servicing_details}")

    
    return "success!"

# Function to calculate score
def calculate_score(user_x, user_y, optimal_x, optimal_y):
    distance = np.sqrt((user_x - optimal_x)**2 + (user_y - optimal_y)**2)
    score = min(1, 1 / max(1, distance))
    return score

# Create a plot and connect the event handler
fig, ax = plt.subplots(figsize=(10,10))


def draw_supply_lines(facility_index):
    """Draws lines from a facility to warehouses it supplies.

    Args:
        facility_index (int): Index of the facility in the game_state facility service details list.
    """
    facility_x, facility_y = game_state["facility_locations"][facility_index]
    servicing_details = game_state["facility_service_details"][facility_index]
    
    # Choose a colormap based on whether the facility is new or existing
    if facility_index == 0:
        cmap = plt.get_cmap("binary")  # Cool colors for the new facility
    else:
        cmap = plt.get_cmap("binary")   # Warm colors for existing facilities
    
    max_supply = max(servicing_details, key=lambda x: x[1])[1] if servicing_details else 1

    for warehouse_index, supply_amount in servicing_details:
        warehouse_x, warehouse_y = game_state["warehouse_locations"][warehouse_index]
        color = cmap(supply_amount / max_supply)
        ax.plot([facility_x, warehouse_x], [facility_y, warehouse_y], color=color)


# Event handler for click events
def on_click(event):
    
    game_state["click_count"] += 1
    
    cmap = plt.get_cmap("YlOrRd")  # Yellow to Red colormap
    
    if game_state["click_count"] % 2 == 1:
        user_x, user_y = event.xdata, event.ydata

        # Plot user-selected location
        ax.plot(user_x, user_y, 'go', markersize=15)  # Plot user guess as green circle

        # Find the optimal location for the first facility
        optimal_x, optimal_y = game_state["facility_locations"][0]
        
        # Calculate the score
        score = calculate_score(user_x, user_y, optimal_x, optimal_y)
        
        # Set the score as the title of the plot
        ax.set_title(f"Score: {score:.2f}")

        # Plot optimal location of the first facility and its corresponding paths
        ax.add_artist(AnnotationBbox(optimal_img, (optimal_x, optimal_y), frameon=False))
        
        #         ax.plot(optimal_x, optimal_y, 'bo', markersize=15)  # Plot optimal location as blue circle

        
        draw_supply_lines(0)
        
        for i in range(1, game_state["number_of_facilities"]):
            draw_supply_lines(i)
        
        plt.draw()
    else:
        # Reset the game state and start a new game
        initialize_game_state()

# Initialize the first game state
initialize_game_state()

# Connect the event handler
cid = fig.canvas.mpl_connect('button_press_event', on_click)

