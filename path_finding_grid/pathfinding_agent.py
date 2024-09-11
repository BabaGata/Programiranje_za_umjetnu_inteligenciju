import heapq


# Function to find the shortest path from agent_pos to target_pos on the given grid,
#   and return direction in which the agent should move
def pathfinding_direction(agent_pos, target_pos, grid):
    # args:
    #   agent_pos (tuple): agent coordinates
    #   target_pos (tuple): target coordinates
    #   grid (2D list): 2D grid describing the world
    #       0 -> empty space
    #       1 -> obstacle
    # return: direction, shortest_path
    #   direction: direction in which the agent will move, such as 'RIGHT', 'LEFT', 'UP', or 'DOWN'
    #   shortest_path: a list of coordinates (tuples) for visualization of the path, such as [(1, 3), (2, 3), ...]
    shortest_path = astar(agent_pos, target_pos, grid)
    direction = get_direction(agent_pos, shortest_path)
    return direction, shortest_path


# A* algorithm for pathfinding:
def astar(agent_pos, target_pos, grid):
    # Initialize start position and goal position
    start = agent_pos
    goal = target_pos

    # Create an open set as a priority queue and push the start position with priority 0
    open_set = []  # Priority queue to store nodes to be explored
    heapq.heappush(open_set, (0, start))  # Push start node with priority 0

    # Initialize dictionaries to track the parent of each position and the cost to reach each position
    came_from = {}  # Key: position, value: its parent (previous position on the path)
    g_cost = {start: 0}


    '''
    While the open set is not empty:
        Pop the position with the lowest priority from the open set (which is the current position).
            Hint: `heappop()`

        If the current position is the goal (found the shortest path):
            Reconstruct the path from the start to the goal using the parent information.
                Hint: `reconstruct_path()`
            Return the path.

        Generate neighboring positions of the current position.

        For each neighbor:
            If the neighbor is a valid position on the grid:
                Calculate the tentative cost to reach the neighbor.
                    Hint: tentative_g_cost = g_cost for the current position + 1

                If the neighbor is not in the g_cost dictionary or the tentative_g_cost is lower than its recorded g_cost:
                    Update the g_cost to reach the neighbor.
                    Calculate the combined (total) cost for the neighbor position (g_cost + heuristic cost).
                        Hint: `heuristic()`
                    Push the neighbor position and its total cost (as its priority) to the open set.
                    Update the parent of the neighbor.
                        Hint: `came_from`
    '''
    # YOUR CODE HERE
    while open_set:
        current_cost, current_pos = heapq.heappop(open_set)

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

        for neighbor in neighbors:
            if is_valid(neighbor, grid):
                tentative_g_cost = g_cost[current_pos] + 1

                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g_cost
                    total_cost = tentative_g_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (total_cost, neighbor))
                    came_from[neighbor] = current_pos

    # If the goal is not reached, return an empty path
    return []  # Target not reachable


# Estimate the cost from position 'a' to position 'b' using the Manhattan distance:
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Reconstruct the path from the target to the start using parent information:
def reconstruct_path(came_from, start, target):
    '''
    Create the path by traversing positions backwards from target until you reach the start position.
    Return the reversed path (to get the correct order).
    '''
    path = [target]
    while target != start:
        target = came_from[target]
        path.append(target)
    return path[::-1]


# Check if a given position is within the grid boundaries and corresponds to an empty space:
def is_valid(pos, grid):
    '''
    Return true if the row and column are within grid boundaries and the grid value at that position is 0.
    '''
    row, col = pos
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] == 0


# Determine the direction from the current position to the next position along the shortest path:
def get_direction(current_pos, shortest_path):
    '''
    Return None if shortest_path isn't a path (contains only one or zero positions).
    Compare the row and column values of the current and next positions.
    Return 'UP' if the next position is above, 'DOWN' if below, 'LEFT' if to the left, and 'RIGHT' if to the right.
    '''
    if len(shortest_path) < 2: return None
    next_pos = shortest_path[1]
    if next_pos[0] < current_pos[0]:
        return 'UP'
    elif next_pos[0] > current_pos[0]:
        return 'DOWN'
    elif next_pos[1] < current_pos[1]:
        return 'LEFT'
    elif next_pos[1] > current_pos[1]:
        return 'RIGHT'