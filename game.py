from kivy.app import App
from kivy.uix.label import Label
import random
import time
import tkinter as tk
from tkinter import messagebox, simpledialog

class AdditionGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Addition Game")
        
        # Game settings
        self.num_range = (1, 10)
        self.num_problems = 5
        self.score = 0
        self.current_problem = 0
        self.start_time = None
        self.time_limit = 60  # 1-minute time limit
        self.timer_running = False

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Difficulty selection
        self.difficulty_label = tk.Label(self.root, text="Choose Difficulty:")
        self.difficulty_label.pack()

        self.difficulty_var = tk.StringVar(value="easy")
        self.easy_radio = tk.Radiobutton(self.root, text="Easy (1-10)", variable=self.difficulty_var, value="easy")
        self.hard_radio = tk.Radiobutton(self.root, text="Hard (1-100)", variable=self.difficulty_var, value="hard")
        self.easy_radio.pack()
        self.hard_radio.pack()

        # Number of problems selection
        self.problems_label = tk.Label(self.root, text="Number of Problems:")
        self.problems_label.pack()
        self.problems_entry = tk.Entry(self.root)
        self.problems_entry.pack()
        
        # Start button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        # Game area
        self.question_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.question_label.pack(pady=10)
        
        # Answer input field (only allows numbers)
        self.answer_entry = tk.Entry(self.root, font=("Helvetica", 14), validate="key")
        self.answer_entry.pack()
        self.answer_entry.bind("<Return>", self.check_answer)  # Bind Enter key to submit answer
        
        # Configure the validation for numbers only
        self.answer_entry.config(validate="key")
        self.answer_entry['validatecommand'] = (self.root.register(self.only_numbers), '%P')

        # Score display
        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.pack(pady=10)

        # Timer display
        self.timer_label = tk.Label(self.root, text="Time left: 60s")
        self.timer_label.pack(pady=10)

    def only_numbers(self, text):
        return text.isdigit() or text == ""  # Allows only digits or empty text

    def start_game(self):
        # Set difficulty range based on user selection
        difficulty = self.difficulty_var.get()
        self.num_range = (1, 10) if difficulty == "easy" else (1, 100)
        
        # Set the number of problems
        try:
            self.num_problems = int(self.problems_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of problems.")
            return

        # Reset game state
        self.score = 0
        self.current_problem = 0
        self.start_time = time.time()
        self.timer_running = True
        
        # Update UI and start the first question
        self.score_label.config(text="Score: 0")
        self.timer_label.config(text="Time left: 60s")
        self.next_question()
        self.update_timer()  # Start the timer

    def update_timer(self):
        # Check if the timer is still running
        if not self.timer_running:
            return
        
        # Calculate remaining time
        elapsed_time = int(time.time() - self.start_time)
        time_left = self.time_limit - elapsed_time
        
        if time_left > 0:
            self.timer_label.config(text=f"Time left: {time_left}s")
            # Schedule next timer update after 1 second
            self.root.after(1000, self.update_timer)
        else:
            # Time is up, stop the timer and end the game
            self.timer_label.config(text="Time left: 0s")
            self.timer_running = False
            self.end_game()

    def next_question(self):
        if self.current_problem < self.num_problems:
            # Generate a new question
            self.num1 = random.randint(*self.num_range)
            self.num2 = random.randint(*self.num_range)
            self.question_label.config(text=f"What is {self.num1} + {self.num2}?")
            self.answer_entry.delete(0, tk.END)  # Clear the entry box
            self.current_problem += 1
        else:
            # Stop the timer if game is completed before time is up
            self.timer_running = False
            self.end_game()

    def check_answer(self, event=None):
        # Calculate the elapsed time to ensure it's within the 1-minute limit
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.time_limit:
            self.end_game()
            return

        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        # Check if the answer is correct
        if user_answer == (self.num1 + self.num2):
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
        
        # Go to the next question
        self.next_question()

    def end_game(self):
        # Stop the timer
        self.timer_running = False
        
        # Calculate time taken
        time_taken = min(round(time.time() - self.start_time, 2), self.time_limit)
        
        # Show final score within 1-minute limit
        messagebox.showinfo("Game Summary", f"Score within 1 minute: {self.score}/{self.num_problems}\nTime Taken: {time_taken} seconds")
        
        # Ask if the player wants to play again
        play_again = messagebox.askyesno("Play Again?", "Do you want to play again?")
        if play_again:
            self.start_game()
        else:
            self.root.quit()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AdditionGameApp(root)
    root.mainloop()
