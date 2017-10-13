def get_legal_moves(self):
    """ Return a list of all legal moves available to the
    active player.  Each player should get a list of all
    empty spaces on the board on their first move, and
    otherwise they should get a list of all open spaces
    in a straight line along any row, column or diagonal
    from their current position. (Players CANNOT move
    through obstacles or blocked squares.) Moves should
    be a pair of integers in (column, row) order specifying
    the zero-indexed coordinates on the board.
    """
    global COLUMNS, ROWS

    self.get_legal_moves_fast()

    print('valid locations output:')
    print()

    empty_positions = [cell.get_coordinates()
                        for cell in self.cells if cell.value == 0]
    # emptyPositions = [cell for col in board for cell in col if cell == 0]

    # If board is empty, it's the player's first move
    # So anywhere is legal
    if is_board_empty(self.cells):
        return empty_positions

    # Otherwise, find player's current position
    valid_locations = []

    # What does this do?
    current_col = self.locations[self.player2_active][0]
    current_row = self.locations[self.player2_active][1]

    # Output which player it's checking valid moves for
    print('# INITIATING MAIDEN VOYAGE TO EXPLORE VALID CELLS, SIR!')
    print("# We'll be searching for valid moves for player: {}, Sir".format(
        str(self.player2_active * 1 + 1)))
    print("# Our journey will start at cell: {} at coordinates ({}, {}), Sir".format(
        coordinates_to_pos((current_col, current_row)), current_col, current_row))

    for direction in (-4, -3):
        search = self.search_for_valid_moves(
            direction, current_col, current_row, COLUMNS, ROWS, True)
        if search:
            for cell in search:
                valid_locations.append(cell)

    print('# Results are back from analysis, Sir. Our maiden voyage found the following valid cells: {}'.format(
        valid_locations))

def search_for_valid_moves(self, direction, current_col, current_row, column_limit, row_limit, is_original_function_call):
    """Check to see if the current cell is empty. 
    If it is, check if it's about to search off the edge of the grid.
    If it's not, then move onto the next cell and call itself"""
    # Direction: -1 = up; 1 = down; 2 = right; -2 is left
    # -3 is top left; 3 is bottom right
    # -4 is bottom left; 4 is top right
    valid_locations = []

    if is_original_function_call:
        print()
        # Skip the validation check for current cell, since we already know the original cell will be filled
    else:
        # Check if the current cell is available
        pos = coordinates_to_pos((current_col, current_row))
        print(
            '# Just arrived on the scene, Sir. Our current cell position is: ' + str(pos))

        current_cell = self.cells[coordinates_to_pos(
            (current_col, current_row))]
        if current_cell.value != 0:
                # Cell is already occupied; jump outta this one, Jack
            print('# Cell already occupied, Sir. Time to abort search in direction: {}'.format(
                direction))
            return

    # Check if this cell is at the end of the grid (example: if at (0, 0) when direction = left)
    end_of_the_line = False
    if (direction == -1 and current_row == 0) or (direction == 1 and current_row == row_limit - 1):
        end_of_the_line = True
    elif (direction == -2 and current_col == 0) or (direction == 2 and current_col == column_limit - 1):
        end_of_the_line = True
    elif (direction == -3 and current_col == 0) or (direction == -3 and current_row == 0):
        end_of_the_line = True
    elif (direction == 3 and current_row == row_limit - 1) or (direction == 3 and current_col == column_limit - 1):
        end_of_the_line = True
    elif (direction == -4 and current_row == row_limit - 1) or (direction == -4 and current_col == 0):
        end_of_the_line = True
    elif (direction == 4 and current_row == 0) or (direction == 4 and current_col == column_limit - 1):
        end_of_the_line = True 

    # If searching and reached the end (top, bottom, far left or far right), then return
    if end_of_the_line:
        print('# End of the line, Sir. No more searching left in direction: {}'.format(
            direction))
        if is_original_function_call:
            return
        else:
            current_position = (current_col, current_row)
            valid_locations.append(current_position)
            return valid_locations

    print('# Still in the game, Sir. Searching the next cell in direction: {}'.format(
        direction))

    # Check if increment is +1 or -1 (dependig on whether it's doing positive or negative traversal)
    incrementer = 0
    if direction > 0:
        incrementer = 1
    elif direction < 0:
        incrementer = -1

    # Add current position to valid locations, as long as it isn't the original cell, haha
    if not is_original_function_call:
        current_position = (current_col, current_row)
        valid_locations.append(current_position)

    # Increment to the next cell
    if direction in {-1, 1}:
        # Direction = vertical
        current_row += incrementer

    elif direction in {-2, 2}:
        # Direction = horizontal
        current_col += incrementer

    elif direction in {-3, 3}:
        current_row += incrementer
        current_col += incrementer

    elif direction in {4, -4}:
        current_col += incrementer
        current_row -= incrementer

    # Search the next cell and add it to valid locations if it's valid
    search_next_cell = self.search_for_valid_moves(
        direction, current_col, current_row, column_limit, row_limit, False)
    print('Just got word back from the next cell, Sir. They have found the following cells available: {}'.format(
        search_next_cell))
    if search_next_cell:
        for cell in search_next_cell:
            valid_locations.append(cell)

    return valid_locations

