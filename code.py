import pygame
import pygame_gui
import time
import webbrowser

"""
This program allows you to easily visualize the difference in speeds when overcoming an equal distance.
The colors of the "devices" (balls) are set on line 20 (in rgb).
The initial speeds of the balls in the simulation are set on line 23 in km/h, but can be easily changed in the interface of the running program.
It is not recommended to change everything else, but the sizes of windows can be changed in a small range without affecting the performance of the program.
When you run the program, you will see 4 fields for entering the speeds of each of the balls and the "Restart" button. This button restarts the simulation with the new speeds. The button must be pressed twice!
The distance bar is calculated so that the ball with the lowest speed overcomes the path in exactly 60 seconds.
Made by Gleb Ischenko (DilerFeed) in 2023 – https://github.com/DilerFeed
"""

# Initializing Pygame
pygame.init()

# Colors for devices
COLORS = [(255, 0, 0), (0, 255, 0), (0, 191, 255), (255, 255, 0)]

# Device speeds (in km/h)
speeds = [50, 70, 30, 90]

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Creating of window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualization of the speed difference. \u00A9 Gleb Ischenko")

# Distance bar options
start_mark = 50  # Offset from the left edge of the screen
end_mark = WIDTH - 50  # Offset from the right edge of the screen
num_marks = 5  # Number of marks
step = ((min(speeds) / 60) * 1000) / (num_marks - 1)  # Step between marks
start = 0   # Start value (in meters)
end = step * 4  # End value (in meters)
pixel_cost = (WIDTH - 100) / end    # Price per pixel in meters

# Draw distance bar
for i in range(num_marks):
    x = start_mark + i * ((WIDTH - 100) / 4)
    pygame.draw.line(window, (0, 0, 0), (x, HEIGHT - 20), (x, HEIGHT - 10))
    text = str(int(i * step)) + " m"
    font = pygame.font.Font(None, 20)
    text_surface = font.render(text, True, (0, 0, 0))
    window.blit(text_surface, (x - 10, HEIGHT - 35))

# Device options
device_radius = 20
device_distance = 50
device_positions = [HEIGHT - device_radius - 50,
                    HEIGHT - device_radius - 50 - device_distance,
                    HEIGHT - device_radius - 50 - 2 * device_distance,
                    HEIGHT - device_radius - 50 - 3 * device_distance]

# Draw devices
devices = []
for i in range(len(speeds)):
    device = pygame.draw.circle(window, COLORS[i], (start_mark, device_positions[i]), device_radius)
    devices.append(device)

pygame.display.flip()

# Create interface manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

