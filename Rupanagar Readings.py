import tkinter as tk
import random
import math
import pygame
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL for handling images
import csv
from tkinter import Toplevel
import subprocess
import tkinter.messagebox as messagebox
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plotting
import matplotlib.pyplot as plt

def run_second_file():
#    """Run the second file in the background."""
    subprocess.Popen(['python', 'testing2.py'])

# In your main function or at the start of your program, call this function:
#run_second_file()






def plot_pressure_vs_time(csv_file='dataa.csv'):
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(csv_file)

    # Check the shape of the DataFrame to ensure it has enough columns
    print(f"Data shape: {data.shape}")

    # Verify that the DataFrame has at least 6 columns (for pressure and time)
    if data.shape[1] < 6:
        print("Error: CSV file doesn't have enough columns.")
        return

    # Extract the pressure (index 0) and time (index 5) columns
    pressure = data.iloc[:, 0]  # First column (pressure)

    # Convert the time column (index 5) to a pandas datetime object
    time = pd.to_datetime(data.iloc[:, 5], format="%Y-%m-%d %H:%M:%S")

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(time, pressure, label="Pressure")
    plt.xlabel("Time")
    plt.ylabel("Pressure")
    plt.title("Pressure vs Time")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


# Example usage:
# plot_pressure_vs_time('data.csv')

def read_all_gauge_values(file_path):
    """Read all rows of data from the CSV file."""
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        for row in reader:
            if row:  # Only add non-empty rows
                data.append(row)
    return data
