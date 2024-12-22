import os
from rembg import remove
from PIL import Image

# Function to process all PNG images in a folder
def remove_background_from_folder(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Open image
            with open(input_path, 'rb') as input_file:
                input_image = input_file.read()

            # Remove the background
            output_image = remove(input_image)

            # Save the result as a PNG
            with open(output_path, 'wb') as output_file:
                output_file.write(output_image)

            print(f"Processed {filename}")

# Specify input and output folders
input_folder = r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\bird\birdd"
output_folder = r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\bird\birds"

# Run the function to process the images
remove_background_from_folder(input_folder, output_folder)
