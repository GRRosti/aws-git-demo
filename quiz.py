import random

class QuizGame:
    """A class to represent a simple Quiz Game with multiple participants."""

    def __init__(self):
        """
        Initializes a new QuizGame.
        Participant names, number of questions, and scores will be set later based on user input.
        """
        # Define the questions as a dictionary where keys are topics and values are lists of question dictionaries.
        # Each question dictionary contains 'question' and 'answer'.
        self.questions = {
            "Python Basics": [
                {'question': 'What keyword is used to define a function in Python?', 'answer': 'def'},
                {'question': 'What is the output of 2 + 2 * 3?', 'answer': '8'},
                {'question': 'What is the data type of [1, 2, 3]?', 'answer': 'list'},
                {'question': 'Which built-in function returns the length of an object?', 'answer': 'len'},
                {'question': 'What is the correct way to comment a single line in Python?', 'answer': '#'},
            ],
            "General Knowledge": [
                {'question': 'What is the capital of France?', 'answer': 'Paris'},
                {'question': 'What is the largest planet in our solar system?', 'answer': 'Jupiter'},
                {'question': 'What is the chemical symbol for water?', 'answer': 'H2O'},
                {'question': 'Who wrote "Romeo and Juliet"?', 'answer': 'Shakespeare'},
                {'question': 'What is the highest mountain in the world?', 'answer': 'Mount Everest'},
            ],
            "Science": [
                {'question': 'What is the process by which plants make their own food?', 'answer': 'Photosynthesis'},
                {'question': 'What is the force that pulls objects towards the center of the Earth?', 'answer': 'Gravity'},
                {'question': 'What is the smallest unit of matter?', 'answer': 'Atom'},
                {'question': 'What is the boiling point of water in Celsius?', 'answer': '100'},
                {'question': 'What gas do plants absorb from the atmosphere?', 'answer': 'Carbon Dioxide'},
            ]
        }
        self.participants = [] # List to store participant names
        self.scores = {} # Dictionary to store scores, key is participant name, value is score
        self.total_questions = 0 # Will be set by user input
        self.current_question_index = 0  # Track the number of questions asked
        self.current_participant_index = 0 # Track whose turn it is
        self.winner = None # Will be set at the end of the game
        self.winner_score = 0 # Will be set at the end of the game
        self.winner_name = None # Will be set at the end of the game

    def get_participant_info(self):
        """Prompts for participant names and the number of questions."""
        while True:
            try:
                num_participants_str = input("How many participants are playing? ")
                num_participants = int(num_participants_str)
                if num_participants > 0:
                    break
                else:
                    print("Please enter a positive number of participants.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        for i in range(num_participants):
            name = input(f"Enter name for Participant {i + 1}: ")
            self.participants.append(name)
            self.scores[name] = 0 # Initialize score for each participant

        while True:
            try:
                num_questions_str = input("How many questions would you like to answer in total? ")
                num_questions = int(num_questions_str)
                if num_questions > 0:
                    self.total_questions = num_questions
                    break # Exit the loop if input is a valid positive integer
                else:
                    print("Please enter a positive number of questions.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        print(f"\nWelcome, {', '.join(self.participants)}! You will answer a total of {self.total_questions} questions, taking turns.")

    def ask_question(self):
        """Asks a question to the current participant."""
        if self.current_question_index < self.total_questions:
            # Determine the current participant based on the index
            current_participant = self.participants[self.current_participant_index]

            # Randomly select a topic and question
            topic = random.choice(list(self.questions.keys()))
            question_data = random.choice(self.questions[topic])

            # Print the question for the current participant
            print(f"\n{current_participant}'s turn.")
            print(f"Topic: {topic}")
            print(f"Question: {question_data['question']}")

            # Get the user's answer input.
            answer = input("Your answer: ")

            # Check if the user's answer matches the correct answer (case-insensitive comparison).
            if answer.lower() == question_data['answer'].lower():
                print("Correct!")
                # Increment the score for the current participant.
                self.scores[current_participant] += 1
            else:
                # Inform the user that the answer is wrong and provide the correct answer.
                print(f"Wrong! The correct answer is: {question_data['answer']}")

            # Increment the question index to track the number of questions asked so far.
            self.current_question_index += 1

            # Switch to the next participant for the next question
            self.current_participant_index = (self.current_participant_index + 1) % len(self.participants)

        else:
            # This case should ideally not be reached if the game loop is correct,
            # but included for completeness.
            print("No more questions available.")


    def start_game(self):
        """Starts and runs the main quiz game loop."""
        print("Welcome to the Quiz Game!")

        # Get participant names and number of questions before starting
        self.get_participant_info()

        # Loop to ask questions until the total number of questions is reached.
        while self.current_question_index < self.total_questions:
            self.ask_question()

        # After all questions are asked, display the final scores.
        self.display_scores()
        # Determine the winner based on the highest score.
        self.determine_winner()
        # Call the method to determine the winner after all questions are answered

    def display_scores(self):
        """Displays the final scores for all participants."""
        print("\nQuiz Finished!")
        print("Final Scores:")
        # Iterate through the scores dictionary and print each participant's score
        for name, score in self.scores.items():
            print(f"{name}: {score} out of {self.total_questions}")
    def determine_winner(self):
        """Determines the winner based on the highest score."""
        max_score = max(self.scores.values())
        winners = [name for name, score in self.scores.items() if score == max_score]
        if len(winners) == 1:
            self.winner_name = winners[0]
            self.winner_score = max_score
        else:
            self.winner_name = " and ".join(winners)
            self.winner_score = max_score
        print(f"\nCongratulations {self.winner_name}! You are the winner with a score of {self.winner_score} out of {self.total_questions}.")

        # Call the method to determine the winner after all questions are answered.
# --- Main part of the script ---
if __name__ == "__main__":
    # Create an instance of the QuizGame class.
    game = QuizGame()

    # Start the quiz game.
    game.start_game()

   
    # Call the method to switch participants after each question.
    # Call the method to update the score for the current participant.