# Display all CSV data in a popup
def display_csv_data():
    # Create a new window to display CSV data
    data_window = tk.Toplevel(root)
    data_window.title("All CSV Data")
    data_window.geometry("600x400")
    data_window.configure(bg="#1d1d1d")

    # Get all the data from the CSV file
    data = read_all_gauge_values("dataa.csv")

    # Create a Text widget with a scrollbar to display the data
    text_widget = tk.Text(data_window, wrap=tk.WORD, width=70, height=15, font=("Helvetica", 12))
    text_widget.pack(pady=20)

    scrollbar = tk.Scrollbar(data_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Insert the CSV data into the Text widget
    for row in data:
        text_widget.insert(tk.END, ', '.join(row) + '\n')

    # Make the Text widget read-only
    text_widget.config(state=tk.DISABLED)


# Function to simulate flying birds (creatures) animation
def create_flying_bird(canvas, root_width, root_height):
    """Create and animate a flying bird that moves across the entire screen."""
    # Initial position (start outside the canvas)
    start_x = random.choice([-50, root_width + 50])  # Randomly start on the left or right side
    start_y = random.randint(50, root_height - 50)  # Random Y position for variety
    folder = "bird/birds/"
    # Load the bird images (replace with your image file names)
    bird_images = []

    # Loop through image indices (assuming image names are sequential like 0.png, 1.png, ...)
    for i in range(1,19):  # For 0.png to 6.png
        img_path = f"{folder}{i}.png"
        bird_images.append(Image.open(img_path))

    # Resize each bird image to a smaller size (e.g., 50x50 pixels)
    bird_images_resized = [bird.resize((50, 50)) for bird in bird_images]  # Resize to 50x50

    # Convert images to PhotoImage objects for Tkinter
    bird_photos = [ImageTk.PhotoImage(bird) for bird in bird_images_resized]

    # Create an image item for the bird on the canvas (initially use the first image)
    bird = canvas.create_image(start_x, start_y, image=bird_photos[0], tags="bird")

    # Save a reference to the image objects (Tkinter requires this to keep them in memory)
    canvas.image_refs = bird_photos

    # Random flight direction and speed (moving to the left or right)
    end_x = random.randint(0, root_width)  # Random position where bird will fly
    end_y = random.randint(50, root_height - 50)
    flight_time = random.randint(4000, 6000)  # Flight time between 4-6 seconds

    # Counter to switch images
    image_index = 0

    # Function to change the bird image (frame-by-frame animation)
    def switch_bird_image():
        nonlocal image_index
        image_index = (image_index + 1) % len(bird_photos)  # Cycle through the images
        canvas.itemconfig(bird, image=bird_photos[image_index])  # Update the image on canvas
        canvas.after(100, switch_bird_image)  # Repeat every 100ms for smooth animation

    # Animation function to move the bird
    def move_bird():
        # Animate the bird moving across the screen
        canvas.move(bird, (end_x - start_x) / flight_time * 50, (end_y - start_y) / flight_time * 50)  # Adjust speed
        # Continue the movement until the bird reaches its destination
        if abs(canvas.coords(bird)[0] - end_x) > 1 and abs(canvas.coords(bird)[1] - end_y) > 1:
            canvas.after(50, move_bird)
        else:
            # Fade out the bird by gradually removing it after some time
            fade_out_bird()

    # Function to fade out the bird (simulated by removing the bird after some time)
    def fade_out_bird():
        current_opacity = 1

        def reduce_opacity():
            nonlocal current_opacity
            if current_opacity > 0:
                current_opacity -= 0.05  # Reduce opacity
                canvas.after(50, reduce_opacity)  # Keep reducing opacity
            else:
                canvas.delete(bird)  # Remove the bird after it fades

        reduce_opacity()

    # Start switching bird images and moving the bird after a short delay
    canvas.after(1000, switch_bird_image)  # Start the image switching animation
    canvas.after(1000, move_bird)  # Start moving the bird after 1 second

    # Ensure bird is on top after creation and movement
    canvas.tag_raise("bird")  # This makes sure the bird stays above all other items


# Function to create birds every 5-6 seconds
def start_bird_animation(canvas, root_width, root_height):
    create_flying_bird(canvas, root_width, root_height)
    canvas.after(random.randint(5000, 6000), lambda: start_bird_animation(canvas, root_width, root_height))
def blink_status5():
    """Function to make the status5 label blink (appear and disappear)."""
    if status5.winfo_ismapped():  # Check if the label is currently visible
        status5.grid_forget()  # Hide the label
    else:
        status5.grid(row=17, column=0, pady=50)  # Show the label again using grid
    root.after(1000, blink_status5)  # Repeat every 500ms for the blinking effect


# Function to draw the gauge on the canvas (remains unchanged)
def draw_gauge(canvas, value, label_color, tag, reading_color="white"):
    """Draw a gauge with the current value and change the reading's color."""
    canvas.delete(tag)  # Clear previous drawings

    # Draw the arc (gauge dial)
    canvas.create_arc(10, 10, 190, 190, start=180, extent=180, style=tk.ARC, width=3, outline="black", tags=tag)

    # Draw tick marks and measurements on the gauge
    for i in range(11):
        angle = math.radians(180 - i * 18)  # 180° to 0° in 10 steps
        x_start = 100 + 90 * math.cos(angle)
        y_start = 100 - 90 * math.sin(angle)
        x_end = 100 + 80 * math.cos(angle)
        y_end = 100 - 80 * math.sin(angle)
        canvas.create_line(x_start, y_start, x_end, y_end, width=2, tags=tag)

        # Draw measurement labels with the color specified
        label_value = i * 10
        label_x = 100 + 100 * math.cos(angle)
        label_y = 100 - 100 * math.sin(angle)
        canvas.create_text(label_x, label_y, text=str(label_value), font=("Helvetica", 12), fill=reading_color, tags=tag)

    # Draw the needle (indicator)
    needle_angle = math.radians(180 - value * 1.8)  # Convert value to angle (0-100 to 180-0 degrees)
    needle_x = 100 + 70 * math.cos(needle_angle)
    needle_y = 100 - 70 * math.sin(needle_angle)
    canvas.create_line(100, 100, needle_x, needle_y, width=3, fill=label_color, arrow=tk.LAST, tags=tag)





def draw_gauge_for_pressure(canvas, value, label_color, tag, reading_color="white"):
    """Draw a gauge with the current value and change the reading's color."""
    canvas.delete(tag)  # Clear previous drawings

    # Draw the arc (gauge dial)
    canvas.create_arc(10, 10, 190, 190, start=180, extent=180, style=tk.ARC, width=3, outline="black", tags=tag)

    # Draw tick marks and measurements on the gauge
    for i in range(11):
        angle = math.radians(180 - i * 18)  # 180° to 0° in 10 steps
        x_start = 100 + 90 * math.cos(angle)
        y_start = 100 - 90 * math.sin(angle)
        x_end = 100 + 80 * math.cos(angle)
        y_end = 100 - 80 * math.sin(angle)
        canvas.create_line(x_start, y_start, x_end, y_end, width=2, tags=tag)

        # Draw measurement labels with the color specified (scale 0-10)
        label_value = i  # 0-10 scale now
        label_x = 100 + 100 * math.cos(angle)
        label_y = 100 - 100 * math.sin(angle)
        canvas.create_text(label_x, label_y, text=str(label_value), font=("Helvetica", 12), fill=reading_color,
                           tags=tag)

    # Map value (0-10) to an angle (0-180 degrees)
    needle_angle = math.radians(180 - value * 18)  # Convert value to angle (0-10 to 180-0 degrees)

    # Draw the needle (indicator)
    needle_x = 100 + 70 * math.cos(needle_angle)
    needle_y = 100 - 70 * math.sin(needle_angle)
    canvas.create_line(100, 100, needle_x, needle_y, width=3, fill=label_color, arrow=tk.LAST, tags=tag)


def blink_button():
    """Function to toggle the button color to create a blinking effect."""
    current_color = blink_btn.cget("bg")
    new_color = "red" if current_color == "#8b0000" else "#8b0000"
    blink_btn.config(bg=new_color)
    root.after(500, blink_button)  # Repeat every 500ms


def blink_buttongreen():
    """Function to toggle the button color to create a blinking effect."""
    current_color = blink_btngreen.cget("bg")
    new_color = "green" if current_color == "#90ee90" else "#90ee90"
    blink_btngreen.config(bg=new_color)
    root.after(500, blink_button)



current_color = "#8b0000"
def toggle_red_button1():  # Pressure button
    """Toggle the red button color and play sound."""
    global current_color  # Use the global color state variable

    if current_color == "red":
        canvas.itemconfig(canvas_btn1, fill="#8b0000")  # Reset to default background (inactive state)
        pygame.mixer.music.stop()  # Stop the sound
        current_color = "#1d1d1d"  # Update the color state
    else:
        canvas.itemconfig(canvas_btn1, fill="red")  # Change to red (active state)
        pygame.mixer.music.load("pressure_alarm.mp3")  # Load the sound
        pygame.mixer.music.play()  # Play the sound
        current_color = "red"  # Update the color state# Play the sound
current_color2='#90ee90'

def toggle_green_button():  # Add 'event' as an argument
    """Toggle the green button color and play sound."""
    global current_color2  # Use the global color state variable

    if current_color2 == "green":
        canvas2.itemconfig(canvas_btn2, fill="#90ee90")  # Reset to default background (inactive state)
        pygame.mixer.music.stop()  # Stop the sound
        current_color2 = "90ee90"  # Update the color state
    else:
        canvas2.itemconfig(canvas_btn2, fill="green")  # Change to green (active state)
        pygame.mixer.music.load("running-stream-water-sound-239612.mp3")  # Load the sound
        pygame.mixer.music.play()  # Play the sound
        current_color2 = "green"  # Update the color state


  # Play green sound


# Initialize pygame mixer for sound
pygame.mixer.init()

# Main Application
root = tk.Tk()
root.title("Autoflow Well System")

# Set the window to fullscreen
root.attributes("-fullscreen", True)  # Set the window to fullscreen
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))  # Allow exiting fullscreen mode with Escape

