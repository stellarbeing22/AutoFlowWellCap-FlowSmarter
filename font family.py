import tkinter as tk
from tkinter import ttk
import math
import pygame

# Initialize pygame for sound
pygame.init()

# Load sound files
red_blink_sound = pygame.mixer.Sound("redlight.mp3")  # Replace with your red light sound file path
green_blink_sound = pygame.mixer.Sound("green_blink_sound.wav")  # Replace with your green light sound file path

# Initialize condition variables for red and green lights
gauge_value1 = 0  # Track the current gauge value for the first gauge

gauge_value2 = 0  # Track the current gauge value for the second gauge

# Initialize condition variables for red and green lights
red_blink_condition1 = False
red_blink_condition2 = False
green_blink_condition = False

def toggle_red_condition1():
    """Toggle the red blink condition on and stop the green light."""
    global red_blink_condition1, green_blink_condition
    red_blink_condition1 = not red_blink_condition1
    green_blink_condition = False  # Turn off the green condition when red is blinking
    button_red1.config(text="Stop Red Blinking" if red_blink_condition1 else "Start Red Blinking")
    button_green.config(text="Start Green Blinking")  # Reset the green button text
    if red_blink_condition1:
        red_blink_sound.play(-1)  # Play red light sound in a loop
    else:
        red_blink_sound.stop()  # Stop red light sound

def toggle_red_condition2():
    """Toggle the red blink condition on and stop the green light."""
    global red_blink_condition2, green_blink_condition
    red_blink_condition2 = not red_blink_condition2
    green_blink_condition = False  # Turn off the green condition when red is blinking
    button_red2.config(text="Stop Red Blinking" if red_blink_condition2 else "Start Red Blinking")
    button_green.config(text="Start Green Blinking")  # Reset the green button text
    if red_blink_condition2:
        red_blink_sound.play(-1)  # Play red light sound in a loop
    else:
        red_blink_sound.stop()  # Stop red light sound

def toggle_green_condition():
    """Toggle the green blink condition on and stop the red lights."""
    global green_blink_condition, red_blink_condition1, red_blink_condition2
    green_blink_condition = not green_blink_condition
    red_blink_condition1 = False  # Turn off the red conditions when green is blinking
    red_blink_condition2 = False  # Turn off the red conditions when green is blinking
    button_green.config(text="Stop Green Blinking" if green_blink_condition else "Start Green Blinking")
    button_red1.config(text="Start Red Blinking")  # Reset the red button text
    button_red2.config(text="Start Red Blinking")  # Reset the red button text
    if green_blink_condition:
        green_blink_sound.play(-1)  # Play green light sound in a loop
    else:
        green_blink_sound.stop()  # Stop green light sound

def blink_button():
    """Blink the lights based on their individual conditions."""
    if red_blink_condition1:  # Blink red light 1 if the condition is true
        current_red_color = canvas.itemcget(red_circle_id1, "fill")
        next_red_color = "red" if current_red_color == "white" else "white"
        canvas.itemconfig(red_circle_id1, fill=next_red_color)

        # Change the color of the red label based on the light state
        alert_label.config(fg="red" if next_red_color == "red" else "black")
    else:
        canvas.itemconfig(red_circle_id1, fill="white")  # Turn off red light 1 when condition is False
        alert_label.config(fg="black")  # Keep the label text but reset color

    if red_blink_condition2:  # Blink red light 2 if the condition is true
        current_red_color = canvas.itemcget(red_circle_id2, "fill")
        next_red_color = "red" if current_red_color == "white" else "white"
        canvas.itemconfig(red_circle_id2, fill=next_red_color)

        # Change the color of the red label based on the light state
        alert_label2.config(fg="red" if next_red_color == "red" else "black")
    else:
        canvas.itemconfig(red_circle_id2, fill="white")  # Turn off red light 2 when condition is False
        alert_label2.config(fg="black")  # Keep the label text but reset color

    if green_blink_condition:  # Blink green light if the condition is true
        current_green_color = canvas.itemcget(green_circle_id, "fill")
        next_green_color = "green" if current_green_color == "white" else "white"
        canvas.itemconfig(green_circle_id, fill=next_green_color)

        # Change the color of the green label based on the light state
        tap_label.config(fg="green" if next_green_color == "green" else "black")
    else:
        canvas.itemconfig(green_circle_id, fill="white")  # Turn off green light when condition is False
        tap_label.config(fg="black")  # Keep the label text but reset color

    root.after(500, blink_button)  # Call this function every 500ms to keep checking

def update_gauge():
    """Update the gauge values and redraw both pressure gauges periodically."""
    global gauge_value1, gauge_value2
    gauge_value1 = (gauge_value1 + 10) % 110  # Increment and loop back to 0 after reaching 100
    gauge_value2 = (gauge_value2 + 5) % 110  # Increment and loop back to 0 after reaching 100 (for variety)

    draw_gauge(gauge_canvas1, gauge_value1)
    draw_gauge(gauge_canvas2, gauge_value2)

    root.after(1000, update_gauge)  # Update the gauges every 1 second

