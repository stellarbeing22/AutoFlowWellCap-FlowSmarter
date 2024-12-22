import tkinter as tk
from tkinter import ttk
import math

# Initialize condition variables for red and green lights
red_blink_condition = False
green_blink_condition = False
gauge_value1 = 0  # Track the current gauge value for the first gauge
gauge_value2 = 0  # Track the current gauge value for the second gauge


def toggle_red_condition():
    """Toggle the red blink condition on and stop the green light."""
    global red_blink_condition, green_blink_condition
    red_blink_condition = not red_blink_condition
    green_blink_condition = False  # Turn off the green condition when red is blinking
    button_red.config(text="Stop Red Blinking" if red_blink_condition else "Start Red Blinking")
    button_green.config(text="Start Green Blinking")  # Reset the green button text


def toggle_green_condition():
    """Toggle the green blink condition on and stop the red light."""
    global green_blink_condition, red_blink_condition
    green_blink_condition = not green_blink_condition
    red_blink_condition = False  # Turn off the red condition when green is blinking
    button_green.config(text="Stop Green Blinking" if green_blink_condition else "Start Green Blinking")
    button_red.config(text="Start Red Blinking")  # Reset the red button text


def blink_button():
    """Blink the lights based on their individual conditions."""
    if red_blink_condition:  # Blink red light if the condition is true
        current_red_color = canvas.itemcget(red_circle_id, "fill")
        next_red_color = "red" if current_red_color == "white" else "white"
        canvas.itemconfig(red_circle_id, fill=next_red_color)

        # Change the color of the red label based on the light state
        alert_label.config(fg="red" if next_red_color == "red" else "black")
    else:
        canvas.itemconfig(red_circle_id, fill="white")  # Turn off red light when condition is False
        alert_label.config(fg="black")  # Keep the label text but reset color

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
    canvas.create_arc(20, 20, 280, 280, start=180, extent=180, style=tk.ARC, width=3, outline="black", tags="gauge")

    # Draw tick marks and measurements on the gauge
    for i in range(11):
        angle = math.radians(180 - i * 18)  # 180° to 0° in 10 steps
        x_start = 150 + 130 * math.cos(angle)
        y_start = 150 - 130 * math.sin(angle)
        x_end = 150 + 120 * math.cos(angle)
        y_end = 150 - 120 * math.sin(angle)
        canvas.create_line(x_start, y_start, x_end, y_end, width=2, tags="gauge")

        # Draw measurement labels
        label_value = i * 10
        label_x = 150 + 140 * math.cos(angle)
        label_y = 150 - 140 * math.sin(angle)
        canvas.create_text(label_x, label_y, text=str(label_value), font=("Helvetica", 10), tags="gauge")

    # Draw needle/pointer
    needle_angle = math.radians(180 - (value / 100) * 180)  # Calculate angle based on value
    needle_x = 150 + 110 * math.cos(needle_angle)
    needle_y = 150 - 110 * math.sin(needle_angle)
    canvas.create_line(150, 150, needle_x, needle_y, width=4, fill="red", tags="gauge")

    # Draw the center of the needle
    canvas.create_oval(140, 140, 160, 160, fill="black", tags="gauge")


def on_circle_click(event):
    """Handle clicks on the circular buttons."""
    print("Circle button clicked!")


# Create main window
root = tk.Tk()
root.title("Blinking Button with Pressure Gauges")

# Make the window full screen
root.attributes('-fullscreen', True)

# Create a Label for "Autoflow Well System" at the top in an attractive font
title_label = tk.Label(root, text="Autoflow Well System", font=("Helvetica", 28, "bold"), fg="#4CAF50")
title_label.pack(pady=20)
head_label = tk.Label(root, text="assistances in maintaining your well", font=("Bodoni MT Black", 28, "bold"),
                      fg="#4CAF50")
head_label.pack(pady=20)

# Create a Frame to hold the circular buttons and alert label
frame = tk.Frame(root)
frame.pack(pady=20)

# Create a Canvas widget for the circular buttons
canvas = tk.Canvas(frame, width=400, height=200, bg="white", bd=0, highlightthickness=0)
canvas.grid(row=0, column=0, padx=10)

# Draw a red circular button on the Canvas (left)
red_circle_id = canvas.create_oval(20, 20, 180, 180, fill="white", outline="black", width=2)

# Draw a green circular button on the Canvas (right)
green_circle_id = canvas.create_oval(220, 20, 380, 180, fill="white", outline="black", width=2)

# Bind click event to the circular buttons
canvas.tag_bind(red_circle_id, "<Button-1>", on_circle_click)
canvas.tag_bind(green_circle_id, "<Button-1>", on_circle_click)

# Label for red alert, positioned to the right of the red circular button
alert_label = tk.Label(frame, text="Alert", font=("Helvetica", 20), fg="black")
alert_label.grid(row=0, column=1, padx=10, sticky="w")

# Label for green tap status, positioned to the right of the green circular button
tap_label = tk.Label(frame, text="Tap Opened", font=("Helvetica", 20), fg="black")
tap_label.grid(row=0, column=2, padx=10, sticky="w")

# Create toggle buttons to switch the blinking condition on and off for red and green lights
button_red = tk.Button(root, text="Start Red Blinking", command=toggle_red_condition, width=20, height=2)
button_red.pack(pady=10)

button_green = tk.Button(root, text="Start Green Blinking", command=toggle_green_condition, width=20, height=2)
button_green.pack(pady=10)

# Create a Frame to hold both pressure gauges
gauges_frame = tk.Frame(root)
gauges_frame.pack(pady=20)

# Create labels for the gauges
label_left = tk.Label(gauges_frame, text="Depth Of Water", font=("Helvetica", 20))
label_left.grid(row=0, column=0, padx=10, sticky="e")

label_right = tk.Label(gauges_frame, text="Pressure", font=("Helvetica", 20))
label_right.grid(row=0, column=2, padx=10, sticky="w")

# Create canvases for the two pressure gauges
gauge_canvas1 = tk.Canvas(gauges_frame, width=300, height=300, bg="white", bd=0, highlightthickness=0)
gauge_canvas1.grid(row=0, column=1, padx=10)

gauge_canvas2 = tk.Canvas(gauges_frame, width=300, height=300, bg="white", bd=0, highlightthickness=0)
gauge_canvas2.grid(row=0, column=3, padx=10)

# Start the blink button function (it will only blink if the condition is true)
blink_button()

# Create and draw the pressure gauges
draw_gauge(gauge_canvas1, gauge_value1)
draw_gauge(gauge_canvas2, gauge_value2)

# Start updating the gauges
update_gauge()

# Start the main event loop
root.mainloop()