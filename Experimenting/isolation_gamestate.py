import copy

# Game inputs
COLUMNS = 3
ROWS = 2

# Game logic
# Subtract 1 for array sizes (start from 0)

# columns -=  1
# rows -= 1


class Cell:
    """Store the position and value of a single cell"""

    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.value = 0

    def get_coordinates(self):
        """Return a tuple of the cell's (x, y) position"""
        return (self.col, self.row)

    def get_pos(self):
        return coordinates_to_pos(self.get_coordinates())


class GameState:
    """Store the game state at a single point in time: array of cells, who's turn it is, and where the players are"""

    def __init__(self):
        global COLUMNS, ROWS

        # Empty = 0; Blocked = -1
        # Player 1 = 1; Player 2 = -1

        self.cells = []

        # False = Player 1's turn; True= Player 2's turn
        self.player2_active = False

        # Player 1's location = (0, 0)
        # Player 2's location = (0, 1)
        # Note: currently this doesn't seem to do anything
        self.locations = [(0, 0), (0, 1)]

        # Populate the cells list
        for row in range(ROWS):
            for col in range(COLUMNS):
                # self.grid[col - 1][row - 1] = 0
                cell = Cell(col, row)
                self.cells.append(cell)

        # Block the cell in the bottom left (set it to -1)
        blocked_cell = coordinates_to_pos((COLUMNS - 1, ROWS - 1))
        self.cells[blocked_cell].value = -1

        # TODO: TEMPOORARY
        self.set_players_temp_positions()

        self.get_legal_moves()

        # self.grid = [][]
        # self.grid = [[0 for y in range(rows + 1)] for x in range(columns + 1)]
        # self.grid[columns][rows] = -1

    def forecast_move(self, move):
        """Return a new game state with a move made"""
        move_col = move[0]
        move_row = move[1]

        target_cell = coordinates_to_pos(move)

        # Check if cell isn't taken
        if self.cells[target_cell].value == 0:

            new_game_state = copy.deepcopy(self)

            current_player_num = new_game_state.player2_active

            # Move self (player 1) into the new position

            new_game_state.cells[target_cell].value = current_player_num + 1

            new_game_state.locations[current_player_num] = (move_col, move_row)
            new_game_state.player2_active = not new_game_state.player2_active

            # if self.grid[moveX][moveY] == 0:
            # newGameState.grid[moveX][moveY] = 1

            return new_game_state

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

        for direction in (-4, -3, -2, -1, 1, 2, 3, 4):
            search = self.search_for_valid_moves(
                direction, current_col, current_row, COLUMNS, ROWS, True)
            if search:
                for cell in search:
                    valid_locations.append(cell)

        print('# Results are back from analysis, Sir. Our maiden voyage found the following valid cells: {}'.format(
            valid_locations))

    def set_players_temp_positions(self):
        self.locations[0] = (2, 0)
        self.locations[1] = (1, 0)

        self.cells[coordinates_to_pos(self.locations[0])].value = 1
        self.cells[coordinates_to_pos(self.locations[1])].value = 2

        print('Current (temp) positions:')
        display(self.cells)

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


def display(cells):
    print()
    output = ''
    previous_cell_row = 0

    for cell in cells:
        if previous_cell_row != cell.row:
            output += '\n'
            previous_cell_row = cell.row
        output += str(cell.value) + ' '

    print(output)
    print()

    # for row in range(rows + 1):
    #     rowOutput = ''
    #     for col in range(columns + 1):
    #         output = ('{}  '.format(grid[col][row]))
    #         rowOutput += output
    #     print(rowOutput)


def is_board_empty(board):
    filled_postions = [cell for cell in board if cell.value > 0]
    # filledPositions = [cell for col in board for cell in col if cell > 0]
    if len(filled_postions):
        return False
    return True


def coordinates_to_pos(move):
    # TO FIND INDEX (0 - 5) OF A SQUARE IN GRID USING (X, Y) VALUES (starting from 0)
    # USE: COL + (ROW * TOTAL NUM OF COLUMNS)
    global COLUMNS

    move_col = move[0]
    move_row = move[1]

    target_cell = move_col + (move_row * (COLUMNS))

    return target_cell


GAME = GameState()
