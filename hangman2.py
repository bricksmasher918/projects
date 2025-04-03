import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QGridLayout, QHBoxLayout, QCheckBox, QRadioButton, QButtonGroup, QLineEdit, QPushButton, QStyleFactory
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt


class HangmanGame(QMainWindow):
        
    def __init__(self):
        super().__init__()
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.words = [
    "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon",
    "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine", "ugli",
    "vigilant", "watermelon", "xylophone", "yellow", "zebra", "ant", "bird", "cat", "dog", "elephant",
    "frog", "giraffe", "hippopotamus", "iguana", "jaguar", "kangaroo", "lion", "monkey", "newt", "octopus",
    "parrot", "quail", "rabbit", "snake", "tiger", "umbrella", "vulture", "whale", "xenon", "yak",
    "zebra", "abacus", "ball", "candle", "door", "elephant", "flag", "glove", "hat", "ice",
    "jug", "kite", "lamp", "mug", "notebook", "orange", "pencil", "quilt", "ring", "sock",
    "tree", "umbrella", "van", "wallet", "xylophone", "yarn", "zoo", "apple", "box", "cake",
    "dove", "egg", "flag", "goat", "hug", "ink", "jacket", "key", "leaf", "moon", "nest",
    "owl", "pen", "quilt", "rod", "sail", "tub", "vase", "whistle", "gay", "yellow", "zebra"
]
        self.chosen_word = random.choice(self.words)
        self.hangman_list = ['''
 +--+
 |    |
      |
      |
      |
      |
=========''', '''
 +--+
 |    |
 O   |
      |
      |
      |
=========''', '''
 +--+
 |    |
 O   |
  |   |
      |
      |
=========''', '''
 +--+
 |    |
 O   |
 /|   |
      |
      |
=========''', '''
 +--+
 |    |
 O   |
 /|\\  |
      |
      |
=========''', '''
 +--+
 |    |
 O   |
 /|\\  |
 /    |
      |
=========''', '''
 +--+
 |    |
 O   |
 /|\\  |
 / \\  |
      |
=========''']
        self.setWindowTitle("Hangman Game")
        self.word = ""
        print(self.chosen_word)
        self.wrong_words = []
        self.correct_letters = []
        self.wrong_letters = []
        self.wrong = 0
        self.feedback_text = ""
        self.output = ""
        self.initUI()


    def initUI(self):

# win label
        self.win_message_label = QLabel("", self)
        self.win_message_label.setGeometry(300, 250, 400, 50)
        self.win_message_label.setStyleSheet("font-size: 30px; font-weight: bold;")

# play again
        self.play_again_button = QPushButton("Play Again", self)
        self.play_again_button.setGeometry(350, 350, 100, 50)
        self.play_again_button.setStyleSheet("font-size: 20px;")
        self.play_again_button.setVisible(False)
        self.play_again_button.clicked.connect(self.play_again)

# window
        self.title_label = QLabel("Hangman Game")
        self.title_label.setGeometry(10, 10, 500, 100)
        self.title_label.setStyleSheet("font-size: 20px;")
        self.word_display = QLabel("")
        self.word_display.setFont(QFont("Arial", 20))
        self.word_display.setGeometry(500, 500, 500, 100)

# letter input
        self.input_letter = QLineEdit(self)
        self.input_letter.setPlaceholderText("Enter a letter")
        self.input_letter.setGeometry(20, 20, 200, 50)
        self.input_letter.setFont(QFont("Arial", 20))

# word input
        self.input_word = QLineEdit(self)
        self.input_word.setPlaceholderText("Enter a word")
        self.input_word.setGeometry(20, 150, 200, 50)
        self.input_word.setFont(QFont("Arial", 20))

# wrong guesses
        self.wrong_letters_text = self.return_wrong_letter()
        self.wrong_letter_guesses_label = QLabel(f"Wrong letter guesses: {self.wrong_letters_text}", self)
        self.wrong_letter_guesses_label.setGeometry(20, 100, 400, 50)
        self.wrong_letter_guesses_label.setFont(QFont("Arial", 15))

# right guesses
        self.correct_letters_text = self.return_correct_letter()
        self.right_guesses_label = QLabel(f"Right letter guesses: {self.correct_letters_text}", self)
        self.right_guesses_label.setGeometry(20, 70, 400, 50)
        self.right_guesses_label.setFont(QFont("Arial", 15))

# wrong word guesses
        self.wrong_word_guesses_label = QLabel("Wrong word guesses: ", self)
        self.wrong_word_guesses_label.setGeometry(20, 200, 400, 50)
        self.wrong_word_guesses_label.setFont(QFont("Arial", 15))
        
        self.wrong_guesses_text = self.return_wrong_words()
        self.label_wrong_guess = QLabel(self.wrong_guesses_text,self)
        self.label_wrong_guess.setGeometry(20, 250, 400, 50)
        self.label_wrong_guess.setStyleSheet("font-size: 20px;")


# submit buttons
        self.pushbutton1 = QPushButton("Submit",self)
        self.pushbutton1.setGeometry(225,20,100,50)
        self.pushbutton1.setStyleSheet("font-size:20px")

        self.pushbutton1.clicked.connect(self.get_letter_input)

        self.pushbutton2 = QPushButton("Submit",self)
        self.pushbutton2.setGeometry(225,150,100,50)
        self.pushbutton2.setStyleSheet("font-size:20px")

        self.pushbutton2.clicked.connect(self.get_word_input)

