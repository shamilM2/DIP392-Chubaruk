import random
from PIL import Image, ImageOps
import PySimpleGUI as sg
import io

size = (100, 100)

# Load the dice images
dice_images = {}
for i in range(1, 7):
    filename = f'dices/inverted-dice-{i}.png'
    image = Image.open(filename)
    image = ImageOps.fit(image, size, method=Image.LANCZOS)
    bio = io.BytesIO()
    image.save(bio, format='PNG')
    dice_images[i] = bio.getvalue()



class Dice:
    def __init__(self, sides=6):
        self.sides = sides
        self.value = None
    
    def roll(self):
        self.value = random.randint(1, self.sides)
        return self.value


class Game:
    def __init__(self, players):
        self.players = players
        self.current_round = 1
        self.scores = [0] * players
        self.dice = [Dice() for _ in range(3)]
    
    def play_round(self):
        sg.popup("Round " + str(self.current_round), title="Bunco")

        for player in range(self.players):
            sg.popup("Player " + str(player+1) + ", it's your turn.", title="Bunco")
            sg.popup("Click OK to roll the dice...", title="Bunco")
        
            # Roll the dice
            dice_values = [die.roll() for die in self.dice]

            # Calculate the score
            score = sum([1 for value in dice_values if value == self.current_round])

            # Display the dice images
            dice_images_layout = [[sg.Image(dice_images[die_value],key=f'die{i}') for i, die_value in enumerate(dice_values)]]
            sg.Window('Dice', dice_images_layout).Read()

            sg.popup("Score: " + str(score), title="Bunco")

            self.scores[player] += score

        self.current_round += 1


    def play_game(self):
        self.current_player = 0
        while self.current_round <= 6:
            self.play_round()

        results = "Game Over!\n"
        for player in range(self.players):
            results += "Player " + str(player+1) + " Score: " + str(self.scores[player]) + "\n"

        sg.popup(results, title="Bunco")
        
    def get_scores(self):
        return self.all_scores
        


        
def start_game():
    layout = [[sg.Text("Welcome to Bunco!", font=("Helvetica", 20))],
              [sg.Text("Enter the number of players:", font=("Helvetica", 16)), sg.InputText(key='num_players', font=("Helvetica", 16))],
              [sg.Button('Start', font=("Helvetica", 16)), sg.Button('Exit', font=("Helvetica", 16))]]

    window = sg.Window('Bunco', layout, size=(500, 200))

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


def main_menu():
    layout = [[sg.Text("Bunco Menu", font=("Helvetica", 20))],
              [sg.Button('Start Game', font=("Helvetica", 16)), sg.Button('Exit', font=("Helvetica", 16))]]

    window = sg.Window('Bunco', layout, size=(500, 200))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Start Game':
            start_game()

    window.close()


# Main program
main_menu()