root.configure(bg="#1d1d1d")

# Create a canvas that spans the entire screen as the background (ensure it's behind other widgets)
root_width = root.winfo_screenwidth()
root_height = root.winfo_screenheight()
full_screen_canvas = tk.Canvas(root, width=root_width, height=root_height, bg="#1d1d1d", highlightthickness=0)
full_screen_canvas.place(x=0, y=0)
start_bird_animation(full_screen_canvas, root_width, root_height)
# Header section (this will now appear on top of the canvas)
def battery_display(file_path='dataa.csv'):
    """Function to extract battery percentage from the CSV file."""
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        last_row = None
        for row in reader:
            last_row = row  # Keep the latest row

        # Check if the last row has enough elements to extract battery data
        if last_row and len(last_row) > 4:  # Ensure there are enough columns to extract battery percentage
            try:
                batteryd = float(last_row[4])  # Battery percentage is in the 5th column (index 4)
            except ValueError:
                batteryd = 0  # In case the value is invalid or not a number
        else:
            batteryd = 0  # Default value if data is missing or malformed

        return batteryd

header = tk.Label(root, text=f"{battery_display()}%🔋                                                                           Autoflow Well                                                                                            ", font=("Bernard MT Condensed", 24, "bold"), fg="black", bg="#4CAF50")
header.pack(fill="x", pady=10)

