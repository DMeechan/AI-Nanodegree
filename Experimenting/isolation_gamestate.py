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
        move_col, move_row = move

        target_cell = coordinates_to_pos(move)

        # Check if cell isn't taken
        if self.cells[target_cell].value == 0:
            new_game_state = copy.deepcopy(self)
            current_player_num = new_game_state.player2_active

            # Move self (player 1) into the new position
            new_game_state.cells[target_cell].value = current_player_num + 1

            new_game_state.locations[current_player_num] = (move_col, move_row)
            new_game_state.player2_active = not new_game_state.player2_active

            return new_game_state

    def is_move_legal(self, col, row):
        global COLUMNS, ROWS
        col_max = COLUMNS - 1
        row_max = ROWS - 1

        if 0 <= col <= col_max and 0 <= row <= row_max:
            current_cell = self.cells[coordinates_to_pos((col, row))]
            if current_cell.value == 0:
                return True
        return False

    def get_legal_moves(self):
        print('# Initiating traversal with upgraded algorithm, Sir!')
        current_col, current_row = self.locations[self.player2_active]
        print('# Our current position is: (' + str(current_col) + ', ' + str(current_row) + ')')

        # If board is empty, it's the player's first move
        # So anywhere is legal
        if is_board_empty(self.cells):
            empty_positions = [cell.get_coordinates() for cell in self.cells]
            return empty_positions

        fringe_directions = [(-1, -1), (0, -1), (1, -1),
                             (-1,  0),          (1,  0),
                             (-1,  1), (0,  1), (1,  1)]

        fringe = [((current_col + col_increment, current_row + row_increment), (col_increment, row_increment)) 
                    for col_increment, row_increment in fringe_directions if self.is_move_legal(current_col + col_increment, current_row + row_increment)]

        valid_moves = []

        while fringe:
            move, direction = fringe.pop()
            col, row = move
            col_dir, row_dir = direction

            valid_moves.append((col, row))

            next_col = col + col_dir
            next_row = row + row_dir

            if self.is_move_legal(next_col, next_row):
                next_move = (next_col, next_row)
                fringe.append((next_move, direction))

        print('# Results are back from analysis, Sir. Our maiden voyage found the following valid cells: {}'.format(valid_moves))
        return valid_moves

    def set_players_temp_positions(self):
        self.locations[0] = (2, 0)
        self.locations[1] = (1, 0)

        self.cells[coordinates_to_pos(self.locations[0])].value = 1
        self.cells[coordinates_to_pos(self.locations[1])].value = 2

        print('Current (temp) positions:')
        display(self.cells)


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
