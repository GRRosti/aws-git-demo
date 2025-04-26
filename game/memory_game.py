import random
import time

class MemoryGameBoard:
    """Represents the state and logic of the Memory Game board."""

    def __init__(self, rows, cols, values_list, category_name="Items"):
        """Initializes the game board."""
        if (rows * cols) % 2 != 0:
            raise ValueError("Grid dimensions (rows * cols) must be even.")
        if len(values_list) * 2 < rows * cols:
             raise ValueError(f"Not enough unique values ({len(values_list)}) for grid size ({rows * cols}). Need at least {(rows * cols) // 2}.")

        self.rows = rows
        self.cols = cols
        self.category_name = category_name
        self._board_values = [] # Stores the actual values
        self._board_state = []  # Stores the state (True for face-up, False for face-down)
        self._initialize_board(values_list)

        self.pairs_found = 0
        self.guesses = 0 # Track pairs of flips

    def _initialize_board(self, values_list):
        """Creates and shuffles the values, then populates the board."""
        # Select just enough unique values and duplicate them
        required_unique_values = (self.rows * self.cols) // 2
        if len(values_list) > required_unique_values:
            selected_values = random.sample(values_list, required_unique_values)
        else:
             selected_values = values_list[:] # Use all provided values if less than needed

        all_values = selected_values * 2 # Create pairs

        # Shuffle the combined list of values
        random.shuffle(all_values)

        # Populate the board grids
        self._board_values = []
        self._board_state = []
        value_index = 0
        for r in range(self.rows):
            row_values = []
            row_state = []
            for c in range(self.cols):
                row_values.append(all_values[value_index])
                row_state.append(False) # Initially all face-down
                value_index += 1
            self._board_values.append(row_values)
            self._board_state.append(row_state)

    def display_board(self, selected_coords=None):
        """Prints the current state of the board, showing face-up values or '*'."""
        print("\n" + "-" * (self.cols * 4 + 3))
        # Print column headers
        print("    " + " ".join([f"{c+1:<3}" for c in range(self.cols)]))
        print("   " + "----" * self.cols + "-")

        for r in range(self.rows):
            print(f"{r+1:<2}|", end=" ")
            for c in range(self.cols):
                if self._board_state[r][c] or (selected_coords and (r, c) in selected_coords):
                    # Show value if face-up or temporarily selected
                    print(f"{str(self._board_values[r][c]):<3}", end=" ")
                else:
                    # Show face-down indicator
                    print("* ", end=" ")
            print("|")
        print("-" * (self.cols * 4 + 3))

    def is_valid_selection(self, row, col):
        """Checks if the selected coordinates are within bounds and the cell is face-down."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            print("Invalid input: Coordinates out of bounds.")
            return False
        if self._board_state[row][col]:
            print("Invalid input: That cell is already face-up.")
            return False
        return True

    def flip_cell(self, row, col, face_up=True):
        """Sets the state of a cell (face_up=True or face_down=False)."""
        self._board_state[row][col] = face_up

    def get_cell_value(self, row, col):
        """Returns the value of the cell at the given coordinates."""
        return self._board_values[row][col]

    def check_match(self, r1, c1, r2, c2):
        """Checks if the values at the two sets of coordinates match."""
        return self._board_values[r1][c1] == self._board_values[r2][c2]

    def mark_matched(self, r1, c1, r2, c2):
        """Marks two cells as permanently face-up and increments pairs_found."""
        # Their state is already True from flip_cell, no need to re-set
        self.pairs_found += 1

    def hide_cells(self, r1, c1, r2, c2):
        """Sets two cells back to face-down state."""
        self._board_state[r1][c1] = False
        self._board_state[r2][c2] = False

    def is_game_over(self):
        """Checks if all pairs have been found."""
        return self.pairs_found * 2 == self.rows * self.cols

    def increment_guesses(self):
        """Increments the guess counter."""
        self.guesses += 1

    def get_guesses(self):
        """Returns the total number of guesses."""
        return self.guesses

def get_valid_selection(board, prompt):
    """Prompts the player for coordinates until a valid face-down cell is selected."""
    while True:
        try:
            user_input = input(prompt).split()
            if len(user_input) != 2:
                print("Invalid input format. Please enter row and column numbers separated by a space.")
                continue

            row = int(user_input[0]) - 1 # Convert to 0-based index
            col = int(user_input[1]) - 1 # Convert to 0-based index

            if board.is_valid_selection(row, col):
                return row, col
            # is_valid_selection prints the error message

        except ValueError:
            print("Invalid input. Please enter numbers for row and column.")

def main_game():
    """Main function to set up and run the memory game."""
    # --- Game Setup ---
    print("Welcome to the Memory Game!")

    # Define available categories and values
    categories = {
        "colors": ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown"],
        "fruits": ["apple", "banana", "cherry", "date", "grape", "kiwi", "lemon", "mango"],
        "cars": ["ford", "audi", "bmw", "chevy", "honda", "jeep", "kia", "nissan"]
    }

    # --- Get Grid Dimensions ---
    while True:
        try:
            rows = int(input("Enter the number of rows (at least one dimension must be even): "))
            cols = int(input("Enter the number of columns (at least one dimension must be even): "))
            if (rows * cols) % 2 != 0:
                 print("The total number of cells (rows * cols) must be even.")
            elif rows <= 0 or cols <= 0:
                 print("Rows and columns must be positive numbers.")
            else:
                 break
        except ValueError:
            print("Invalid input. Please enter whole numbers for rows and columns.")

    # --- Choose Category ---
    print("\nAvailable categories:")
    for i, category_name in enumerate(categories.keys()):
        print(f"{i+1}. {category_name.capitalize()}")

    chosen_values = None
    chosen_category_name = None
    while chosen_values is None:
        try:
            choice = int(input(f"Select a category (1-{len(categories)}): "))
            category_names_list = list(categories.keys())
            if 1 <= choice <= len(categories):
                chosen_category_name = category_names_list[choice - 1]
                chosen_values = categories[chosen_category_name]
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except IndexError:
             print("Invalid choice. Please select a number from the list.")


    # --- Initialize Board ---
    try:
        board = MemoryGameBoard(rows, cols, chosen_values, chosen_category_name)
    except ValueError as e:
        print(f"Error creating board: {e}")
        return # Exit if board creation fails

    # --- Game Loop ---
    print("\nStarting the game! Find the matching pairs.")

    while not board.is_game_over():
        board.display_board()
        print(f"Guesses: {board.get_guesses()}")

        # Get first selection
        print("\nSelect the first card (row col):")
        r1, c1 = get_valid_selection(board, "> ")
        board.flip_cell(r1, c1, face_up=True) # Temporarily show the first card

        # Get second selection
        board.display_board(selected_coords=[(r1,c1)]) # Show board with first card revealed
        print("\nSelect the second card (row col):")
        # Need to loop until the second selection is valid AND different from the first
        while True:
             r2, c2 = get_valid_selection(board, "> ")
             if r1 == r2 and c1 == c2:
                 print("Invalid input: You must select a different card.")
             else:
                 break
        board.flip_cell(r2, c2, face_up=True) # Temporarily show the second card

        board.increment_guesses() # Count this pair of flips as one guess

        # Display board with both selected cards
        board.display_board(selected_coords=[(r1,c1), (r2,c2)])

        # Check for match
        if board.check_match(r1, c1, r2, c2):
            print("Match found!")
            board.mark_matched(r1, c1, r2, c2) # Keep cards face-up
        else:
            print("No match. Cards will flip back.")
            time.sleep(2) # Pause so player can see the cards
            board.hide_cells(r1, c1, r2, c2) # Flip cards back face-down

    # --- Game Over ---
    board.display_board() # Show final solved board
    print("\nCongratulations! You found all the pairs!")
    print(f"Total guesses: {board.get_guesses()}")

# --- Reliability, Maintainability, Scalability Considerations ---
"""
Reliability:
- Input Validation: The script includes checks to ensure user input for grid dimensions
  is valid (positive integers, product is even) and that selected coordinates
  are within bounds and correspond to a face-down cell. This prevents crashes
  due to malformed input or invalid moves.
