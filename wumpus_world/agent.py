import sys

memory = {
    "time": 0,
    "prev_position": (0,0),
    "path": []
}

def get_moves(x, y):
    moves = []
    if x != 0:
        moves.append((-1, 0))
    if x != 3:
        moves.append((1, 0))
    if y != 0:
        moves.append((0, -1))
    if y != 3:
        moves.append((0, 1))
    return moves
def not_safe(x, y, knowl_base, tile):
    if x != 0:
        if knowl_base[x - 1][y] == '':
            knowl_base[x - 1][y] = 'N' + tile
        elif 'N' in knowl_base[x - 1][y]:
            knowl_base[x - 1][y] = knowl_base[x - 1][y] + tile
    if x != 3:
        if knowl_base[x + 1][y] == '':
            knowl_base[x + 1][y] = 'N' + tile
        elif 'N' in knowl_base[x + 1][y]:
            knowl_base[x + 1][y] = knowl_base[x + 1][y] + tile
    if y != 0:
        if knowl_base[x][y - 1] == '':
            knowl_base[x][y - 1] = 'N' + tile
        elif 'N' in knowl_base[x][y - 1]:
            knowl_base[x][y - 1] = knowl_base[x][y - 1] + tile
    if y != 3:
        if knowl_base[x][y + 1] == '':
            knowl_base[x][y + 1] = 'N' + tile
        elif 'N' in knowl_base[x][y + 1]:
            knowl_base[x][y + 1] = knowl_base[x][y + 1] + tile
def is_safe(x, y, knowl_base, tile):
    if x != 0:
        if knowl_base[x - 1][y] != '' and tile not in knowl_base[x - 1][y]:
            return True
    if x != 3:
        if knowl_base[x + 1][y] != '' and tile not in knowl_base[x + 1][y]:
            return True
    if y != 0:
        if knowl_base[x][y - 1] != '' and tile not in knowl_base[x][y - 1]:
            return True
    if y != 3:
        if knowl_base[x][y + 1] != '' and tile not in knowl_base[x][y + 1]:
            return True
    return False
def get_score(tile):
    if tile == '':
        return 1
    if tile == 'I':
        return 10
    elif 'N' in tile:
        return -10
    elif tile == 'C' or 'S' in tile or 'B' in tile:
        return -1
def has_gold(knowl_base):
    for i in range(4):
        for j in range(4):
            if 'G' in knowl_base[i][j]:
                print('Has gold')
                return True
    return False
def get_best_move(coord, tile, knowl_base):
    gold = has_gold(knowl_base)
    if gold:
        next_position = memory["path"][-1]
        best_move = (next_position[0] - coord[0], next_position[1] - coord[1])
        memory["path"].pop()

    else:
        x0 = coord[0]
        y0 = coord[1]

        if 'B' in tile:
            not_safe(x0, y0, knowl_base, 'B')

        if 'S' in tile:
            not_safe(x0, y0, knowl_base, 'S')

        moves = get_moves(x0, y0)

        score = float('-inf')
        best_move = coord

        for move in moves:
            x1 = coord[0] + move[0]
            y1 = coord[1] + move[1]
            if 'N' in knowl_base[x1][y1]:
                if 'B' in knowl_base[x1][y1] and is_safe(x1, y1, knowl_base, 'B'):
                    knowl_base[x1][y1] = knowl_base[x1][y1].replace('B', '')

                if 'S' in knowl_base[x1][y1] and is_safe(x1, y1, knowl_base, 'S'):
                    knowl_base[x1][y1] = knowl_base[x1][y1].replace('S', '')

                if knowl_base[x1][y1] == 'N':
                    knowl_base[x1][y1] = 'I'

            move_score = get_score(knowl_base[x1][y1])
            if move_score > score:
                score = move_score
                best_move = move

    return best_move, gold

def agent_decision(coord, tile, knowl_base):
    global memory
    memory["time"] += 1
    knowl_base[coord[0]][coord[1]] = 'C' if tile == '' or tile == 'I' else tile
    print(knowl_base)

    best_move, has_gold = get_best_move(coord, tile, knowl_base)
    print(best_move)

    # wasd movement (for testing)
    # key = input(":")
    # direction = {"a": (0,-1), "d": (0,1), "w": (-1,0), "s": (1,0)}[key]

    direction = best_move

    memory["prev_position"] = coord
    if not has_gold:
        memory["path"].append(coord)

    mp = memory["path"]
    if len(mp) > 4:
        if mp[-1] == mp[-3] and mp[-1] == mp[-5] and mp[-2] == mp[-4]:
            print("Nema sigurnih opcija za nastavak!")
            sys.exit(0)

    return direction  # return (0,1) pomakne agenta za jedno mjesto u desno
