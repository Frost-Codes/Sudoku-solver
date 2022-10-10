from itertools import zip_longest, chain

rows = 'ABCDEFGHI'
cols = '123456789'
digits = cols


def cross_product(a, b):
    return [c + d for c in a for d in b]


def chunk(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


allSquares = cross_product(rows, cols)
possibleRows = [cross_product(r, cols) for r in rows]
possibleCols = [cross_product(rows, c) for c in cols]
blocks = [cross_product(rs, cl) for rs in chunk(rows, 3) for cl in chunk(cols, 3)]

allUnits = possibleCols + possibleRows + blocks  # all rows cols and blocks

# dict with each square as key and a list of row, col and block in which it belong as value
units = dict((square, [unit for unit in allUnits if square in unit]) for square in allSquares)

# dict with each square as key and set of peers (col, row and block in which square is in) as values
peers = dict((square, set(chain(*units[square])) - {square}) for square in allSquares)


def eliminate(grid, square, digit):
    """
    Eliminate digit from grid[square] and propagate when candidates <=2
    :param grid:
    :param square:
    :param digit:
    :return grid or False otherwise:
    """
    if digit not in grid[square]:  # already eliminated
        return grid
    grid[square] = grid[square].replace(digit, '')
    # if len of square is reduced to one remove that value from peers
    if len(grid[square]) == 0:
        return False  # wrong solution
    elif len(grid[square]) == 1:
        value = grid[square]
        if not all(eliminate(grid, peer, value) for peer in peers[square]):  # Eliminating from peers
            return False
    # if a unit is reduced to one place for a value, put it there
    for unit in units[square]:
        places = [sqr for sqr in unit if digit in grid[sqr]]
        if len(places) == 0:
            return False  # No place for this digit
        elif len(places) == 1:  # Assign the digit there
            if not place(grid, places[0], digit):
                return False
    return grid


def place(grid, square, digit):
    """
    Eliminate all other values except digit from grid[square] and propagate
    :param grid:
    :param square:
    :param digit:
    :return grid or False otherwise:
    """
    other_values = grid[square].replace(digit, '')
    if all(eliminate(grid, square, value) for value in other_values):
        return grid
    return False


def search(grid):
    """
    Check if grid is empty or solved
    else: check square with min amount of possible candidates and try placing them. if only one candidate in
            square a value is already placed there
    :param grid:
    :return result of searching:
    """
    if not grid:
        return False
    if all(len(grid[square]) == 1 for square in allSquares):  # solved
        return grid
    values, square = min((len(grid[square]), square) for square in allSquares if len(grid[square]) > 1)
    for digit in grid[square]:
        result = search(place(grid.copy(), square, digit))
        if result:
            return result


def parse_puzzle(puzzle):
    """
    Places values of the puzzle in the grid to corresponding squares, other squares will be initialized with
        possible values
    :param puzzle:
    :return initialized grid(puzzle):
    """
    assert set(puzzle) <= set('.0123456789')
    assert len(puzzle) == 81

    # Initialize the grid as a dictionary with key as square and values as all possible candidates
    grid = dict((square, digits) for square in allSquares)
    for square, digit in zip(allSquares, puzzle):
        if digit in digits and not place(grid, square, digit):
            return False
    return grid


def solve_puzzle(puzzle):
    """
    solves the puzzle
    :param puzzle:
    :return solved puzzle:
    """
    grid = parse_puzzle(puzzle)
    return search(grid)



