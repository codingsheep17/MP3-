# Importing required modules
import pygame as py
import sys
from mutagen.mp3 import MP3  # Used to get song duration

# Initializing Pygame and its mixer module
py.init()
py.mixer.init()

# Setting up the display and caption
screen_width = 320
screen_height = 500
screen = py.display.set_mode((screen_width, screen_height))
py.display.set_caption("Music Player")

# Loading images
bg_img = py.image.load("bg_img.png").convert()  # Background image
pause_img = py.image.load('Pause.png')          # Pause button image
play_img = py.image.load('Play.png')            # Play button image
cic_img = py.image.load("circle1.png")         # Rotating circle image
next_img = py.image.load('next.png')            # Next button image
prev_img = py.image.load('previous.png')        # Previous button image
line_img = py.image.load('line.png')            # Progress line image
dot_image = py.image.load('dot.png')            # Dot image for progress

# Button positions and rectangles
button_rect = play_img.get_rect()
button_rect.topleft = (135, 430)
cic_img_rect = cic_img.get_rect(center=(155, 135))
next_img_rect = next_img.get_rect()
next_img_rect.topleft = (225, 430)
prev_img_rect = prev_img.get_rect()
prev_img_rect.topleft = (50, 430)
line_img_rect = line_img.get_rect()
line_img_rect.topleft = (15, 360)

# Angle for rotating the circle
angle = 0

# Frames per second setting
fps = 60
clock = py.time.Clock()

# State variables
is_play = True
is_rotating = False
running = True

# Song handling variables
songs = ['Keep up.mp3', 'Aura.mp3']  # List of songs
current_song_index = 0               # Current song index

# Load and play the first song
py.mixer.music.load(songs[current_song_index])
py.mixer.music.play()

# Getting the duration of the current song using Mutagen
current_song = MP3(songs[current_song_index])
duration = current_song.info.length  # Duration in seconds

# Dot position settings
dot_y = 380  # Y-coordinate of the dot (same as the line)
dot_start_x = 35  # Leftmost position of the dot
dot_end_x = 315   # Rightmost position of the dot

#text_box function
font = py.font.SysFont("Courier New", 20)
def text(text,color, x,y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x,y])

# Game loop
while running:
    # Blit the background image
    screen.blit(bg_img, (0, 0))

    # Calculate elapsed time and progress
    elapsed_time = py.mixer.music.get_pos() / 1000  # Elapsed time in seconds
    progress_ratio = elapsed_time / duration       # Ratio of elapsed time to total duration

    # Update dot position based on progress
    dot_x = dot_start_x + (progress_ratio * (dot_end_x - dot_start_x))
    dot_x = min(max(dot_x, dot_start_x), dot_end_x)  # Keep dot within bounds

    # Handle rotating circle
    rotated_cic = py.transform.rotate(cic_img, angle)
    rotated_cic_rect = rotated_cic.get_rect(center=cic_img_rect.center)

    # Event handling
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        if event.type == py.MOUSEBUTTONDOWN:
            mouse_pos = py.mouse.get_pos()

            # Play/Pause toggle button
            if button_rect.collidepoint(mouse_pos):
                is_play = not is_play
                is_rotating = not is_rotating

            # Next song button
            if next_img_rect.collidepoint(mouse_pos):
                current_song_index += 1
                if current_song_index >= len(songs):
                    current_song_index = 0  # Loop back to the first song
                py.mixer.music.load(songs[current_song_index])
                py.mixer.music.play()

                # Update song duration and reset angle
                current_song = MP3(songs[current_song_index])
                duration = current_song.info.length
                angle = 0

            # Previous song button
            if prev_img_rect.collidepoint(mouse_pos):
                current_song_index -= 1
                if current_song_index < 0:
                    current_song_index = len(songs) - 1  # Go to the last song
                py.mixer.music.load(songs[current_song_index])
                py.mixer.music.play()

                # Update song duration and reset angle
                current_song = MP3(songs[current_song_index])
                duration = current_song.info.length
                angle = 0

    # Handle rotation and buttons
    if is_rotating:
        angle += 1.7
        angle %= 360  # Keep angle within 0-360

    if is_play:
        screen.blit(play_img, button_rect)
        py.mixer.music.pause()
    else:
        screen.blit(pause_img, button_rect)
        py.mixer.music.unpause()

    # Blit images to the screen
    screen.blit(rotated_cic, rotated_cic_rect)      # Rotating circle
    screen.blit(next_img, next_img_rect)           # Next button
    screen.blit(prev_img, prev_img_rect)           # Previous button
    screen.blit(line_img, line_img_rect.topleft)   # Line image
    screen.blit(dot_image, (dot_x - dot_image.get_width() // 2, dot_y - dot_image.get_height() // 2))  # Dot image
    text(f"""Playing: {songs[current_song_index]}""",(0, 0, 0),30,280)
    # Update the display
    clock.tick(fps)
    py.display.update()

# Quit Pygame
py.quit()