# hangman
        self.hangman = QLabel(self.hangman_list[self.wrong],self)
        self.hangman.setGeometry(480,20,500,500)
        self.hangman.setStyleSheet("font-size: 40px; background-color: hsl(199, 1%, 80%);padding: 10px 75px; margin: 25px; border: 5px solid; border-radius: 10px;")
        self.hangman.setAlignment(Qt.AlignCenter)

# secret word
        self.output = self.return_word()
        self.secret_word = QLabel(self.output,self)
        self.secret_word.setGeometry(480,540,500,140)
        self.secret_word.setStyleSheet("font-size: 40px;")
        self.secret_word.setAlignment(Qt.AlignCenter)

# feedback
        self.feedback = QLabel(self.feedback_text,self)
        self.feedback.setGeometry(20, 600, 600, 50)
        self.feedback.setStyleSheet("font-size: 20px;")

    def show_win_screen(self):
        self.win_message_label.setText("You Win!")
        self.win_message_label.setStyleSheet("font-size: 30px;color: #3ec94c; font-weight: bold;")
        self.play_again_button.setVisible(True)

    def show_loose_screen(self):
        self.win_message_label.setText("You Lost!")
        self.win_message_label.setStyleSheet("font-size: 30px;color: #c72c2c; font-weight: bold;")
        self.play_again_button.setVisible(True)

    def play_again(self):
        self.chosen_word = random.choice(self.words)
        self.correct_letters = []
        self.wrong_letters = []
        self.wrong = 0
        self.feedback_text = ""
        self.output = ""
        
        self.win_message_label.setText("")
        self.play_again_button.setVisible(False)
        
        self.secret_word.setText(self.return_word())
        self.feedback.setText("")
        
        self.wrong = 0
        self.update_hangman()
        self.wrong_letters_text = self.return_wrong_letter()
        self.wrong_letter_guesses_label.setText(f"Wrong letter guesses: {self.wrong_letters_text}")
        self.correct_letters_text = self.return_correct_letter()
        self.right_guesses_label.setText(f"Right letter guesses: {self.correct_letters_text}")
        self.wrong_guesses_text = self.return_wrong_words()
        self.label_wrong_guess.setText(self.wrong_guesses_text)

    def return_wrong_words(self):
        self.wrong_word_guesses = " , ".join(self.wrong_words)
        return self.wrong_word_guesses

    def return_correct_letter(self):
        return " , ".join(sorted(self.correct_letters)).upper()

    def return_wrong_letter(self):
        return " , ".join(sorted(self.wrong_letters)).upper()

    def update_hangman(self):
        self.hangman.setText(self.hangman_list[self.wrong])

    def update_feedback(self):
        self.feedback.setText(self.feedback_text)

    def return_word(self):
        self.output = ""
        for letter in self.chosen_word:
            if letter in self.correct_letters:
                self.output += letter + " "
            else:
                self.output += "_ "
        return self.output.strip()

    def get_letter_input(self):
        user_letter = self.input_letter.text().lower()
        self.input_letter.clear()

        if user_letter not in self.alphabet:
            self.feedback_text = "Invalid input. Please enter a single letter."
            self.feedback.setStyleSheet("font-size: 20px;color : black")
            self.update_feedback()


        elif user_letter in self.correct_letters or user_letter in self.wrong_letters:
            self.feedback_text = f"You have already guessed the letter ' {user_letter.upper()} ' ."
            self.feedback.setStyleSheet("font-size: 20px;color : black")
            self.update_feedback()


        elif user_letter in self.chosen_word:
            self.feedback_text = f"Good job. The letter ' {user_letter.upper()} ' was in the word."
            self.update_feedback()
            self.correct_letters.append(user_letter)
            self.output = self.return_word()
            self.secret_word.setText(self.output.upper())
            self.correct_letters_text = self.return_correct_letter()
            self.right_guesses_label.setText(f"Right letter guesses: {self.correct_letters_text}")
            self.feedback.setStyleSheet("font-size: 20px;color : #3ec94c")
            print(self.output.replace(" ",""))
            if self.output == self.chosen_word:
                self.show_win_screen()


        else:
            self.feedback_text = f"Nice guess but the letter ' {user_letter.upper()} ' wasn't in the word."
            self.update_feedback()
            self.wrong_letters.append(user_letter)
            self.wrong += 1
            if self.wrong == 7:
                self.show_loose_screen()
                self.wrong = 0
            self.update_hangman()
            self.wrong_letters_text = self.return_wrong_letter()
            self.wrong_letter_guesses_label.setText(f"Wrong letter guesses: {self.wrong_letters_text}")
            self.feedback.setStyleSheet("font-size: 20px;color : #c72c2c")

    def get_word_input(self):
        user_word = self.input_word.text().lower()
        self.input_word.clear()

        if user_word.isalpha() == False:
            self.feedback_text = "Invalid input. Please enter a word."
            self.feedback.setStyleSheet("font-size: 20px;color : black")
            self.update_feedback()


        elif user_word == self.chosen_word:
            self.show_win_screen()


        elif user_word in self.wrong_words:
            self.feedback_text = f"You have already guessed ' {user_word.upper()} ' ."
            self.feedback.setStyleSheet("font-size: 20px;color : black")
            self.update_feedback()


        else:
            self.feedback_text = f"Nice guess but ' {user_word.upper()} ' wasn't the word."
            self.update_feedback()
            self.wrong_words.append(user_word)
            self.wrong_guesses_text = self.return_wrong_words()
            self.label_wrong_guess.setText(self.wrong_guesses_text)
            self.feedback.setStyleSheet("font-size: 20px;color : #c72c2c")

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HangmanGame()
    window.setGeometry(100, 100, 1000, 700)
    window.show()
    sys.exit(app.exec_())