import random

class TicTacToe:
    """A class to represent a Tic-Tac-Toe game."""

    def __init__(self):
        """Initializes a new game."""
        self.board = [' '] * 10  # The game board, index 0 is unused
        self.player1_marker = ''
        self.player2_marker = ''
        self.player1_name = ''
        self.player2_name = ''
        self.turn = ''
        self.game_on = True

    def display_board(self):
        """Prints the current state of the Tic-Tac-Toe board."""
        print("\n")
        print(" 7 " + self.board[7] + " |8 " + self.board[8] + " |9 " + self.board[9])
        print("-----------")
        print(" 4 " + self.board[4] + " |5 " + self.board[5] + " |6 " + self.board[6])
        print("-----------")
        print(" 1 " + self.board[1] + " |4 " + self.board[2] + " |5 " + self.board[3])
        print("\n")

    def player_input(self):
        """Asks players to choose X or O and sets their markers."""
        marker = ''
        while not (marker == 'X' or marker == 'O'):
            marker = input('Player 1: Do you want to be X or O? ').upper()

        if marker == 'X':
            self.player1_marker = 'X'
            self.player2_marker = 'O'
        else:
            self.player1_marker = 'O'
            self.player2_marker = 'X'

    def place_marker(self, marker, position):
        """Places the player's marker on the board at the given position."""
        self.board[position] = marker

    def win_check(self, mark):
        """Checks if the player with 'mark' has won."""
        return ((self.board[7] == mark and self.board[8] == mark and self.board[9] == mark) or # across the top
                (self.board[4] == mark and self.board[5] == mark and self.board[6] == mark) or # across the middle
                (self.board[1] == mark and self.board[2] == mark and self.board[3] == mark) or # across the bottom
                (self.board[7] == mark and self.board[4] == mark and self.board[1] == mark) or # down the left side
                (self.board[8] == mark and self.board[5] == mark and self.board[2] == mark) or # down the middle
                (self.board[9] == mark and self.board[6] == mark and self.board[3] == mark) or # down the right side
                (self.board[7] == mark and self.board[5] == mark and self.board[3] == mark) or # diagonal
                (self.board[9] == mark and self.board[5] == mark and self.board[1] == mark)) # diagonal

    def choose_first(self):
        """Randomly decides which player goes first and sets the turn."""
        if random.randint(0, 1) == 0:
            self.turn = 'Player 2'
        else:
            self.turn = 'Player 1'
        print(self.turn + ' will go first.')


    def space_check(self, position):
        """Checks if a space on the board is freely available."""
        return self.board[position] == ' '

    def full_board_check(self):
        """Checks if the board is full."""
        for i in range(1, 10):
            if self.space_check(i):
                return False
        return True

    def player_choice(self):
        """Asks the player for their next position (1-9) and validates the input."""
        position = 0
        while position not in range(1, 10) or not self.space_check(position):
            try:
                position = int(input('Choose your next position: (1-9) '))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")

        return position

    def replay(self):
        """Asks the players if they want to play again."""
        return input('Do you want to play again? Enter Yes or No: ').lower().startswith('y')

    def play_game(self):
        """Runs the main game loop."""
        print('Welcome to Tic Tac Toe!')

        while True:
            # Reset the game state
            self.__init__() # Re-initialize the object for a new game

            self.player_input()
            self.player1_name = input("Enter Player 1's name: ")
            self.player2_name = input("Enter Player 2's name: ")
            self.choose_first()

            while self.game_on:
                if self.turn == 'Player 1':
                    # Player 1's turn
                    self.display_board()
                    print(f"{self.player1_name}'s turn.")
                    position = self.player_choice()
                    self.place_marker(self.player1_marker, position)

                    if self.win_check(self.player1_marker):
                        self.display_board()
                        print(f'Congratulations {self.player1_name}! You have won the game!')
                        self.game_on = False
                    else:
                        if self.full_board_check():
                            self.display_board()
                            print('The game is a tie!')
                            break
                        else:
                            self.turn = 'Player 2'

                else:
                    # Player 2's turn
                    self.display_board()
                    print(f"{self.player2_name}'s turn.")
                    position = self.player_choice()
                    self.place_marker(self.player2_marker, position)

                    if self.win_check(self.player2_marker):
                        self.display_board()
                        print(f'Congratulations {self.player2_name}! You have won the game!')
                        self.game_on = False
                    else:
                        if self.full_board_check():
                            self.display_board()
                            print('The game is a tie!')
                            break
                        else:
                            self.turn = 'Player 1'

            if not self.replay():
                break

# Create an instance of the game and play
if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()

# This code implements a simple Tic Tac Toe game where two players (X and O) take turns making moves.
# The game board is represented as a list of 9 elements, and the game continues until there is a winner or a tie.
# The game is played in the console, and the board is printed after each move.
# The winner is determined by checking the rows, columns, and diagonals for three of the same symbol in a row.
# The game ends when there is a winner or all squares are filled, resulting in a tie.
# The game is played using random moves for both players, but you can modify the code to allow for user input.