def draw_gauge(canvas, value):
    """Draw a pressure gauge on the specified canvas based on the current value."""
    canvas.delete("gauge")  # Clear previous drawings

    # Draw the arc (pressure gauge dial)
    canvas.create_arc(10, 10, 190, 190, start=180, extent=180, style=tk.ARC, width=3, outline="black", tags="gauge")

    # Draw tick marks and measurements on the gauge
    for i in range(11):
        angle = math.radians(180 - i * 18)  # 180° to 0° in 10 steps
        x_start = 100 + 90 * math.cos(angle)
        y_start = 100 - 90 * math.sin(angle)
        x_end = 100 + 80 * math.cos(angle)
        y_end = 100 - 80 * math.sin(angle)
        canvas.create_line(x_start, y_start, x_end, y_end, width=2, tags="gauge")

        # Draw measurement labels
        label_value = i * 10
        label_x = 100 + 100 * math.cos(angle)
        label_y = 100 - 100 * math.sin(angle)
        canvas.create_text(label_x, label_y, text=str(label_value), font=("Helvetica", 12), tags="gauge")

        # Draw the needle (indicator)
    needle_angle = math.radians(180 - value * 1.8)  # Convert value to angle (0-100 to 180-0 degrees)
    needle_x = 100 + 70 * math.cos(needle_angle)
    needle_y = 100 - 70 * math.sin(needle_angle)
    canvas.create_line(100, 100, needle_x, needle_y, width=3, fill="red", arrow=tk.LAST, tags="gauge")

root = tk.Tk()
root.title("Pressure Gauge")
root.attributes('-fullscreen', True)

# Create a Label for "Autoflow Well System" at the top in an attractive font
title_label = tk.Label(root, text="Autoflow Well System", font=("Helvetica", 28, "bold"), fg="#4CAF50")
title_label.pack(pady=20)
head_label = tk.Label(root, text="assistances in maintaining your well", font=("Bodoni MT Black", 28, "bold"),
                      fg="#4CAF50")
head_label.pack(pady=20)
# Create a single frame to hold both gauges and buttons
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Create labels for the gauges
label_left = tk.Label(main_frame, text="Depth Of Water", font=("Helvetica", 20))
label_left.grid(row=0, column=0, padx=10, sticky="e")

label_right = tk.Label(main_frame, text="Pressure", font=("Helvetica", 20))
label_right.grid(row=0, column=2, padx=10, sticky="w")

# Create canvases for the two pressure gauges
gauge_canvas1 = tk.Canvas(main_frame, width=200, height=200, bg="white", bd=0, highlightthickness=0)
gauge_canvas1.grid(row=1, column=0, padx=10)

gauge_canvas2 = tk.Canvas(main_frame, width=200, height=200, bg="white", bd=0, highlightthickness=0)
gauge_canvas2.grid(row=1, column=2, padx=10)

# Add two new lines in between the gauges and the buttons
tk.Label(main_frame, text="").grid(row=2, column=0, columnspan=3)
tk.Label(main_frame, text="").grid(row=3, column=0, columnspan=3)

# Create a frame to hold the buttons and labels
button_frame = tk.Frame(main_frame)
button_frame.grid(row=4, column=0, columnspan=3, padx=10)

# Create toggle buttons to switch the blinking condition on and off for red and green lights
button_red1 = tk.Button(button_frame, text="Start Red Blinking", command=toggle_red_condition1, width=20, height=2)
button_red1.grid(row=0, column=0, padx=10)

button_red2 = tk.Button(button_frame, text="Start Red Blinking", command=toggle_red_condition2, width=20, height=2)
button_red2.grid(row=0, column=1, padx=10)

button_green = tk.Button(button_frame, text="Start Green Blinking", command=toggle_green_condition, width=20, height=2)
button_green.grid(row=0, column=2, padx=10)

# Create labels for the buttons
alert_label = tk.Label(button_frame, text="Depth", font=("Helvetica", 20), fg="black")
alert_label.grid(row=1, column=0, padx=10, sticky="w")

alert_label2 = tk.Label(button_frame, text="Pressure ", font=("Helvetica", 20), fg="black")
alert_label2.grid(row=1, column=1, padx=10, sticky="w")

tap_label = tk.Label(button_frame, text="Tap Opened", font=("Helvetica", 20), fg="black")
tap_label.grid(row=1, column=2, padx=10, sticky="w")

# Create a canvas for the blinking lights
canvas = tk.Canvas(button_frame, width=400, height=100, bg="white", bd=0, highlightthickness=0)
canvas.grid(row=2, column=0, columnspan=3, padx=10)

# Draw the blinking lights
red_circle_id1 = canvas.create_oval(50, 25, 100, 75, fill="white", outline="black")
red_circle_id2 = canvas.create_oval(150, 25, 200, 75, fill="white", outline="black")
green_circle_id = canvas.create_oval(250, 25, 300, 75, fill="white", outline="black")

# Start the blinking and gauge updating
blink_button()
update_gauge()

root.mainloop()