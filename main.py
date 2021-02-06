import random

def main():
    board = create_board(10, 10)
    print(board_to_string(board))
    place_ships(board, [4, 3, 3, 2, 2, 2, 1, 1, 1, 1])
    print(board_to_string(board))

def create_board(width, height):
    board =  [['-' for i in range(width)] for j in range(height)]
    return board

def board_to_string(board):
    width = len(board[0])
    return "   %s\n%s\n" % (top_header(width), rows_with_num(board))

def top_header(width):
    start = ord('A')
    header = [chr(i) for i in range(start, start + width)]
    return " ".join(header)

def rows_with_num(board):
     return "\n".join([row_with_num(i, row) for i, row in enumerate(board)])

def row_with_num(i, row):
    return "%2d %s" % (i+1, " ".join(row))

def place_ships(board, ships):
    for ship in ships:
        place_ship(board, ship)

def place_ship(board, ship):
    coords = random_coords(board, ship)
    while not valid_coords(board, coords):
        coords = random_coords(board, ship)
    update_board(board, coords)

def random_coords(board, ship):
    h = len(board)
    w = len(board[0])
    dir = random.randint(0, 1)
    if dir == 0:
        w -= ship
    else:
        h -= ship
    x = random.randint(0, w-1)
    y = random.randint(0, h-1)
    if dir == 0:
        return [(i, y) for i in range(x, x+ship)]
    else:
        return [(x, i) for i in range(y, y+ship)]

def valid_coords(board, coords):
    for c in coords:
        if not valid_coord(board, c):
            return False
    return True

def valid_coord(board, coord):
    (x, y) = coord
    coords = [(x-1,y), (x,y), (x+1,y), (x,y-1), (x,y+1)]
    in_bounds = lambda c: on_board(board, c)
    possible = filter(in_bounds, coords)
    invalid = filter(lambda c: board[c[1]][c[0]] == ':', possible)
    return len(list(invalid)) == 0

def on_board(board, coord):
    (x, y) = coord
    return x >= 0 and x < len(board[0]) and y >=0 and y < len(board)

def update_board(board, coords):
    for (x, y) in coords:
        board[y][x] = ':'

if __name__ == "__main__":
    main()

