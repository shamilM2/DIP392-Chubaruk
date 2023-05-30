import random,time
from PIL import Image, ImageOps
import io
import pygame
import PySimpleGUI as sg
import threading

# Constants
DICE_SIZE = (100, 100)
NUM_ROUNDS = 6

# Function to play the game open sound
def play_game_open_sound():
    game_open_sound.play()

# Function to stop the game open sound
def stop_game_open_sound():
    game_open_sound.stop()

# Initialize the sound mixer
pygame.mixer.init()

# Load the sound file for game open
game_open_sound = pygame.mixer.Sound('sounds/game_open.wav')

# Class representing a dice
class Dice:
    def __init__(self, sides=6):
        self.sides = sides
        self.value = None
    
    def roll(self):
        self.value = random.randint(1, self.sides)
        return self.value

# Class representing the game
class Game:
    def __init__(self, players):
        self.players = players
        self.current_round = 1
        self.scores = [0] * players
        self.dice = [Dice() for _ in range(3)]
    
    def play_round(self):
        # Display round information
        sg.popup(f"Round {self.current_round}", title="Bunco")

        for player in range(self.players):
            # Display player turn information
            sg.popup(f"Player {player+1}, it's your turn.", title="Bunco")
            sg.popup("Click OK to roll the dice...", title="Bunco")

            # Play dice roll sound
            dice_roll_sound.play()

            # Roll the dice
            dice_values = [die.roll() for die in self.dice]

            # Calculate the score for the round
            score = sum([1 for value in dice_values if value == self.current_round])

            # Display dice images
            self.display_dice_images(dice_values)

            # Play score update sound
            score_update_sound.play()

            # Display the score for the round
            sg.popup(f"Score: {score}", title="Bunco")

            # Update the player's score
            self.scores[player] += score

        self.current_round += 1

    def play_game(self):
        self.current_player = 0
        while self.current_round <= NUM_ROUNDS:
            self.play_round()

        # Display the game results
        self.display_results()
        stop_game_open_sound()
        game_finish_sound.play()
        sg.popup(self.results, title="Bunco")

    def display_dice_images(self, dice_values):
        # Create the layout for displaying dice images
        dice_images_layout = [[sg.Image(dice_images[die_value], key=f'die{i}') for i, die_value in enumerate(dice_values)]]
        sg.Window('Dice', dice_images_layout).read()

    def display_results(self):
        self.results = "Game Over!\n"
        for player in range(self.players):
            self.results += f"Player {player+1} Score: {self.scores[player]}\n"

    def get_scores(self):
        return self.scores

# Function to start the game
def start_game():
    layout = [
        [sg.Text("Welcome to Bunco!", font=("Helvetica", 20))],
        [sg.Text("Enter the number of players:", font=("Helvetica", 16)), sg.InputText(key='num_players', font=("Helvetica", 16))],
        [sg.Button('Start', font=("Helvetica", 16)), sg.Button('Exit', font=("Helvetica", 16))]
    ]

    window = sg.Window('Bunco', layout, size=(500, 200))
    play_game_open_sound()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Start':
            try:
                num_players = int(values['num_players'])
                game = Game(num_players)
                game.play_game()
                break
            except:
                sg.popup("Invalid input! Please enter a valid integer.", title="Bunco")

    window.close()

# Function for the main menu
def main_menu():
    layout = [
        [sg.Text("Bunco Menu", font=("Helvetica", 20))],
        [sg.Button('Start Game', font=("Helvetica", 16))],
        [sg.Button('Instructions', font=("Helvetica", 16))],
        [sg.Button('Exit', font=("Helvetica", 16))]
    ]

    window = sg.Window('Bunco', layout, size=(500, 200))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Start Game':
            start_game()
        elif event == 'Instructions':
            show_instructions()

    window.close()

# Function to show the game instructions
def show_instructions():
    instructions = """
    Bunco is a dice game played with 3 dice. The game consists of multiple rounds, and in each round, players take turns rolling the dice.
    The goal of the game is to score points by rolling dice that match the current round number.
    For each dice that matches the current round number, the player earns 1 point. Rolling a Bunco (all three dice showing the same number as the current round number) earns the player 21 points.
    The game lasts for a total of 6 rounds, and the player with the highest score at the end wins.
    """

    sg.popup('Instructions', instructions, title='Bunco Instructions')

# Load the dice images
dice_images = {}
for i in range(1, 7):
    filename = f'dices/inverted-dice-{i}.png'
    image = Image.open(filename)
    image = ImageOps.fit(image, DICE_SIZE, method=Image.LANCZOS)
    bio = io.BytesIO()
    image.save(bio, format='PNG')
    dice_images[i] = bio.getvalue()

# Initialize the sound mixer
pygame.mixer.init()

# Load the sound files
dice_roll_sound = pygame.mixer.Sound('sounds/dice_roll.wav')
score_update_sound = pygame.mixer.Sound('sounds/score_update.wav')
game_finish_sound = pygame.mixer.Sound('sounds/game_finish.wav')

# Main program
main_menu()