def show_instructions():
    # Window cleaning
    window.fill((255, 255, 255))

    # Display text with instructions
    instructions = [
        "Instructions for using the program:",
        "- Enter speeds for each device in the input fields.",
        '- Click the "Restart" button to run the simulation with the new speeds. The button must be pressed twice!',
        "- Devices will move along the distance scale, displaying the current speed and time.",
        "- When devices reach the end of the path, their arrival time will be displayed.",
        "- The colors of the circles can be adjusted on line 20 of the code in rgb .",
        '- You can also configure the initial speeds of the "devices"; to do this, change the "speeds" list.',
        "Press any button on the keyboard to return to the simulation."
    ]

    font = pygame.font.Font(None, 22)
    line_height = 25
    y = 50

    for instruction in instructions:
        text = font.render(instruction, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.topleft = (10, y)
        window.blit(text, text_rect)
        y += line_height

    pygame.display.flip()
    
    # Wait for a key press
    global is_running
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                is_running = False
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_author_info():
    # Window cleaning
    window.fill((255, 255, 255))

    # Display information about the author
    author_info = [
        "Author: Gleb Ischenko (DilerFeed)",
        "GitHub: https://github.com/DilerFeed",
        "Press any button on the keyboard to return to the simulation.",
        "Click here with the LMB to open the author's GitHub in the browser."
    ]

    font = pygame.font.Font(None, 25)
    line_height = 25
    y = 50
    
    # Store the URL and its rect for mouse click detection
    url = "https://github.com/DilerFeed"

    for info in author_info:
        text = font.render(info, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.topleft = (10, y)
        window.blit(text, text_rect)
        y += line_height

    pygame.display.flip()
    
    # Wait for a key press
    global is_running
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                is_running = False
            elif event.type == pygame.KEYDOWN:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                # Check if the mouse click is within the URL rect
                if text_rect.collidepoint(event.pos):
                    webbrowser.open(url)  # Open the URL in the default web browser

# Create input fields
input_rects = []
input_boxes = []
for i in range(len(speeds)):
    rect = pygame.Rect(start_mark + 120, i * 50 + 10, 150, 30)
    input_rects.append(rect)
    input_box = pygame_gui.elements.UITextEntryLine(relative_rect=rect, manager=manager)
    input_box.set_allowed_characters('numbers')
    input_boxes.append(input_box)

# Create a "Restart" button
restart_button_rect = pygame.Rect(start_mark + 120, len(speeds) * 50 + 20, 150, 30)
restart_button = pygame_gui.elements.UIButton(relative_rect=restart_button_rect, text="Restart", manager=manager)

# Create instruction button
instruction_button_rect = pygame.Rect(WIDTH - 260, 10, 140, 30)
instruction_button = pygame_gui.elements.UIButton(relative_rect=instruction_button_rect, text="Instructions", manager=manager)

# Create author button
author_button_rect = pygame.Rect(WIDTH - 110, 10, 100, 30)
author_button = pygame_gui.elements.UIButton(relative_rect=author_button_rect, text="Author", manager=manager)

# Animation of movement of devices
is_running = True
start_time = time.time()
elapsed_times = [0] * len(speeds)  # List to store the elapsed time of each ball
final_times = [None] * len(speeds)  # List to store the final travel times

while is_running:
    current_time = time.time()
    elapsed_time = current_time - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Handling pygame_gui interface events
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_button:
                    new_speeds = []
                    for input_box in input_boxes:
                        speed = input_box.get_text()
                        if speed.isdigit() and int(speed) > 0:
                            new_speeds.append(int(speed))
                        else:
                            break
                    else:
                        speeds = new_speeds.copy()
                        elapsed_times = [0] * len(speeds)
                        final_times = [None] * len(speeds)
                        start_time = current_time
                    # Draw devices
                    devices = []
                    for i in range(len(speeds)):
                        device = pygame.draw.circle(window, COLORS[i], (start_mark, device_positions[i]), device_radius)
                        devices.append(device)
                elif event.ui_element == instruction_button:
                    show_instructions()
                elif event.ui_element == author_button:
                    show_author_info()

        manager.process_events(event)

    # Update pygame_gui interface
    manager.update(elapsed_time)

    window.fill((255, 255, 255))

    step = ((min(speeds) / 60) * 1000) / (num_marks - 1)  # Step between marks
    end = step * 4
    pixel_cost = (WIDTH - 100) / end
    
    # Draw distance bar
    for i in range(num_marks):
        x = start_mark + i * ((WIDTH - 100) / 4)
        pygame.draw.line(window, (0, 0, 0), (x, HEIGHT - 20), (x, HEIGHT - 10))
        text = str(int(i * step)) + " m"
        font = pygame.font.Font(None, 20)
        text_surface = font.render(text, True, (0, 0, 0))
        window.blit(text_surface, (x - 10, HEIGHT - 35))

    # Draw devices and text
    for i in range(len(speeds)):
        distance = (speeds[i] / 3600) * elapsed_times[i] * 1000  # Distance traveled (in meters)
        if distance <= end:
            device = devices[i]
            new_x = start_mark + (distance * pixel_cost)
            new_y = device.y
            pygame.draw.circle(window, COLORS[i], (new_x, new_y), device_radius)

            # Display the speed inside the ball
            speed_text = str(speeds[i]) + " km/h"
            font = pygame.font.Font(None, 16)
            speed_surface = font.render(speed_text, True, (0, 0, 0))
            window.blit(speed_surface, (new_x - device_radius, new_y))

            # Display the current time of the ball
            time_text = "{:.2f} sec".format(elapsed_times[i])
            font = pygame.font.Font(None, 16)
            time_surface = font.render(time_text, True, (0, 0, 0))
            window.blit(time_surface, (new_x - device_radius - 60, new_y - device_radius))

            elapsed_times[i] = elapsed_time  # Update ball elapsed time

        # Check if the ball has reached the end of the path, but has not yet stopped
        elif distance <= end + device_radius + (((speeds[i] / 3600) * 1000) / 60):
            device = devices[i]
            new_x = end_mark
            new_y = device.y
            pygame.draw.circle(window, COLORS[i], (new_x, new_y), device_radius)

            # Display the speed inside the ball
            speed_text = str(speeds[i]) + " km/h"
            font = pygame.font.Font(None, 16)
            speed_surface = font.render(speed_text, True, (0, 0, 0))
            window.blit(speed_surface, (new_x - device_radius, new_y))

            # Display the final time of the ball
            if final_times[i] is None:
                final_times[i] = elapsed_times[i]
            time_text = "{:.2f} sec".format(final_times[i])
            font = pygame.font.Font(None, 16)
            time_surface = font.render(time_text, True, (0, 0, 0))
            window.blit(time_surface, (new_x - device_radius - 60, new_y - device_radius))

    # Rendering the pygame_gui interface
    manager.draw_ui(window)

    pygame.display.flip()

# Program termination
pygame.quit()