# Status label (this will also appear above the canvas)
status_label = tk.Label(root, text="Active", font=("Helvetica", 14), fg="gray", bg="#1d1d1d")
status_label.pack(pady=(0, 20))

# Gauges frame (this will appear above the canvas)
gauges_frame = tk.Frame(root, bg="#1d1d1d")
gauges_frame.pack(pady=10)

# Water level gauge
water_canvas = tk.Canvas(gauges_frame, width=200, height=200, bg="#1d1d1d", highlightthickness=0)
water_canvas.grid(row=0, column=0, padx=20)
statush = tk.Label(gauges_frame, text="", font=("Helvetica", 12), fg="gray", bg="#1d1d1d")
statush.grid(row=0, column=0, pady=0)
tk.Label(gauges_frame, text="Expected Height", font=("Helvetica", 16), fg="blue", bg="#1d1d1d").grid(row=1, column=0, pady=5)

# Pressure gauge
pressure_canvas = tk.Canvas(gauges_frame, width=220, height=220, bg="#1d1d1d", highlightthickness=0)
pressure_canvas.grid(row=0, column=1, padx=20)

tk.Label(gauges_frame, text="Pressure Level", font=("Helvetica", 16), fg="orange", bg="#1d1d1d").grid(row=1, column=1, pady=5)

# Status indicators frame (this will appear above the canvas)
status_frame = tk.Frame(root, bg="#1d1d1d")
status_frame.pack(pady=10)
status1 = tk.Label(gauges_frame, text="", font=("Helvetica", 12), fg="gray", bg="#1d1d1d")
status1.grid(row=0, column=1, pady=5)



status2 = tk.Label(status_frame, text="Pressure limit reached", font=("Helvetica", 12), fg="gray", bg="#1d1d1d")
status2.grid(row=2, column=0, padx=50)



# Blinking Button (this will appear above the canvas)
canvas = tk.Canvas(status_frame, width=130, height=140, bg="#1d1d1d", bd=0, highlightthickness=0)
canvas.grid(row=3, column=0, pady=0)

# Create Circular Button (Canvas Circle)
button_radius = 26  # Radius of the circular button
center_x = 70  # X coordinate of the center
center_y = 40  # Y coordinate of the center

# Draw the circle on the canvas (no text, no border)
canvas_btn1 = canvas.create_oval(
    center_x - button_radius, center_y - button_radius,
    center_x + button_radius, center_y + button_radius,
    fill=current_color, outline="#1d1d1d", width=3
)

# Bind mouse click event to the circular button
#canvas.tag_bind(canvas_btn1, "<Button-1>", toggle_red_button1)
status3 = tk.Label(status_frame, text="Tap is opened", font=("Helvetica", 12), fg="gray", bg="#1d1d1d")
status3.grid(row=2, column=1, padx=50)
# Green blinking button (this will appear above the canvas)
canvas2 = tk.Canvas(status_frame, width=130, height=130, bg="#1d1d1d", bd=0, highlightthickness=0)
canvas2.grid(row=3, column=1, pady=0)
button_radius1 = 26  # Radius of the circular button
center_x1 = 70  # X coordinate of the center
center_y1 = 40
# Draw the circle on the canvas (no text, no border)
canvas_btn2 = canvas2.create_oval(
    center_x1 - button_radius1, center_y1 - button_radius1,
    center_x1 + button_radius1, center_y1 + button_radius1,
    fill=current_color2, outline="#1d1d1d", width=3
)

# Bind mouse click event to the circular button
#canvas2.tag_bind(canvas_btn2, "<Button-1>", toggle_green_button)

