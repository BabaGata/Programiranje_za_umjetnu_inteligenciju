import heapq


EMPTY_STEP_COST = 1
MUD_STEP_COST = 10
FEAR_OF_UNKNOWN = 6.66
UNKNOWN_STEP_COST = max(EMPTY_STEP_COST, MUD_STEP_COST) * FEAR_OF_UNKNOWN  # for unknown positions (not visible)
FEAR_OF_ENEMY = 10


# Function to find the shortest path from agent_pos to target_pos on the given grid,
#   and return direction in which the agent should move
def pathfinding_direction(agent_pos, target_pos, enemy_pos, grid):
    # args:
    #   agent_pos (tuple): agent coordinates
    #   target_pos (tuple): target coordinates
    #   enemy_pos (tuple): enemy coordinates
    #   grid (2D list): 2D grid describing the world
    #      -1 -> unknown
    #       0 -> empty space
    #       1 -> obstacle
    #       2 -> mud
    # return: direction, shortest_path
    #   direction: direction in which the agent will move, such as 'RIGHT', 'LEFT', 'UP', or 'DOWN'
    #   shortest_path: a list of coordinates (tuples) for visualization of the path, such as [(1, 3), (2, 3), ...]
    shortest_path = astar(agent_pos, target_pos, enemy_pos, grid)
    direction = get_direction(agent_pos, shortest_path)
    return direction, shortest_path


# Copy the rest of your previous pathfinding code here (from pathfinding_agent.py)

'''
In this implementation:
   - Optimize path directness:
        Enhance the heuristic function to encourage the agent to choose more direct paths (replace manhattan distance).
   - Prefer clean paths:
        Modify the algorithm to prioritize paths with fewer muddy positions.
   - Favor explored positions:
        Adjust the algorithm to give preference to positions that have already been explored.
   - Avoid the enemy:
        Adjust the cost calculation so the agent avoids the enemy.
'''

# A* algorithm for pathfinding:
def astar(agent_pos, target_pos, enemy_pos, grid):
    # Initialize start position and goal position
    start = agent_pos
    goal = target_pos

    # Create an open set as a priority queue and push the start position with priority 0
    open_set = []  # Priority queue to store nodes to be explored
    heapq.heappush(open_set, (0, start))  # Push start node with priority 0

    # Initialize dictionaries to track the parent of each position and the cost to reach each position
    came_from = {}  # Key: position, value: its parent (previous position on the path)
    g_cost = {start: 0}

    # While the open set is not empty:
    while open_set:
        current_cost, current_pos = heapq.heappop(open_set)

        # If the current position is the goal (found the shortest path):
        if current_pos == goal:
            path = reconstruct_path(came_from, start, goal)
            return path

        # Generate neighboring positions of the current position:
        neighbors = [
            (current_pos[0] + 1, current_pos[1]),
            (current_pos[0] - 1, current_pos[1]),
            (current_pos[0], current_pos[1] + 1),
            (current_pos[0], current_pos[1] - 1)
        ]

        # For each neighbor:
        for neighbor in neighbors:
            if is_valid(neighbor, grid):
                tentative_g_cost = g_cost[current_pos] + calculate_step_cost(neighbor, grid, enemy_pos)

                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g_cost
                    total_cost = tentative_g_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (total_cost, neighbor))
                    came_from[neighbor] = current_pos

    # If the goal is not reached, return an empty path
    return []


# Estimate the cost from position 'a' to position 'b' using the Manhattan distance:
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Calculate the step cost based on the type of terrain and presence of the enemy:
def calculate_step_cost(pos, grid, enemy_pos):
    row, col = pos
    terrain_cost = get_terrain_cost(grid[row][col])

    # Check if the position is adjacent to the enemy:
    if is_adjacent(pos, enemy_pos):
        return terrain_cost + FEAR_OF_ENEMY

    return terrain_cost


# Get the terrain cost based on the grid value:
def get_terrain_cost(value):
    if value == -1:  # Unknown
        return UNKNOWN_STEP_COST
    elif value == 0:  # Empty space
        return EMPTY_STEP_COST
    elif value == 1:  # Obstacle
        return float('inf')  # Impassable
    elif value == 2:  # Mud
        return MUD_STEP_COST
    else:
        return float('inf')


# Check if a given position is within the grid boundaries and corresponds to an empty space:
def is_valid(pos, grid):
    row, col = pos
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != 1


# Check if two positions are adjacent:
def is_adjacent(pos1, pos2):
    return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1


# Reconstruct the path from the target to the start using parent information:
def reconstruct_path(came_from, start, target):
    path = [target]
    while target != start:
        target = came_from[target]
        path.append(target)
    return path[::-1]


# Determine the direction from the current position to the next position along the shortest path:
def get_direction(current_pos, shortest_path):
    if len(shortest_path) < 2:
        return None
    next_pos = shortest_path[1]
    if next_pos[0] < current_pos[0]:
        return 'UP'
    elif next_pos[0] > current_pos[0]:
        return 'DOWN'
    elif next_pos[1] < current_pos[1]:
        return 'LEFT'
    elif next_pos[1] > current_pos[1]:
        return 'RIGHT'