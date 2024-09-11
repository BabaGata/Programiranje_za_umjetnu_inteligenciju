import random
import time
from agent import agent_decision


def display(grid, agent_coord=(-1,-1)):
    print("\n\n")
    print("\n---------------------")
    for y, row in enumerate(grid):
        print("|", end="")
        for x, tile in enumerate(row):
            if (y, x) == agent_coord:
                tile += "A"
            tile += " " * (4 - len(tile))
            print(tile + "|", end="")
        print("\n---------------------")


#### WORLD STATE INIT ####

world_state = [["A", "", "", ""],
               ["", "", "", ""],
               ["", "", "", ""],
               ["", "", "", ""]]

def init_world_state():
    # pits
    pits_coords = []
    for y in range(3):
        for x in range(3):
            if (y == 0 and x == 0) or (y == 0 and x == 1) or (y == 1 and x == 0): continue
            if random.random() <= 0.2:
                pits_coords.append((y, x))
                world_state[y][x] = "P"
    # breeze
    for y, x in pits_coords:
        for coords_neigh in [(y,x-1), (y,x+1), (y-1,x), (y+1,x)]:
            if coords_neigh[0] < 0 or coords_neigh[0] > 3: continue
            if coords_neigh[1] < 0 or coords_neigh[1] > 3: continue
            if "P" in world_state[coords_neigh[0]][coords_neigh[1]] or "B" in world_state[coords_neigh[0]][coords_neigh[1]]: continue
            world_state[coords_neigh[0]][coords_neigh[1]] += "B"
        
    # wumpus
    y, x = random.randint(0,3), random.randint(0,3)
    while (y,x) == (0,0) or (y,x) == (0,1) or (y,x) == (1,0) or "P" in world_state[y][x]:
        y, x = random.randint(0,3), random.randint(0,3)
    world_state[y][x] += "W"
    wumpus_coord = (y, x)
    # stench
    for coords_neigh in [(wumpus_coord[0],wumpus_coord[1]-1), (wumpus_coord[0],wumpus_coord[1]+1), (wumpus_coord[0]-1,wumpus_coord[1]), (wumpus_coord[0]+1,wumpus_coord[1])]:
        if coords_neigh[0] < 0 or coords_neigh[0] > 3: continue
        if coords_neigh[1] < 0 or coords_neigh[1] > 3: continue
        if "P" in world_state[coords_neigh[0]][coords_neigh[1]]: continue
        world_state[coords_neigh[0]][coords_neigh[1]] += "S"
    
    # gold
    y, x = random.randint(0,3), random.randint(0,3)
    while (y,x) == (0,0) or "P" in world_state[y][x] or "W" in world_state[y][x]:
        y, x = random.randint(0,3), random.randint(0,3)
    world_state[y][x] += "G"

init_world_state()


#### AGENT ####

knowl_base = [["", "", "", ""],
              ["", "", "", ""],
              ["", "", "", ""],
              ["", "", "", ""]]

def agent_state(tile):
    global agent_has_gold
    if "P" in tile:
        print("Fell into a pit!")
        return False
    if "W" in tile:
        print("Eaten by a wumpus!")
        return False
    if "G" in tile:
        print("Found gold!")
        agent_has_gold = True
    if agent_coord == (0, 0) and agent_has_gold:
        print("Escaped the cave with gold!")
        return False
    return True

agent_coord = (0, 0)
agent_has_gold = False
def move_agent(agent_coord, direction=(0,0)):
    new_agent_coord = agent_coord
    new_agent_coord = (new_agent_coord[0] + direction[0], new_agent_coord[1] + direction[1])

    if new_agent_coord[0] < 0 or new_agent_coord[0] > 3 or\
        new_agent_coord[1] < 0 or new_agent_coord[1] > 3:
        print("Bumped into a wall!")
        return agent_coord
    
    world_state[agent_coord[0]][agent_coord[1]] = world_state[agent_coord[0]][agent_coord[1]].replace("A", "")
    world_state[new_agent_coord[0]][new_agent_coord[1]] += "A"
    return new_agent_coord


#### MAIN LOOP ####

running = True
while True:
    tile = world_state[agent_coord[0]][agent_coord[1]].replace("A", "")
    knowl_base[agent_coord[0]][agent_coord[1]] = tile
    display(world_state)
    #display(knowl_base, agent_coord)
    print("Tile content:", tile)
    running = agent_state(tile)
    if not running: break
    if agent_has_gold:
        world_state[agent_coord[0]][agent_coord[1]] = world_state[agent_coord[0]][agent_coord[1]].replace("G", "")
        knowl_base[agent_coord[0]][agent_coord[1]] = knowl_base[agent_coord[0]][agent_coord[1]].replace("G", "")
    move_direction = agent_decision(agent_coord, tile, knowl_base)
    agent_coord = move_agent(agent_coord, move_direction)
    time.sleep(1)