import copy

# Game inputs
COLUMNS = 3
ROWS = 2

# Game logic
# Subtract 1 for array sizes (start from 0)

# columns -=  1
# rows -= 1

class Cell:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.value = 0

    def get_coordinates(self):
        return (self.col, self.row)

class GameState:

    def __init__(self):
        global COLUMNS, ROWS

        # Empty = 0; Blocked = -1
        # Player 1 = 1; Player 2 = -1

        self.cells = []
        # self.grid = [][]

        # True = Player 1's turn; False = Player 2's turn
        self.player2_active = False

        # Player 1's location = (0, 0)
        # Player 2's location = (0, 1)
        self.locations = [(-1, -1), (-1, -1)]

        for row in range(ROWS):
            for col in range(COLUMNS):

                # self.grid[col - 1][row - 1] = 0

                cell = Cell(col, row)
                self.cells.append(cell)

        # self.grid = [[0 for y in range(rows + 1)] for x in range(columns + 1)]

        # self.grid[columns][rows] = -1
        print('CONVERSION:')
        print(coordinates_to_pos((COLUMNS - 1, ROWS - 1)))
        blocked_cell = coordinates_to_pos((COLUMNS - 1, ROWS - 1))
        self.cells[blocked_cell].value = -1

        # self.forecast_move((0, 1))
        display(self.cells)
        self.get_legal_moves()

    def forecast_move(self, move):
        move_col = move[0]
        move_row = move[1]

        # TO FIND INDEX (0 - 5) OF A SQUARE IN GRID
        # USING A PAIR OF COL, ROW VALUES (starting from 0)
        # USE: COL + (ROW * TOTAL NUM OF COLUMNS)

        target_cell = coordinates_to_pos(move)

        # Check if cell isn't taken
        # if self.grid[moveX][moveY] == 0:
        if self.cells[target_cell].value == 0:

            new_game_state = copy.deepcopy(self)

            current_player_num = new_game_state.player2Active

            # Move self (player 1) into the new position
            # newGameState.grid[moveX][moveY] = 1
            new_game_state.cells[target_cell].value = current_player_num + 1            

            new_game_state.locations[current_player_num] = (move_col, move_row)
            new_game_state.player2Active = not new_game_state.player2Active

            return new_game_state

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
    def get_legal_moves(self):
        # TODO: TEMPOORARY
        self.set_players_temp_positions()

        empty_positions = [cell.getCoordinates() for cell in self.cells if cell.value == 0]
        # emptyPositions = [cell for col in board for cell in col if cell == 0]

        # If board is empty, it's the player's first move
        # So anywhere is legal
        if is_board_empty(self.cells):
            return empty_positions

        # Otherwise, find player's current position
        
        valid_locations = []

        vertical_cells = self.get_valid_cells_verticle(self.locations, False)

        valid_locations.append(vertical_cells)
        
        print('validLocations')
        print(valid_locations)

    def set_players_temp_positions(self):
        self.locations[0] = (0, 1)
        self.locations[1] = (1, 0)

        self.cells[coordinates_to_pos(self.locations[0])].value = 1
        self.cells[coordinates_to_pos(self.locations[1])].value = 2

        display(self.cells)

    def get_valid_cells_verticle(self, locations, searchUpwards):
        global ROWS

        current_col = locations[0][0]
        current_row = locations[0][1]

        valid_locations = []

        def traverse():
            valid_locations.append((current_col, current_row))
            current_cell = self.cells[coordinates_to_pos((current_col, current_row))]

        # Find potential routes above / below the square
        if searchUpwards:
            if current_row == 0:
                return []

            current_row -= 1

        else:
            if current_row == ROWS - 1:
                print('Nope, time to return')
                return []

            current_row += 1 
        
        # Use ((double brackets)) because it's embedding the coordinates in a tuple
        current_cell = self.cells[coordinates_to_pos((current_col, current_row))]

        if searchUpwards:
            while current_row > -1 and current_cell.value == 0:
                # Traverse upwards
                traverse()
                current_row -= 1
        else:
            print('current row:')
            print(current_row)
            while current_row < ROWS and current_cell.value == 0:
                # Traverse upwards
                traverse()
                current_row += 1

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
    global COLUMNS

    move_col = move[0]
    move_row = move[1]

    target_cell = move_col + (move_row * (COLUMNS))

    return target_cell

game = GameState()







