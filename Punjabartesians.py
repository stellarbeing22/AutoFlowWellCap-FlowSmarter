import pygame
import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plotting
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize pygame
pygame.init()

# Constants
BACKGROUND_COLOR = (0, 0, 0)  # Black color
TEXT_COLOR = (255, 255, 255)  # White color
FONT_SIZE = 32
TITLE = "Punjab"

# Image files with their customized names and corresponding python scripts
images = [
    (r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\artesianwell.jpg", "Gurdaspur", r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\Gurdaspur Readings.py"),
    (r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\artesianwell.jpg", "Hoshiarpur", "Hoshiarpur Readings.py"),
    (r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\artesianwell.jpg", "Rupanagar", "Rupanagar Readings.py"),
    (r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\artesianwell.jpg", "Custom Name 4", "autoflow2.py"),
    (r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\artesianwell.jpg", "Custom Name 5", "autoflow2.py"),
    (r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\artesianwell.jpg", "Custom Name 6", "autoflow2.py")
]

# Get screen size for full-screen mode
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Initialize the screen in full-screen mode
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Punjab")

# Load fonts
font = pygame.font.SysFont("Engravers MT", FONT_SIZE)

# Calculate dynamic image size
IMAGE_SIZE = min(WIDTH, HEIGHT) // 6  # 6 Images per screen width/height
MARGIN = 90  # Margin between images


# Function to plot the graph
def plot_average_pressure_vs_time(csv_file1="dataa.csv", csv_file2='dataa.csv'):
    # Read the two CSV files into pandas DataFrames
    data1 = pd.read_csv(csv_file1)
    data2 = pd.read_csv(csv_file2)

    # Check the shapes of the data to ensure they have enough columns
    if data1.shape[1] < 6 or data2.shape[1] < 6:
        print("Error: CSV files don't have enough columns.")
        return

    # Extract the pressure (index 0) and time (index 5) columns from both DataFrames
    pressure1 = data1.iloc[:, 0]  # First column (pressure) from the first file
    time1 = pd.to_datetime(data1.iloc[:, 5], format="%Y-%m-%d %H:%M:%S")  # Fifth column (time) from the first file

    pressure2 = data2.iloc[:, 0]  # First column (pressure) from the second file
    time2 = pd.to_datetime(data2.iloc[:, 5], format="%Y-%m-%d %H:%M:%S")  # Fifth column (time) from the second file

    # Align the times between the two datasets (optional, depending on the time format)
    # For simplicity, we'll just merge the data from both files on time
    df1 = pd.DataFrame({'time': time1, 'pressure': pressure1})
    df2 = pd.DataFrame({'time': time2, 'pressure': pressure2})

    # Merge the two DataFrames on time
    merged_data = pd.merge(df1, df2, on='time', suffixes=('_file1', '_file2'))

    # Calculate the average pressure
    merged_data['average_pressure'] = (merged_data['pressure_file1'] + merged_data['pressure_file2']) / 2

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


# Function to draw text
def draw_text(text, x, y, font, color):
    label = font.render(text, True, color)
    screen.blit(label, (x - label.get_width() // 2, y))


# Function to load images
def load_images():
    loaded_images = []
    for image_file, _, _ in images:
        img = pygame.image.load(image_file)
        img = pygame.transform.scale(img, (IMAGE_SIZE, IMAGE_SIZE))  # Scale image to IMAGE_SIZE
        loaded_images.append(img)
    return loaded_images


# Function to run a Python script
def run_script(script_name):
    try:
        # Ensure the script_name contains the full path
        os.system(f"python \"{script_name}\"")
    except Exception as e:
        print(f"Error running {script_name}: {e}")



# Function to check if a click is within an image
def is_within_image(x, y, rect):
    return rect.collidepoint(x, y)


# Main game loop
def main():
    # Load images
    loaded_images = load_images()

    # Calculate positions for images in full screen
    image_x = (WIDTH - 3 * IMAGE_SIZE - 2 * MARGIN) // 2
    image_y = (HEIGHT - 2 * IMAGE_SIZE - MARGIN) // 2

    # Define the button area (top-left corner)
    button_width, button_height = 100, 40
    button_rect = pygame.Rect(10, 10, button_width, button_height)

    # Run the game loop
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        FONT_SIZE1=40
        font1 = pygame.font.SysFont("Showcard Gothic", FONT_SIZE1)

        # Draw the title at the top-center
        draw_text(TITLE, WIDTH // 2, 30,font1,  TEXT_COLOR)

        # Draw the button
        pygame.draw.rect(screen, (255, 0, 0), button_rect)  # Red button
        draw_text("📈", button_rect.centerx, button_rect.centery, font, TEXT_COLOR)

        # Draw images and labels
        for i, (image, img_name, _) in enumerate(images):
            row = i // 3
            col = i % 3
            x = image_x + col * (IMAGE_SIZE + MARGIN)
            y = image_y + row * (IMAGE_SIZE + MARGIN)

            # Draw the image
            screen.blit(loaded_images[i], (x, y))

            # Draw the customized image name below the image
            draw_text(img_name, x + IMAGE_SIZE // 2, y + IMAGE_SIZE + 20, font, TEXT_COLOR)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse click
                    mx, my = event.pos
                    # Check if the button is clicked
                    if button_rect.collidepoint(mx, my):
                        plot_average_pressure_vs_time()  # Call the plot function
                    # Check if any image is clicked
                    for i, (_, _, script_name) in enumerate(images):
                        row = i // 3
                        col = i % 3
                        x = image_x + col * (IMAGE_SIZE + MARGIN)
                        y = image_y + row * (IMAGE_SIZE + MARGIN)
                        rect = pygame.Rect(x, y, IMAGE_SIZE, IMAGE_SIZE)
                        if is_within_image(mx, my, rect):
                            run_script(script_name)
                            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
