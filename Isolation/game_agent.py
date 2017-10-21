"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    opponent = game.get_opponent(player)
    my_moves = len(game.get_legal_moves())
    opponent_moves = len(game.get_legal_moves(opponent))

    # Score: 65%
    # return float(my_moves - (2 * opponent_moves))

    # Score: 66%
    # return float(my_moves - (opponent_moves ** 2))

    # Opponent's moves are weighted exponentially
    # So the nodes where the opponent has many possible moves
    # Are weighted much more negatively

    # Score: 74%
    return float(my_moves - (opponent_moves ** 1.5))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)
    my_moves = len(game.get_legal_moves())
    opponent_moves = len(game.get_legal_moves(opponent))

    # Score: 63%
    # return float(my_moves - opponent_moves)

    # Both players' moves counts are weighted exponentially
    # With the opponent's moves being weighted more heavily
    # Using indices means nodes with notably more moves are
    # Weighted much more heavily

    # Score: 70%
    return float((my_moves ** 2) - (opponent_moves ** 2.5))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # If game is over, return with the result
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)
    my_moves = len(game.get_legal_moves())
    opponent_moves = len(game.get_legal_moves(opponent))

    # Score: 64%
    # return float(len(game.get_legal_moves()))
    
    # Score: 64%
    # return float((my_moves ** 2) - opponent_moves))

    # Score: 64%
    # return float((my_moves ** 2) - (opponent_moves ** 2))

    # Opponent's moves are weighted *much* more heavily
    # So AI will be super aggressive

    # Score: 68%
    return float((my_moves ** (1/2)) - (opponent_moves ** 2))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        if legal_moves:
            best_move = legal_moves[0]
        else:
            return (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        def terminal_test(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
                
            if depth == 0:
                return True
            return not bool(game.get_legal_moves())

        def max_value(game, depth):
            # Return a loss (-1) if the game is over
            # Else give max value for all legal nodes
            if terminal_test(game, depth):
                return self.score(game, self)

            value = float("-inf")
            for move in game.get_legal_moves():
                value = max(value, min_value(game.forecast_move(move), depth - 1))
            return value

        def min_value(game, depth):
            # Return a win if the game is over
            # Else give min value for all legal nodes
            if terminal_test(game, depth):
                return self.score(game, self)

            value = float("inf")
            for move in game.get_legal_moves():
                value = min(value, max_value(game.forecast_move(move), depth - 1))
            return value

        def get_minimax_decision(game, depth):
            """ Return the move along a branch of the game tree that
            has the best possible value.  A move is a pair of coordinates
            in (column, row) order corresponding to a legal move for
            the searching player.
            
            Ignoring the special case of calling this function
            from a terminal state.
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            best_score = float("-inf")
            legal_moves = game.get_legal_moves()
            if legal_moves:
                best_move = legal_moves[0]
            else:
                return (-1, -1)

            for move in game.get_legal_moves():
                forecasted_game = game.forecast_move(move)
                new_score = max(best_score, min_value(forecasted_game, depth - 1))
                if new_score > best_score:
                    best_score = new_score
                    best_move = move
            return best_move
        
        return get_minimax_decision(game, depth)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        if legal_moves:
            best_move = legal_moves[0]
        else:
            return (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire

            depth_level = 1
            while True:
                best_move = self.alphabeta(game, depth_level)
                depth_level += 1

            # for depth_level in range(1, self.search_depth):
            #     best_move = self.alphabeta(game, depth_level)

        except SearchTimeout:
            # Handle any actions required after timeout as needed
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")

        legal_moves = game.get_legal_moves()
        if legal_moves:
            best_move = legal_moves[0]
        else:
            return (-1, -1)

        if self.terminal_test(game, depth):
            return best_move

        for next_move in game.get_legal_moves():
            # Get game state where player does next_move
            game_forecast = game.forecast_move(next_move)
            # Get score for game state where next_move is taken
            next_score = self.min_value(game_forecast, depth - 1, alpha, beta)
            # Update best move & best score if current score is better
            if next_score > best_score:
                best_move = next_move
                best_score = next_score
            # Best move found
            if best_score >= beta:
                break
            # Update lower bound
            alpha = max(alpha, best_score)
        return best_move

    def terminal_test(self, game, depth):
        if depth == 0 or not game.get_legal_moves():
            return True

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(game, depth):
            return self.score(game, self)

        value = float("-inf")
        for move in game.get_legal_moves():
            game_forecast = game.forecast_move(move)
            value = max(value, self.min_value(game_forecast, depth - 1, alpha, beta))
            if value >= beta:
                # Found upper value
                return value
            # Update lower bound
            alpha = max(alpha, value)

        return value

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(game, depth):
            return self.score(game, self)

        value = float("inf")
        for move in game.get_legal_moves():
            game_forecast = game.forecast_move(move)
            value = min(value, self.max_value(game_forecast, depth - 1, alpha, beta))
            if value <= alpha:
                # Found lower value
                return value
            # Update upper bound
            beta = min(beta, value)

        return value