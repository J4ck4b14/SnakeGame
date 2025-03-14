from tkinter import *
import random

# Game constants
SCORE_HEIGHT = 80
GAME_WIDTH = 800
GAME_HEIGHT = 600 - SCORE_HEIGHT
MENU_WIDTH = 400
MENU_HEIGHT = 500
SPEED = 50
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Classes
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize snake's starting position
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create snake body
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        # Generate random coordinates for food
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        # Create food on canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Game Functions
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    # Update snake position based on direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert new head coordinates
    snake.coordinates.insert(0, (x, y))

    # Create new square for snake's head
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        score_label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food() # This line creates a new Food object
    else:
        # Remove last part of snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        death_feedback(snake, 5)
    else:
        # Schedule next turn
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    # Prevent 180-degree turns
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Check if snake has hit the boundaries
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # Check if snake has hit itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def death_feedback (snake, blinks_left):
    if blinks_left > 0:
        # Toggle the color of the snake's head
        current_color = canvas.itemcget(snake.squares[0], "fill")
        new_color = "#FF0000" if current_color == SNAKE_COLOR else SNAKE_COLOR
        canvas.itemconfig(snake.squares[0], fill = new_color)

        # Schedule the next blink
        window.after(500, death_feedback, snake, blinks_left-1)
    else:
        # Afterwards, proceed to game over screen
        game_over()

def game_over():

    canvas.delete(ALL)

    # Hide canvas and show game over frame
    canvas.pack_forget()
    game_over_frame.pack(expand=True, fill=BOTH)

    # Create Game Over label and pack it
    game_over_label = Label(game_over_frame, font=('Helvetica', 70), text="Game Over", fg="red", bg=BACKGROUND_COLOR)
    game_over_label.pack(pady=50)

    # Create retry button and pack
    retry_button = Button(game_over_frame, text="Try Again", command=restart_game,font=('Papyrus', 20), fg="#AEAEAE", bg="green")
    retry_button.pack(pady=20)

    # Create main menu button and pack
    main_menu_button = Button(game_over_frame, text="Main Menu", command=show_main_menu, font=('Papyrus', 20), fg="#AEAEAE", bg="green")
    main_menu_button.pack(pady=10)

def restart_game():
    # Hide the game over frame
    game_over_frame.pack_forget()

    # Clear the game over frame of any widgets
    for widget in game_over_frame.winfo_children():
        widget.destroy()

    # Start a new game
    start_game()

# Menu Functions
def start_game():
    # Hide the main menu
    main_menu_frame.pack_forget()
    game_over_frame.pack_forget()

    # Resize the window to match the game dimensions (this took me by surprise, honestly)
    window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT + SCORE_HEIGHT}")

    # Show the game canvas and score label
    score_label.pack()
    canvas.pack()

    # Start the game logic
    global snake, good, score, direction

    canvas.delete(ALL)

    # Create snake and food objects
    snake = Snake()
    food = Food()

    # Initialize
    score = 0
    direction = 'down'

    score_label.config(text="Score:{}".format(score))
    next_turn(snake, food)

def show_options():
    print("Options menu (WIP)")

def quit_game():
    window.quit()

def show_main_menu():
    canvas.pack_forget()
    score_label.pack_forget()
    game_over_frame.pack_forget()

    # Clear the game over frame of any widgets
    for widget in game_over_frame.winfo_children():
        widget.destroy()

    main_menu_frame.pack(expand=True, fill = BOTH)


# Set up the main window
window = Tk()
window.title("Snake Game (by Juan Abia)")
window.resizable(False, False)

# Create frames (main menu and game over)
main_menu_frame = Frame(window, bg="#0F0F0F")
game_over_frame = Frame(window, bg=BACKGROUND_COLOR)

# Create and pack a divider (so the main menu won't be at the top of the screen)
divider_label = Label(main_menu_frame, text="", fg="#0F0F0F", bg="#0F0F0F")
divider_label.pack(pady=20)

# Create and pack the title and subtitle in the main menu frame
title_label = Label(main_menu_frame, text="Snake Game", font=('Papyrus', 60), fg="green", bg="black")
title_label.pack(pady=2)

subtitle_label = Label(main_menu_frame, text="By Juan Abia Merino", font=('Papyrus', 16), fg="#AEAEAE", bg="black")
subtitle_label.pack(pady=20)

# Main menu's buttons
play_button = Button(main_menu_frame, text="Play", command=start_game,font=('Papyrus', 20), fg="#AEAEAE", bg="green")
play_button.pack(pady=10)

options_button = Button(main_menu_frame, text="Options", command=show_options,font=('Papyrus', 20), fg="#AEAEAE", bg="green")
options_button.pack(pady=10)

quit_button = Button(main_menu_frame, text="Quit", command=quit_game,font=('Papyrus', 20), fg="#AEAEAE", bg="green")
quit_button.pack(pady=10)

# Create score label and game canvas(UNPACKED)
score_label = Label(window, text="Score:0", font=('consolas', 40))
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)


# Show main menu initially
show_main_menu()

# Center the window on the screen
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{600}x{600}+{x}+{y}")

# Bind arrow keys to change direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))

# Start the Tkinter event loop
window.mainloop()