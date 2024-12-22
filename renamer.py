import os

def rename_images(directory, extension=".png"):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Filter only image files based on the extension
    image_files = [f for f in files if f.lower().endswith(extension.lower())]

    # Sort files to ensure they are renamed in order
    image_files.sort()

    # Rename each image file with a sequence number
    for i, filename in enumerate(image_files, start=1):
        # Get the full file path
        old_file_path = os.path.join(directory, filename)

        # Construct the new file name
        new_file_name = f"{i}{extension}"

        # Get the new file path
        new_file_path = os.path.join(directory, new_file_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{filename}' to '{new_file_name}'")

# Usage example
directory =r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\bird\birdd"

rename_images(directory, extension=".png")