- Error Handling: Uses try-except blocks for converting input to numbers (float/int)
  to handle non-numeric input gracefully. Includes checks during board initialization
  to ensure enough values are provided for the chosen grid size.
- State Management: The game state (which cards are face-up/down) is explicitly
  managed in the `_board_state` grid, reducing the chance of inconsistent display
  or logic errors.

Maintainability:
- Modularity (Functions and Class): The code is organized into functions
  (`get_valid_selection`, `main_game`) and a class (`MemoryGameBoard`).
  The class encapsulates the board's data (`_board_values`, `_board_state`,
  `pairs_found`, `guesses`) and its related behavior (display, flipping,
  checking matches, etc.). This separation of concerns makes the code easier
  to understand, modify, and debug.
- Clear Variable Names: Variable names like `order_amount`, `customer_type`,
  `final_amount`, `is_username_valid`, etc., clearly indicate their purpose.
- Comments and Docstrings: Functions and the class have docstrings explaining
  what they do, and comments are used within the code to explain complex or
  non-obvious parts.
- Categories: Card values are defined in a dictionary `categories`, making it
  easy to add, remove, or modify categories without changing the core game logic.

Scalability:
- Grid Size: The core logic for handling the grid using lists of lists scales
  linearly with the number of cells (N*M). Displaying the board, checking state,
  and handling coordinates work for any valid N and M.
- Number of Values/Categories: Adding more values or categories is straightforward;
  just update the `categories` dictionary. The selection and board population logic
  automatically adapts.
- Performance: For a text-based terminal game, the current implementation
  is efficient enough for typical grid sizes. For extremely large grids
  or a graphical interface, performance might need optimization (e.g.,
  using more efficient data structures if memory became an issue, but this
  is unlikely for terminal display).
- Game Complexity: The current logic handles the basic memory game rules.
  More complex rules (e.g., multiple players, different matching rules)
  would require extending the `MemoryGameBoard` class and the main game loop,
  but the existing structure provides a good foundation. The use of text values
  (`str`) means the values themselves don't add computational complexity.
"""

# --- Run the game ---
if __name__ == "__main__":
    main_game()