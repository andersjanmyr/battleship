
def create_board(width, height):
    board =  [ [ '-' for i in range(width) ] for j in range(height) ]
    return board

def to_string(board):
    return "   %(header)s\n%(rows)s\n" % \
        { "header": top_header(10),
         "rows": rows_with_num(board) }

def top_header(width):
    start = ord('A')
    header = [ chr(i) for i in range(start, start + width) ]
    return " ".join(header)

def rows_with_num(board):
     return "\n".join([ row_with_num(i, row) for i, row in enumerate(board) ])

def row_with_num(i, row):
    return "%(i)2d %(row)s" % { "i": i+1, "row": " ".join(row) }

def print_board(board):
    print(to_string(board))

def main():
    board = create_board(10, 10)
    print_board(board)


if __name__ == "__main__":
    main()

