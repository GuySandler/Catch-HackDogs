import time
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

import math
import random
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# Initialize display
display = PyGameDisplay(width=128, height=128)

# Main display group
splash = displayio.Group()
display.show(splash)

# Load background
background = displayio.OnDiskBitmap("./art/FetchBG.png")
background_sprite = displayio.TileGrid(
    background,
    pixel_shader=background.pixel_shader,
    x=0,
    y=0,
)
splash.append(background_sprite)

# Load dog sprite
dog_sheet = displayio.OnDiskBitmap("./art/Dog.png")
dog_sprite = displayio.TileGrid(
    dog_sheet,
    pixel_shader=dog_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    x=(display.width - 32) // 2,
    y=display.height - 32 - 10,
)
splash.append(dog_sprite)

# Load ball sprite
ball_sheet = displayio.OnDiskBitmap("./art/Ball.png")
ball_sprite = displayio.TileGrid(
    ball_sheet,
    pixel_shader=ball_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    x=(display.width - 16) // 2,
    y=display.height - 16 - 10,
)
splash.append(ball_sprite)

# Load font
font = bitmap_font.load_font("./art/Arial-12.bdf")

# Score label
score_label = label.Label(font, text="Score: 0", color=0x000000)
score_label.x = 10
score_label.y = 10
splash.append(score_label)

# High score label
highscore_label = label.Label(font, text="Highscore: 0", color=0x000000)
highscore_label.x = 10
highscore_label.y = 25
splash.append(highscore_label)

# Initialize game variables
dog_pos = [64, 100]
dog_target = [64, 100]
dog_speed = 1

ball_pos = [64, 50]
ball_target = [64, 20]
ball_thrown = False
ball_speed = 1

score = 0
highscore = 0
running = True

# Game loop
while running:
    # Update dog position
    dx = dog_target[0] - dog_pos[0]
    dy = dog_target[1] - dog_pos[1]
    distance = math.sqrt(dx**2 + dy**2)

    if distance > dog_speed:
        dog_pos[0] += dx / distance * dog_speed
        dog_pos[1] += dy / distance * dog_speed
    else:
        dog_pos[0] = dog_target[0]
        dog_pos[1] = dog_target[1]

    # Update dog sprite position
    dog_sprite.x = int(dog_pos[0] - dog_sprite.width / 2)
    dog_sprite.y = int(dog_pos[1] - dog_sprite.height / 2)

    # Ball logic
    if ball_thrown:
        bx, by = ball_pos
        tx, ty = ball_target
        dx = tx - bx
        dy = ty - by
        ball_distance = math.sqrt(dx**2 + dy**2)

        if ball_distance > ball_speed:
            ball_pos[0] += dx / ball_distance * ball_speed
            ball_pos[1] += dy / ball_distance * ball_speed
        else:
            ball_thrown = False
            ball_pos = [64, 50]
            score += 1
            if score > highscore:
                highscore = score

    # Update ball sprite position
    ball_sprite.x = int(ball_pos[0] - ball_sprite.width / 2)
    ball_sprite.y = int(ball_pos[1] - ball_sprite.height / 2)

    # Update labels
    score_label.text = f"Score: {score}"
    highscore_label.text = f"Highscore: {highscore}"

    # Simulate throw logic (example: move ball when dog reaches it)
    if not ball_thrown and random.random() < 0.01:
        ball_thrown = True
        ball_target = [random.randint(0, 127), random.randint(0, 127)]

    # Pause briefly to control frame rate
    time.sleep(0.05)
