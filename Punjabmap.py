import pygame
import cv2
import moviepy.editor as mp
import time

# Initialize Pygame
pygame.init()

# Set up the Pygame screen in full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Load video using OpenCV
video_path = r"Punjabmap.mp4"  # Change to your video file path
cap = cv2.VideoCapture(video_path)

# Check if the video file was opened correctly
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per second of the video
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Get screen size
screen_width, screen_height = pygame.display.get_surface().get_size()

# Calculate the scaling factors while maintaining the aspect ratio
scale_factor_width = screen_width / video_width
scale_factor_height = screen_height / video_height
scale_factor = min(scale_factor_width, scale_factor_height)  # Use the smaller factor to maintain aspect ratio

# Calculate the new video dimensions
new_video_width = int(video_width * scale_factor + 900)
new_video_height = int(video_height * scale_factor + 45)

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# Extract the audio from the video and start playback
clip = mp.VideoFileClip(video_path)
audio = clip.audio
audio_file = r"C:\Users\Lenovo\Downloads\audio.mp3"
audio.write_audiofile(audio_file)  # Extract audio and save it as a .wav file

pygame.mixer.music.load(audio_file)  # Load the audio file
pygame.mixer.music.play(loops=0, start=0.0)  # Start playing audio

# Start playing the video
clock = pygame.time.Clock()

# Hex code for your color (#2180FF)
color = (33, 128, 255)  # RGB equivalent of #2180FF

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    # Rotate the frame 270 degrees (to the left three times)
    frame_rotated = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # Flip the rotated frame to correct the mirroring
    frame_rotated = cv2.flip(frame_rotated, 1)  # 1 means horizontal flip

    # Convert the rotated frame from OpenCV (BGR) to Pygame (RGB)
    frame_rgb = cv2.cvtColor(frame_rotated, cv2.COLOR_BGR2RGB)

    # Scale the frame to fit the screen
    frame_resized = pygame.transform.scale(pygame.surfarray.make_surface(frame_rgb), (new_video_width, new_video_height))

    # Draw the resized frame on the Pygame window
    screen.fill(color)  # Fill the screen with your hex color #2180FF (RGB equivalent)
    screen.blit(frame_resized, ((screen_width - new_video_width) // 2, (screen_height - new_video_height) // 2))

    # Update the display
    pygame.display.update()

    # Delay to match the FPS
    clock.tick(fps)

# Release the video capture and close Pygame
cap.release()
pygame.quit()
