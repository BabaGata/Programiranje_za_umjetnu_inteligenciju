import pygame
import sys
import random
from pathfinding_agent import pathfinding_direction, heuristic


pygame.init()

# Constants
GRID_SIZE = 30  # 42
GRID_WIDTH = 30  # 20
GRID_HEIGHT = 30  # 20
VISIBLE_RANGE = 4

AGENT_COLOR = (50, 100, 255)
OBSTACLE_COLOR = (150, 150, 150)
MUD_COLOR = (40, 20, 5)
GRID_LINE_COLOR = (50, 50, 50)
TARGET_COLOR = (255, 100, 50)
FLOOR_COLOR = (0, 0, 0)
UNKNOWN_COLOR = (50, 0, 50)
ENEMY_COLOR = (50, 255, 50)

"""AGENT_COLOR = (75, 75, 250)
OBSTACLE_COLOR = (10, 10, 10)
MUD_COLOR = (170, 140, 130)
GRID_LINE_COLOR = (50, 50, 50)
TARGET_COLOR = (250, 75, 75)
FLOOR_COLOR = (250, 250, 250)
UNKNOWN_COLOR = (200, 250, 200)"""

# Create the grid with randomly placed obstacles (and mud)
grid = [[1 if random.random()<0.2 else 0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
grid = [[2 if (random.random()<0.3 and grid[col][row] == 0) else grid[col][row] for col in range(GRID_WIDTH)] for row in range(GRID_HEIGHT)]
grid[0][0] = 0
grid[0][1] = 0
grid[1][0] = 0
grid[1][1] = 0
grid[GRID_HEIGHT-1][GRID_WIDTH-1] = 0
grid[GRID_HEIGHT-1][GRID_WIDTH-2] = 0
grid[GRID_HEIGHT-2][GRID_WIDTH-1] = 0
grid[GRID_HEIGHT-2][GRID_WIDTH-2] = 0
# Create the visible_grid
visible_grid = [[-1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
visible_grid[0][0] = 0
visible_grid[GRID_HEIGHT-1][GRID_WIDTH-1] = 0

# Initialize Pygame window
screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
pygame.display.set_caption("Grid Environment")

# Agent starting position
agent_pos = [0, 0]

# Target position
target_pos = [GRID_HEIGHT - 1, GRID_WIDTH - 1]

# Enemy position
enemy_pos = [GRID_HEIGHT - 1, GRID_WIDTH - 1]

# List of coordinates in a path, for visualization
path = []

prev_mouse_row, prev_mouse_col = None, None
prev_direction = None
mud_slowdown = False
enemy_mud_slowdown = False


# Main loop
sim_iter = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif False and event.type == pygame.KEYDOWN:
            # Move the agent based on key presses
            if event.key == pygame.K_UP and agent_pos[0] > 0 and grid[agent_pos[0] - 1][agent_pos[1]] != 1:
                agent_pos[0] -= 1
            elif event.key == pygame.K_DOWN and agent_pos[0] < GRID_HEIGHT - 1 and grid[agent_pos[0] + 1][agent_pos[1]] != 1:
                agent_pos[0] += 1
            elif event.key == pygame.K_LEFT and agent_pos[1] > 0 and grid[agent_pos[0]][agent_pos[1] - 1] != 1:
                agent_pos[1] -= 1
            elif event.key == pygame.K_RIGHT and agent_pos[1] < GRID_WIDTH - 1 and grid[agent_pos[0]][agent_pos[1] + 1] != 1:
                agent_pos[1] += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            prev_mouse_row, prev_mouse_col = None, None
        
        mouse_buttons = pygame.mouse.get_pressed()
        # Check if the left mouse button is held down
        if mouse_buttons[0]:
            # Add/Remove obstacle when the left mouse button is held down
            x, y = pygame.mouse.get_pos()
            row = y // GRID_SIZE
            col = x // GRID_SIZE
            if (row, col) != (prev_mouse_row, prev_mouse_col) and agent_pos != [row, col] and target_pos != [row, col]:
                prev_mouse_row, prev_mouse_col = row, col
                if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                    if grid[row][col] == 1:
                        grid[row][col] = 0
                    else:
                        grid[row][col] = 1
                    visible_grid[row][col] = grid[row][col]

        # Check if the middle mouse button is held down
        elif mouse_buttons[1]:
            # Move the agent position
            x, y = pygame.mouse.get_pos()
            row = y // GRID_SIZE
            col = x // GRID_SIZE
            if grid[row][col] != 1:
                agent_pos = [row, col]

        # Check if the right mouse button is held down
        elif mouse_buttons[2]:
            # Move the target position
            x, y = pygame.mouse.get_pos()
            row = y // GRID_SIZE
            col = x // GRID_SIZE
            if grid[row][col] != 1:
                target_pos = [row, col]


    # Randomly reposition the target
    if agent_pos == target_pos:
        while True:
            target_pos = [random.randint(0, GRID_HEIGHT-1), random.randint(0, GRID_WIDTH-1)]
            if grid[target_pos[0]][target_pos[1]] != 1:
                break

    # Update visible_grid
    for y_offset in range(-VISIBLE_RANGE, VISIBLE_RANGE+1):
        for x_offset in range(-VISIBLE_RANGE, VISIBLE_RANGE+1):
            if 0 <= agent_pos[0] + y_offset < GRID_HEIGHT\
            and 0 <= agent_pos[1] + x_offset < GRID_WIDTH\
            and heuristic((0, 0), (y_offset, x_offset)) < VISIBLE_RANGE:
                y, x = agent_pos[0] + y_offset, agent_pos[1] + x_offset
                visible_grid[y][x] = grid[y][x]

    # Agent movement
    if sim_iter % 2 == 0 and agent_pos != target_pos:
        if mud_slowdown > 0:
            mud_slowdown -= 1
        else:
            # Update the agent's position based on the previous calculated direction
            if prev_direction == "UP" and agent_pos[0] > 0 and grid[agent_pos[0] - 1][agent_pos[1]] != 1:
                agent_pos[0] -= 1
            elif prev_direction == "DOWN" and agent_pos[0] < GRID_HEIGHT - 1 and grid[agent_pos[0] + 1][agent_pos[1]] != 1:
                agent_pos[0] += 1
            elif prev_direction == "LEFT" and agent_pos[1] > 0 and grid[agent_pos[0]][agent_pos[1] - 1] != 1:
                agent_pos[1] -= 1
            elif prev_direction == "RIGHT" and agent_pos[1] < GRID_WIDTH - 1 and grid[agent_pos[0]][agent_pos[1] + 1] != 1:
                agent_pos[1] += 1

            if grid[agent_pos[0]][agent_pos[1]] == 2:  # agent is on mud
                mud_slowdown = 3

            # Call the pathfinding_direction function from pathfinding_agent.py
            prev_direction, path = pathfinding_direction(tuple(agent_pos), tuple(target_pos), tuple(enemy_pos), visible_grid)

    # Enemy movement
    if sim_iter % 4 == 0:
        if enemy_mud_slowdown > 0:
            enemy_mud_slowdown -= 1
        else:
            enemy_agent_direction = [agent_pos[0] - enemy_pos[0], agent_pos[1] - enemy_pos[1]]
            if abs(enemy_agent_direction[0]) > abs(enemy_agent_direction[1]):
                enemy_agent_direction[0] = 1 if enemy_agent_direction[0] > 0 else -1
                enemy_agent_direction[1] = 0
            else:
                enemy_agent_direction[1] = 1 if enemy_agent_direction[1] > 0 else -1
                enemy_agent_direction[0] = 0
            next_enemy_pos = [enemy_pos[0] + enemy_agent_direction[0], enemy_pos[1] + enemy_agent_direction[1]]
            if 0 <= next_enemy_pos[0] < GRID_HEIGHT\
            and 0 <= next_enemy_pos[1] < GRID_WIDTH\
            and grid[next_enemy_pos[0]][next_enemy_pos[1]] != 1:
                enemy_pos = next_enemy_pos

            if grid[enemy_pos[0]][enemy_pos[1]] == 2:  # enemy is on mud
                enemy_mud_slowdown = 3

            if agent_pos == enemy_pos:
                print("Enemy got you!")
                pygame.quit()
                sys.exit()


    # Draw background
    screen.fill(UNKNOWN_COLOR)

    # Draw the grid (mud)
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if visible_grid[row][col] == 2:
                pygame.draw.rect(screen, MUD_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the grid
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if visible_grid[row][col] == 1:
                pygame.draw.rect(screen, OBSTACLE_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif visible_grid[row][col] == 0:
                pygame.draw.rect(screen, FLOOR_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the target
    pygame.draw.rect(screen, TARGET_COLOR, (target_pos[1] * GRID_SIZE, target_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the enemy
    pygame.draw.rect(screen, ENEMY_COLOR, (enemy_pos[1] * GRID_SIZE, enemy_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the agent
    pygame.draw.rect(screen, AGENT_COLOR, (agent_pos[1] * GRID_SIZE, agent_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the path nodes
    for node in path[1:]:
        pygame.draw.circle(screen, TARGET_COLOR, (node[1] * GRID_SIZE + GRID_SIZE/2, node[0] * GRID_SIZE + GRID_SIZE/2), GRID_SIZE/8)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(24)

    sim_iter += 1