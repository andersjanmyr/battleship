import random

def main():
    board_with_ships = create_board(10, 10)
    place_ships(board_with_ships, [4, 3, 3, 2, 2, 2, 1, 1, 1, 1])
    game_board = create_board(10, 10)
    game_loop(board_with_ships, game_board)

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

def game_loop(board_with_ships, game_board):
    guesses = 0
    ship_parts = count_in_board(board_with_ships, ':')
    while not game_over(game_board, ship_parts):
        print("Guesses: %d" % guesses)
        print(board_to_string(game_board))
        pos = wait_for_input()
        guesses += 1
        (x, y) = pos_to_coord(pos)
        if board_with_ships[y][x] == ':':
            game_board[y][x] = 'x'
        else:
            game_board[y][x] = 'o'

def count_in_board(board, c):
    is_match = lambda i: i == c
    hits = filter(is_match, [i for row in board for i in row])
    return len(list(hits))

def game_over(game_board, ship_parts):
    return count_in_board(game_board, 'x') == ship_parts


def wait_for_input():
    val = input("Guess: ")
    while not input_valid(val):
        print("Invalid input '%s', valid format: A1-J10" % val)
        val = input("Guess: ")
    return val

def input_valid(val):
    if len(val) < 2:
        return False
    if not val[0].upper() in "ABCDEFGHIJ":
        return False
    i = int(val[1:])
    return i >= 1 and i <= 10


def pos_to_coord(pos):
    x = "ABCDEFGHIJ".index(pos[0].upper())
    y = int(pos[1:])-1
    return (x, y)

if __name__ == "__main__":
    main()