# Flow rate gauge (this will appear above the canvas)
flow_rate_frame = tk.Frame(root, bg="#1d1d1d")
flow_rate_frame.pack(pady=0)

flow_canvas = tk.Canvas(flow_rate_frame, width=200, height=200, bg="#1d1d1d", highlightthickness=0)
flow_canvas.grid(row=5, column=0, padx=70)

tk.Label(flow_rate_frame, text="Water Flow Rate", font=("Helvetica", 16), fg="green", bg="#1d1d1d").grid(
    row=6, column=0, pady=5
)
statusw = tk.Label(flow_rate_frame, text="", font=("Helvetica", 12), fg="gray", bg="#1d1d1d")
statusw.grid(row=5, column=0, padx=40)
status4 = tk.Label(flow_rate_frame, text="Water Extracted", font=("Helvetica", 12), fg="gray", bg="#1d1d1d")
status4.grid(row=10, column=0, pady=5)
status5 = tk.Label(flow_rate_frame, text="", font=("Sitka Text Semibold", 30), fg="red", bg="#1d1d1d")
status5.grid(row=1, column=0, pady=0)
# CSV data button in top-right corner
csv_button = tk.Button(root, text="Download", font=("Helvetica", 14), bg="#4CAF50", fg="black", command=display_csv_data)
csv_button.place(x=root_width - 100, y=10, anchor="ne")
graph_button = tk.Button(root, text="📈", font=("Helvetica", 14), bg="#4CAF50", fg="black", command=plot_pressure_vs_time)
graph_button.place(x=root_width -60, y=10, anchor="ne")
area = tk.Label(root, text="(Rupanagr)", font=("Helvetica", 14,'bold'), bg="#4CAF50", fg="black")
area.place(x=root_width//2+299, y=20, anchor="ne")


def read_latest_gauge_values(file_path):
    """Read the latest values for the gauges from the CSV file."""
    def show_popup():
        # Show a simple information popup
        if pressure_level > 6.0 or pressure_level < 0:
            messagebox.showinfo("Warning", "Abnormal Value of Pressure Detected!")
        elif flow_rate > 100 or flow_rate < 0:
            messagebox.showinfo("Warning", "Abnormal Value of Flow Rate!")
        elif last_row[8].strip().lower() == 'false':
            messagebox.showinfo("Warning", "Abnormal Value of Battery Detected!")
        else:
            pass
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Skip the header if present
        next(reader, None)
        last_row = None
        for row in reader:
            last_row = row  # Keep the latest row
        # Extract the values from the last row
        if last_row:  # Ensure there's data
            pressure_level= float(last_row[0])
            water_level = float(last_row[1])
            flow_rate = float(last_row[2])
            water_extracted = float(last_row[3])
            #index5 has timing
            if last_row[6].strip().lower() == 'true':  # Check if 4th index is 'True'
                toggle_green_button()
            if last_row[7].strip().lower() == 'true':  # Check if 4th index is 'True'
                status5.config(text="Someone is inspecting the cap!")
            show_popup()
            return  pressure_level,water_level, flow_rate,water_extracted
        else:
            # Return default values if the file is empty or malformed
            return 0, 0, 0



blink_status5()
def update_gauges():
    # Read values from the CSV file
    pressure_level,water_level, flow_rate,water_extracted = read_latest_gauge_values("dataa.csv")

    # Update the gauges with values from CSV
    draw_gauge(water_canvas, water_level, "blue", "water_gauge")
    draw_gauge_for_pressure(pressure_canvas, pressure_level, "orange", "pressure_gauge")
    draw_gauge(flow_canvas, flow_rate, "green", "flow_gauge")
    status1.config(text=f"{pressure_level:.4f} bar")
    statush.config(text=f"{water_level:.4f} m")
    statusw.config(text=f"{flow_rate:.2f} L/min")
    status4.config(text=f"Water Extracted: {water_extracted:.2f} L")

    if pressure_level > 1.8:
        toggle_red_button1()



    # Update the gauges every 2 seconds (you can adjust the interval)
    root.after(2000, update_gauges)






# Start the bird animation across the full screen
# Start updating gauges from CSV
update_gauges()


# Start the main loop
root.mainloop()
