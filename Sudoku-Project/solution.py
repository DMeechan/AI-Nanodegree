### 
# Configure these values:
USING_DIAGONALS = True
DEBUG = False
###

assignments = []

ALL_DIGITS = '123456789'

ROWS = 'ABCDEFGHI'
COLS = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

BOXES = cross(ROWS, COLS)

ROW_UNITS = [cross(r, COLS) for r in ROWS]
COL_UNITS = [cross(ROWS, c) for c in COLS]
SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
DIAG_UNITS = [[r+c for r,c in zip(ROWS,COLS)], [r+c for r,c in zip(ROWS,COLS[::-1])]]
# DIAG_UNITS = crossDiagonal(rows)

unitlist = []

units = []
peers = []

DICT_ROW_UNITS = dict((s, [u for u in ROW_UNITS if s in u]) for s in BOXES)
ROW_PEERS = dict((s, set(sum(DICT_ROW_UNITS[s], [])) - set([s])) for s in BOXES)

DICT_COL_UNITS = dict((s, [u for u in COL_UNITS if s in u]) for s in BOXES)
COL_PEERS = dict((s, set(sum(DICT_COL_UNITS[s], [])) - set([s])) for s in BOXES)

DICT_SQUARE_UNITS = dict((s, [u for u in SQUARE_UNITS if s in u]) for s in BOXES)
SQUARE_PEERS = dict((s, set(sum(DICT_SQUARE_UNITS[s], [])) - set([s])) for s in BOXES)

def use_diagonals(shouldUseDiagonals):
    global unitlist, units, peers, USING_DIAGONALS

    USING_DIAGONALS = shouldUseDiagonals

    unitlist = ROW_UNITS + COL_UNITS + SQUARE_UNITS

    if shouldUseDiagonals:
         unitlist += DIAG_UNITS

    units = dict((s, [u for u in unitlist if s in u]) for s in BOXES)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in BOXES)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # If a value is 2 chars long, look for a matching pair
    # Because it may be part of a naked twins pattern
    # So that pair can be removed from their unit's peers
    possible_pairs = [box for box in values.keys() if len(values[box]) == 2]      

    # Go through every box containing 2 values
    for pair in possible_pairs:

        # Go through unitTypes 0, 1, 2 to check units for: rows, columns, and squares
        for unitType in range(3):
            pair_value = values[pair]

            # Check that the box's corresponding pair hasn't already been processed; since their peers are the same (efficiency)
            # if pair_value not in seen:

            # Check that only 2 boxes in the same unit share the same values
            if len([box for box in getUnitPeersOfBox(unitType, pair) if values[box] == pair_value]) == 1:

                # Get all eligible peers of the pair
                pair_unit_peers = [peer for peer in getUnitPeersOfBox(unitType, pair) if len(values[peer]) >= 2]

                # Iterate through all peers and remove the digits found in the pair
                for peer in pair_unit_peers:
                    peer_value = values[peer]
                    # print('Peer ' + peer + ' value before: ' + peer_value + ' for pair ' + pair_value)

                    # Prevent it from deleting the pair's corresponding pair
                    if peer_value != pair_value:
                        for char in pair_value:
                            peer_value = peer_value.replace(char, '')

                        # Check if the value has changed before appending
                        if peer_value != values[peer]:
                            assign_value(values, peer, peer_value)   

                    # print('Peer ' + peer + ' value after: ' + peer_value)
    return values

def getUnitPeersOfBox(unitType, box):
    if unitType == 0:
        # Use row unit
        return ROW_PEERS[box]

    elif unitType == 1:
        # Use column unit
        return COL_PEERS[box]

    elif unitType == 2:
        # use square unit
        return SQUARE_PEERS[box]

    else:
        # Invalid input
        print("Error: unitType: " + unitType +
              " is invalid. Please use value between 0 and 2.")
        return []

def grid_values(grid):
    if (len(grid) == 81):
        values = []
        for letter in grid:
            if letter == '.':
                values.append(ALL_DIGITS)
            elif letter == 'X':
                values.append('2379')
            elif letter == 'Y':
                values.append('379')
            elif letter == 'Z':
                values.append('23')
            else:
                values.append(letter)

        assert (len(values) == 81)
        zippedOutput = zip(BOXES, values)
        grid = dict(zippedOutput)

    return grid

