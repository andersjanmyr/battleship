import random
import sys

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['~' for i in range(width)] for j in range(height)]

    def __str__(self):
        return "   %s\n%s" % (self.top_header(), self.rows_with_num())

    def top_header(self):
        start = ord('A')
        header = [chr(i) for i in range(start, start + self.width)]
        return " ".join(header)

    def rows_with_num(self):
         return "\n".join([self.row_with_num(i, row) for i, row in enumerate(self.board)])

    def row_with_num(self, i, row):
        return "%2d %s" % (i+1, " ".join(row))

    def get(self, coord):
        (x, y) = coord
        row = self.board[y]
        return row[x]

    def set(self, coord, i):
        (x, y) = coord
        self.board[y][x] = i

    def in_bounds(self, coord):
        (x, y) = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def match_count(self, c):
        is_match = lambda i: i == c
        matches = filter(is_match, [i for row in self.board for i in row])
        return len(list(matches))


X_INDEX="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def main():
    try:
        (width, height, ships) = parse_args(sys.argv)
    except ValueError as err:
        print(err)
        usage()
        exit(1)

    solution_board = Board(width, height)
    place_ships(solution_board, ships)
    # print(solution_board)
    game_board = Board(width, height)
    game_loop(solution_board, game_board)

def parse_args(args):
    width = 10 if len(args) < 2 else int(args[1])
    height = 10 if len(args) < 3 else int(args[2])
    if width > len(X_INDEX):
        raise ValueError("Max width is: %d" % len(X_INDEX))
    if height > 50:
        raise ValueError("Max height is: %d" % 50)
    if len(sys.argv) < 4:
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    else:
        try:
            ships = list(map(lambda s: int(s), args[3:]))
            to_large = filter(lambda s: s >= min(width, height), ships)

        except:
            raise ValueError("Ships must be numeric values: '%s'" % " ".join(args[3:]))
        if len(list(to_large)) > 0:
            raise ValueError("Ships must be smaller than board (%d, %d): '%s'" % (width, height, " ".join(args[3:])))

    return (width, height, ships)

def usage():
    print("Usage: python main.py [width] [height] [ships]")
    print("Example: python main.py 15 10 7 6 5 1 1 1")

def place_ships(board, ships):
    for ship in ships:
        place_ship(board, ship)

def place_ship(board, ship):
    coords = random_coords(board, ship)
    while not valid_coords(board, coords):
        coords = random_coords(board, ship)
    update_board(board, coords)

def random_coords(board, ship):
    h = board.height
    w = board.width
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
    in_bounds = lambda c: board.in_bounds(c)
    possible = filter(in_bounds, coords)
    invalid = filter(lambda c: board.get(c) == ':', possible)
    return len(list(invalid)) == 0

def update_board(board, coords):
    for c in coords:
        board.set(c, ':')

def game_loop(solution_board, game_board):
    guesses = 0
    ship_parts = solution_board.match_count(':')
    while not game_over(game_board, ship_parts):
        print(game_board)
        print("Guesses: %d" % guesses)
        print("")
        pos = wait_for_input(game_board.width, game_board.height)
        guesses += 1
        c = pos_to_coord(pos)
        if solution_board.get(c) == ':':
            game_board.set(c, 'x')
        else:
            game_board.set(c, 'o')
    print(game_board)
    print("Board solved in %d guesses." % guesses)

def game_over(game_board, ship_parts):
    return game_board.match_count('x') == ship_parts


def wait_for_input(width, height):
    val = input("Guess: ")
    while not input_valid(val, width, height):
        max_x = X_INDEX[width-1]
        max_y = height
        print("Invalid input '%s', valid format: A1-%s%d" % (val, max_x, max_y))
        val = input("Guess: ")
    return val

def input_valid(val, width, height):
    if len(val) < 2:
        return False
    if not val[0].upper() in X_INDEX[:width]:
        return False
    i = int(val[1:])
    return i >= 1 and i <= height


def pos_to_coord(pos):
    x = X_INDEX.index(pos[0].upper())
    y = int(pos[1:])-1
    return (x, y)

if __name__ == "__main__":
    main()

