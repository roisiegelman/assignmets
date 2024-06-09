import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGame:
    def __init__(self, master):
        self.master = master
        master.title("Number Guessing Game")
        master.geometry("300x200")
        
        # Frame for the header
        self.header_frame = tk.Frame(master)
        self.header_frame.pack(pady=10)
        
        self.label = tk.Label(self.header_frame, text="Guess the number between 1 and 20:", font=("Helvetica", 12))
        self.label.pack()
        
        # Frame for the input and buttons
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=10)
        
        self.entry = tk.Entry(self.input_frame, font=("Helvetica", 12))
        self.entry.pack(pady=5)
        
        self.guess_button = tk.Button(self.input_frame, text="Guess", command=self.guess, font=("Helvetica", 12))
        self.guess_button.pack(pady=5)
        
        self.result_label = tk.Label(self.input_frame, text="", font=("Helvetica", 10), fg="blue")
        self.result_label.pack(pady=5)
        
        # Frame for the control buttons
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(pady=10)
        
        self.show_button = tk.Button(self.control_frame, text="Show Number", command=self.show_number, font=("Helvetica", 12))
        self.show_button.pack(side=tk.LEFT, padx=5)
        
        self.new_game_button = tk.Button(self.control_frame, text="New Game", command=self.new_game, font=("Helvetica", 12))
        self.new_game_button.pack(side=tk.LEFT, padx=5)
        
        self.exit_button = tk.Button(self.control_frame, text="Exit", command=master.quit, font=("Helvetica", 12))
        self.exit_button.pack(side=tk.LEFT, padx=5)
        
        self.number_to_guess = self.generate_random_number()
        self.attempts = 0
    
    def generate_random_number(self):
        return random.randint(1, 20)
    
    def guess(self):
        try:
            guess = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a number between 1 and 20.")
            return
        
        self.attempts += 1
        
        if guess == self.number_to_guess:
            messagebox.showinfo("Congratulations!", f"Congrats! You guessed the number {self.number_to_guess} correctly in {self.attempts} attempts.")
            self.new_game()
        elif guess < self.number_to_guess:
            self.result_label.config(text="Guess again, your number is too small!")
        elif guess > self.number_to_guess:
            self.result_label.config(text="Guess again, your number is too large!")
    
    def show_number(self):
        messagebox.showinfo("Hidden Number", f"The hidden number is: {self.number_to_guess}")
    
    def new_game(self):
        self.number_to_guess = self.generate_random_number()
        self.attempts = 0
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
        messagebox.showinfo("New Game", "A new game has started. Guess the new number!")

def main():
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