def grid_values(grid):
    if (len(grid) == 81):
        values = []
        for letter in grid:
            if letter == '.':
                values.append(ALL_DIGITS)
            elif letter == 'X':
                values.append('2379')
            elif letter == 'Y':
                values.append('379')
            elif letter == 'Z':
                values.append('23')
            else:
                values.append(letter)

        assert (len(values) == 81)
        zippedOutput = zip(BOXES, values)
        grid = dict(zippedOutput)

    return grid

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # If value is only 1 char long, then it's filled, so we can remove it
    # from its peers
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes already have a set value
        stored_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Run through eliminate, only choice, and naked twins
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value (to compare to original)
        stored_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # If no new values added; stop
        stalled = stored_values_before == stored_values_after

        # Check if it's even possible: check for boxes with 0 available values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in BOXES): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in BOXES if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    global USING_DIAGONALS
    use_diagonals(USING_DIAGONALS)
    values = grid_values(grid)
    values = search(values)
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    global BOXES, ROWS, COLS
    width = 1+max(len(values[s]) for s in BOXES)
    line = '+'.join(['-'*(width*3)]*3)
    for r in ROWS:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF': print(line)
    return

def runTests():
    input1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    input2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    input3 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    input4 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    # Input which has a twins in it
    input5 = '1.4.9..68956.18.34..84.695151X....868.Y6...1264Z.8..97781923645495.6.823.6Z854179'

    input6 = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'

    input_grid = eval("{\"G7\": \"2345678\", \"G6\": \"1236789\", \"G5\": \"23456789\", \"G4\": \"345678\", \"G3\": \"1234569\", \"G2\": \"12345678\", \"G1\": \"23456789\", \"G9\": \"24578\", \"G8\": \"345678\", \"C9\": \"124578\", \"C8\": \"3456789\", \"C3\": \"1234569\", \"C2\": \"1234568\", \"C1\": \"2345689\", \"C7\": \"2345678\", \"C6\": \"236789\", \"C5\": \"23456789\", \"C4\": \"345678\", \"E5\": \"678\", \"E4\": \"2\", \"F1\": \"1\", \"F2\": \"24\", \"F3\": \"24\", \"F4\": \"9\", \"F5\": \"37\", \"F6\": \"37\", \"F7\": \"58\", \"F8\": \"58\", \"F9\": \"6\", \"B4\": \"345678\", \"B5\": \"23456789\", \"B6\": \"236789\", \"B7\": \"2345678\", \"B1\": \"2345689\", \"B2\": \"1234568\", \"B3\": \"1234569\", \"B8\": \"3456789\", \"B9\": \"124578\", \"I9\": \"9\", \"I8\": \"345678\", \"I1\": \"2345678\", \"I3\": \"23456\", \"I2\": \"2345678\", \"I5\": \"2345678\", \"I4\": \"345678\", \"I7\": \"1\", \"I6\": \"23678\", \"A1\": \"2345689\", \"A3\": \"7\", \"A2\": \"234568\", \"E9\": \"3\", \"A4\": \"34568\", \"A7\": \"234568\", \"A6\": \"23689\", \"A9\": \"2458\", \"A8\": \"345689\", \"E7\": \"9\", \"E6\": \"4\", \"E1\": \"567\", \"E3\": \"56\", \"E2\": \"567\", \"E8\": \"1\", \"A5\": \"1\", \"H8\": \"345678\", \"H9\": \"24578\", \"H2\": \"12345678\", \"H3\": \"1234569\", \"H1\": \"23456789\", \"H6\": \"1236789\", \"H7\": \"2345678\", \"H4\": \"345678\", \"H5\": \"23456789\", \"D8\": \"2\", \"D9\": \"47\", \"D6\": \"5\", \"D7\": \"47\", \"D4\": \"1\", \"D5\": \"36\", \"D2\": \"9\", \"D3\": \"8\", \"D1\": \"36\"}")

    input_value = input6

    solved = solve(input_value)
    if solved:
        display(solved)
    else:
        print(solved)

def run():
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

if __name__ == '__main__':
    if DEBUG:
        runTests()
    else:
        run()