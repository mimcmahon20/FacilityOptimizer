from pulp import LpMaximize, LpProblem, LpVariable

def solve_knapsack(items, max_weight):
    # Define the Linear Program
    model = LpProblem(name="knapsack-problem", sense=LpMaximize)

    # Define decision variables
    x = [LpVariable(name=f"x{i}", cat='Binary') for i in range(len(items))]

    # Define the objective function
    model += sum(x[i] * items[i]['value'] for i in range(len(items))), "Total_Value"

    # Define the weight constraint
    model += sum(x[i] * items[i]['weight'] for i in range(len(items))) <= max_weight, "Weight_Constraint"

    # Solve the problem
    model.solve()

    # Get the results
    selected_items = [int(var.varValue) for var in x]
    total_value = sum(items[i]['value'] * selected_items[i] for i in range(len(items)))

    return selected_items, total_value

# Example usage:
items = [{"weight": 10, "value": 60}, {"weight": 20, "value": 100}, {"weight": 30, "value": 120}]
max_weight = 50
result = solve_knapsack(items, max_weight)
print(result)