
def create_board(width, height):
    board =  [['-' for i in range(width)] for j in range(height)]
    return board

def to_string(board):
    return "   %s\n%s\n" % (top_header(10), rows_with_num(board))

def top_header(width):
    start = ord('A')
    header = [chr(i) for i in range(start, start + width)]
    return " ".join(header)

def rows_with_num(board):
     return "\n".join([row_with_num(i, row) for i, row in enumerate(board)])

def row_with_num(i, row):
    return "%2d %s" % (i+1, " ".join(row))

def print_board(board):
    print(to_string(board))

def main():
    board = create_board(10, 10)
    print_board(board)


if __name__ == "__main__":
    main()

