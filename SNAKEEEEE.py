import tkinter as tk
import random


WIDTH = 400
HEIGHT = 400
SIZE = 20
SPEED = 100


direction = "Right"
snake = [(100, 100), (80, 100), (60, 100)]
food = (0, 0)
running = True
paused = False
score = 0


def change_direction(new_dir):
    global direction
    opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
    if new_dir != opposites.get(direction):
        direction = new_dir

def spawn_food():
    global food
    while True:
        x = random.randrange(0, WIDTH, SIZE)
        y = random.randrange(0, HEIGHT, SIZE)
        if (x, y) not in snake:
            food = (x, y)
            break

def draw():
    canvas.delete("all")

    for x, y in snake:
        canvas.create_rectangle(x, y, x+SIZE, y+SIZE, fill="green")

    fx, fy = food
    canvas.create_rectangle(fx, fy, fx+SIZE, fy+SIZE, fill="blue")

def update_score():
    score_label.config(text=f"Score: {score}")

def move_snake():
    global running, score

    if not running or paused:
        return

    x, y = snake[0]

    if direction == "Up":
        y -= SIZE
    elif direction == "Down":
        y += SIZE
    elif direction == "Left":
        x -= SIZE
    elif direction == "Right":
        x += SIZE

    new_head = (x, y)

    # Wall collision
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        game_over()
        return

    # Self collision
    if new_head in snake:
        game_over()
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        update_score()
        spawn_food()
    else:
        snake.pop()

    draw()
    window.after(SPEED, move_snake)

def toggle_pause():
    global paused
    paused = not paused
    pause_button.config(text="Resume" if paused else "Pause")

    if not paused:
        move_snake()

def game_over():
    global running
    running = False
    canvas.delete("all")

    canvas.create_text(
        WIDTH//2, HEIGHT//2 - 30,
        text="Game Over",
        fill="red",
        font=("Arial", 24, "bold")
    )

    replay_button.place(x=WIDTH//2 - 40, y=HEIGHT//2)

def restart_game():
    global snake, direction, running, paused, score

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "Right"
    running = True
    paused = False
    score = 0

    pause_button.config(text="Pause")
    replay_button.place_forget()
    update_score()
    spawn_food()
    draw()
    move_snake()


window = tk.Tk()
window.title("Snake Game")

score_label = tk.Label(window, text="Score: 0", font=("Arial", 12))
score_label.pack()

canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

pause_button = tk.Button(window, text="Pause", command=toggle_pause)
pause_button.pack(pady=5)

replay_button = tk.Button(window, text="Replay", command=restart_game)
replay_button.place_forget()


window.bind("w", lambda e: change_direction("Up"))
window.bind("s", lambda e: change_direction("Down"))
window.bind("a", lambda e: change_direction("Left"))
window.bind("d", lambda e: change_direction("Right"))


spawn_food()
draw()
move_snake()

window.mainloop()
