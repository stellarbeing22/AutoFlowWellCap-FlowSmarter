import tkinter as tk
import pygame

# Initialize pygame mixer for sound
pygame.mixer.init()

# Global variable to keep track of the current color (state)
current_color = "#1d1d1d"  # Initially set to inactive state (default color)

def toggle_red_button1(event):  # Pressure button
    """Toggle the red button color and play sound."""
    global current_color  # Use the global color state variable

    if current_color == "red":
        canvas.itemconfig(canvas_btn1, fill="#1d1d1d")  # Reset to default background (inactive state)
        pygame.mixer.music.stop()  # Stop the sound
        current_color = "#1d1d1d"  # Update the color state
    else:
        canvas.itemconfig(canvas_btn1, fill="red")  # Change to red (active state)
        pygame.mixer.music.load("running-stream-water-sound-239612.mp3")  # Load the sound
        pygame.mixer.music.play()  # Play the sound
        current_color = "red"  # Update the color state

# Main Window
root = tk.Tk()
root.title("Circular Button Example")
root.geometry("400x400")
root.configure(bg="#1d1d1d")

# Create Canvas
canvas = tk.Canvas(root, width=400, height=400, bg="#1d1d1d", bd=0, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Create Circular Button (Canvas Circle)
button_radius = 50  # Radius of the circular button
center_x = 200  # X coordinate of the center
center_y = 200  # Y coordinate of the center

# Draw the circle on the canvas
canvas_btn1 = canvas.create_oval(
    center_x - button_radius, center_y - button_radius,
    center_x + button_radius, center_y + button_radius,
    fill=current_color, outline="black", width=3
)

# Bind mouse click event to the circular button
canvas.tag_bind(canvas_btn1, "<Button-1>", toggle_red_button1)

# Start the main loop
root.mainloop()
