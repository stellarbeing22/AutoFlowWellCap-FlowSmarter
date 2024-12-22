import pygame
import sys
import os
import subprocess  # For running Python files
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plotting
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image

# Initialize pygame
pygame.init()

# Set up the full screen display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('GIFs Display')

# Get screen width and height
screen_width, screen_height = pygame.display.get_surface().get_size()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up font
font = pygame.font.Font(None, 30)  # Font size for text below each GIF
india_font = pygame.font.Font(None, 100)  # Font size for 'INDIA' at the top

# Load GIFs
gif_paths = ['earth.gif', 'earth.gif', 'earth.gif', 'earth.gif', 'earth.gif', 'earth.gif']  # Add the correct paths
gifs = []

def draw_text(text, x, y, font, color):
    """
    Function to render text at the given (x, y) position with the provided font and color.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def plot_average_pressure_vs_time(csv_files=["dataa.csv", "dataa.csv", "dataa.csv", "dataa.csv"]):
    data_frames = []

    # Read the CSV files and store in a list
    for file in csv_files:
        try:
            data = pd.read_csv(file)
            if data.shape[1] < 6:
                print(f"Error: {file} doesn't have enough columns.")
                return
            # Extract the pressure and time columns
            pressure = data.iloc[:, 0]  # First column (pressure)
            time = pd.to_datetime(data.iloc[:, 5], format="%Y-%m-%d %H:%M:%S")  # Fifth column (time)
            df = pd.DataFrame({'time': time, 'pressure': pressure})
            data_frames.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            return

    # Merge all the data frames on the 'time' column
    merged_data = data_frames[0]
    for df in data_frames[1:]:
        merged_data = pd.merge(merged_data, df, on='time', suffixes=( '_file' + str(len(merged_data.columns) // 2), '_file' + str(len(df.columns) // 2)))

    # Calculate the average pressure from all files
    pressure_columns = [col for col in merged_data.columns if col.startswith('pressure')]
    merged_data['average_pressure'] = merged_data[pressure_columns].mean(axis=1)

    # Plot the graph with average pressure
    plt.figure(figsize=(10, 6))
    plt.plot(merged_data['time'], merged_data['average_pressure'], label="Average Pressure")
    plt.xlabel("Time")
    plt.ylabel("Average Pressure")
    plt.title("Average Pressure vs Time")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

# Function to load GIF as a list of frames
def load_gif(path):
    gif = Image.open(path)
    frames = []

    # Extract all frames from the GIF
    while True:
        # Convert the frame to a format pygame can handle
        frame = gif.copy()
        frame = frame.convert('RGBA')
        frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))

        try:
            # Go to the next frame in the GIF
            gif.seek(gif.tell() + 1)
        except EOFError:
            break

    return frames


# Load all GIFs (each as a list of frames)
for path in gif_paths:
    if os.path.exists(path):
        gifs.append(load_gif(path))
    else:
        gifs.append(None)

# Define the grid layout for displaying the GIFs
gif_size = 150
gap = 90  # Gap between the GIFs
grid_layout = [
    (0, 0), (1, 0), (2, 0),  # First row (3 GIFs)
    (0, 1), (1, 1), (2, 1)  # Second row (3 GIFs)
]

# List of six states of India to display below each GIF
state_names = [
    "Uttarakhand", "Uttar Pradesh", "Bihar",
    "Punjab", "West Bengal", "Kerala"
]

# Corresponding Python files to run for each state
state_actions = [
    "UttarakhandHandler.py", "Uttar Pradesh Home Page.py", "Bihar Home Page.py",
    "PunjabHandler.py", "West Bengal Home Page.py", "Kerala Home Page.py",
]

# Calculate total width and height of the GIF grid
total_grid_width = 3 * gif_size + 2 * gap
total_grid_height = 2 * gif_size + 2 * gap + 30  # Including space for the text below each GIF

# Calculate offset to center the grid in the screen
offset_x = (screen_width - total_grid_width) // 2
offset_y = (screen_height - total_grid_height) // 2

# Frame rate control (frame delay in milliseconds)
frame_rate = 100  # 100 ms per frame

# Define the button area (top-left corner)
button_width, button_height = 120, 40
button_rect = pygame.Rect(10, 10, button_width, button_height)

# Main loop
running = True
frame_count = [0] * len(gifs)  # Track the current frame for each GIF
while running:
    screen.fill(black)  # Fill the screen with black

    # Render and display "INDIA" at the top center
    india_text = india_font.render('INDIA', True, white)
    india_text_rect = india_text.get_rect(center=(screen_width // 2, 50))  # Adjust position above the GIF grid
    screen.blit(india_text, india_text_rect)

    # Draw the button
    pygame.draw.rect(screen, (255, 0, 0), button_rect)  # Red button
    draw_text("📈 Plot", button_rect.centerx, button_rect.centery, font, white)

    # Display the GIFs in a 2x3 grid, centered
    for idx, gif in enumerate(gifs):
        if gif:
            # Get row and column for current GIF
            col, row = grid_layout[idx]

            # Calculate the position for the current GIF, considering the offset
            x = offset_x + col * (gif_size + gap)
            y = offset_y + row * (gif_size + gap)

            # Get the current frame
            frame = gif[frame_count[idx]]

            # Scale the frame to fit into the grid (adjust size as necessary)
            gif_scaled = pygame.transform.scale(frame, (gif_size, gif_size))

            # Display the GIF frame
            screen.blit(gif_scaled, (x, y))

            # Add text below the GIF (state names instead of GIF labels)
            state_name = state_names[idx]  # Get the state name for the current GIF
            text = font.render(state_name, True, white)
            screen.blit(text,
                        (x + (gif_size - text.get_width()) // 2, y + gif_size + 5))  # Center the text below the GIF

    # Update the display
    pygame.display.flip()

    # Update frame count for animation
    for i in range(len(gifs)):
        if gifs[i]:
            frame_count[i] = (frame_count[i] + 1) % len(gifs[i])  # Loop through the frames

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos

                # Check if the mouse click is inside the button
                if button_rect.collidepoint(mouse_x, mouse_y):
                    plot_average_pressure_vs_time()  # Display the graph

                # Check if the mouse click is inside any GIF
                for idx, (col, row) in enumerate(grid_layout):
                    x = offset_x + col * (gif_size + gap)
                    y = offset_y + row * (gif_size + gap)

                    # Check if the click is within the bounds of the GIF
                    if x <= mouse_x <= x + gif_size and y <= mouse_y <= y + gif_size:
                        # Open the corresponding Python file
                        action = state_actions[idx]

                        # Run the corresponding Python script
                        if os.path.exists(action):
                            try:
                                # Specify the full path to Python if needed
                                subprocess.run([sys.executable, action], check=True)
                            except subprocess.CalledProcessError as e:
                                print(f"Error running {action}: {e}")
                        else:
                            print(f"File {action} does not exist")

    # Control the frame rate (wait for a short time before drawing the next frame)
    pygame.time.delay(frame_rate)

# Quit pygame
pygame.quit()
sys.exit()