import csv
import random
import time
from datetime import datetime


csv_file_path = "dataa.csv"  # Define the file path for the CSV


# Function to generate random values for pressure, height, and water flow
def generate_random_data():
    pressure = random.uniform(-1.0, 2.0)  # Pressure between -1.0 and 2.0
    water_flow = random.uniform(0, 100)  # Water flow between 0 and 100
    return pressure, water_flow


def pressure_to_height(pressure_bar):
    # Constants
    density_water = 1000  # in kg/m³ (density of water)
    gravity = 9.81  # in m/s² (acceleration due to gravity)
    bar_to_pa = 100000  # conversion factor from bar to pascal

    # Convert pressure from bar to pascals
    pressure_pa = pressure_bar * bar_to_pa

    # Calculate height in meters
    height = pressure_pa / (density_water * gravity)

    return height


# Function to write data to CSV
def write_data_to_csv():
    # Open the CSV file in append mode, so new data is added without overwriting the existing content
    with open(csv_file_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Generate a random data entry
        pressure, water_flow = generate_random_data()
        height = pressure_to_height(pressure)

        # Write the new data to the CSV file
        writer.writerow([pressure, height, water_flow, 10.5, 80, datetime.strptime('2024-12-14 15:30:20', "%Y-%m-%d %H:%M:%S"), "false", "true", 'true'])
        print(f"Written to CSV: Pressure={pressure}, Height={height}, Water Flow={water_flow}")


# Function to simulate data writing every 1 second
def simulate_data_writing():
    while True:
        write_data_to_csv()  # Write data to CSV
        time.sleep(1)  # Wait for 1 second before writing new data


if __name__ == "__main__":
    # Create the CSV file and add a header (if the file is empty)
    try:
        with open(csv_file_path, mode='x', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Updated header to have separate column names for each data field
            writer.writerow(["Pressure", "Height", "Flow Rate", "Water Extracted", "Battery Percentage", "Time", "Tap Opened", "Safety", "Battery Strength"])
    except FileExistsError:
        pass  # The file already exists, no need to add a header again

    # Start simulating data writing
    simulate_data_writing()
