import pygame
import cv2
import time
import random
import math
import subprocess
import os


def play_video(video_path, sound_path, text):
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer for audio playback

    # Set up display to full screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Open the video file using OpenCV
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Get screen resolution
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Load the sound to play
    background_sound = pygame.mixer.Sound(sound_path)

    # Track the time for playing sound every 5 seconds
    last_sound_time = time.time()

    # Load the custom OTF font (adjust the path to your OTF font file)
    try:
        font_path = 'balo.otf'  # your custom OTF font path
        font_size = 50  # Adjust the size of the font
        font_path1 = 'BeautyMountainsPersonalUse-od7z.ttf'  # your custom OTF font path
        font_size1 = 130
        font = pygame.font.Font(font_path, font_size)
        font1 = pygame.font.Font(font_path1, font_size1)
    except pygame.error as e:
        print(f"Error loading custom font: {e}. Falling back to default font.")
        font = pygame.font.Font(None, 36)  # Default font if custom font fails
        font1 = pygame.font.Font(None, 36)
        # Rotate the frame 90 degrees clockwise
    def rotate_frame(frame):
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Correct clockwise rotation

    # Create a Pygame surface for displaying the video
    class RainDrop:
        def __init__(self, color):
            self.x = random.randint(0, screen_width)
            self.y = random.randint(-screen_height, 0)
            self.length = random.randint(15, 25)
            self.width = random.uniform(1, 3)
            self.speed = random.uniform(4, 8)
            gray_value = random.randint(150, 200)  # Control the shade of gray
            self.color = (gray_value, gray_value, gray_value, random.randint(150, 255))

        def fall(self):
            self.y += self.speed
            if self.y > screen_height:
                self.y = random.randint(-screen_height, 0)
                self.x = random.randint(0, screen_width)
                self.length = random.randint(15, 25)
                self.width = random.uniform(1, 3)

    def draw_rain(rain_drops):
        for drop in rain_drops:
            drop.fall()
            pygame.draw.line(screen, drop.color, (drop.x, drop.y), (drop.x, drop.y + drop.length), int(drop.width))

    def draw_lightning(last_flash_time):
        current_time = pygame.time.get_ticks()
        if current_time - last_flash_time > random.randint(15000, 16000):  # 15-16 seconds
            screen.fill((255, 255, 255))  # White flash
            thunder_sound.play()  # Play thunder sound
            pygame.display.flip()
            pygame.time.delay(100)
            return current_time, True  # Return new last flash time and flag to start rain
        return last_flash_time, False  # Return last flash time and no flag

    # Load thunder sound and rain sound
    thunder_sound = pygame.mixer.Sound("thunder.mp3")
    rain_sound = pygame.mixer.Sound("raaineffect.mp3")

    # Initialize rain effects
    initial_rain_color = (25, 0, 0)  # Initial color (dark gray) for better visibility
    new_rain_color = (25, 0, 0)  # Color to change to (light blue)
    rain_drops = [RainDrop(initial_rain_color) for _ in range(100)]  # Create rain drops with initial color
    rain_active = False
    rain_start_time = 0
    last_flash_time = pygame.time.get_ticks()  # Initialize last flash time

    color_change_time = 10000  # Time in milliseconds when rain color changes (e.g., 10 seconds)
    color_changed = False  # Flag to track if the rain color has changed

    # Play background sound
    background_sound.play(loops=-1, fade_ms=500)  # Loop background sound

    # Circle coordinates and radius
    circle_x, circle_y, circle_radius = screen_width // 2, screen_height // 2, 525

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if mouse click is inside the circle
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if click is inside the invisible circle
                if (mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2 <= circle_radius ** 2:
                    # If clicked on the circle, stop all sounds and run another Python file
                    pygame.mixer.stop()  # Stop all sounds
                    python_executable = r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\python.exe"  # Full path to the Python executable in your virtual environment
                    script_path = r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\Punjabmap.py"  # Full path to the script you want to run
                    subprocess.run(
                        [python_executable, script_path])  # Run the script using the correct Python interpreter
                    script_path_2 =r"C:\Users\Lenovo\PycharmProjects\tkinter\.venv\Scripts\Autoflow Well Cap\autoflow.py"   # Path to the second script you want to run
                    subprocess.run([python_executable, script_path_2])
                    # After script has executed, restart the background sound
                    background_sound.play(loops=-1,
                                          fade_ms=500)  # Restart background sound after the external script runs

        # Read a frame from the video
        ret, frame = cap.read()

        if not ret:  # Restart video if we reach the end
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Go to the first frame
            continue

        # Rotate the frame 90 degrees clockwise
        frame = rotate_frame(frame)

        # Get the new rotated frame's dimensions
        rotated_frame_width, rotated_frame_height = frame.shape[1], frame.shape[0]

        # Convert the frame from BGR (OpenCV format) to RGB (Pygame format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a Pygame surface from the frame
        frame_surface = pygame.surfarray.make_surface(frame_rgb)

        # Calculate scaling factor while maintaining the aspect ratio
        # We want to stretch the video to fill the entire screen
        scaled_width = screen_width
        scaled_height = screen_height

        # Scale the video frame to fill the screen
        frame_surface = pygame.transform.scale(frame_surface, (scaled_width, scaled_height))

        # Display the frame on the full screen
        screen.blit(frame_surface, (0, 0))  # Directly place the video at (0, 0)

        # **Do not draw the circle, it's invisible**

        # Render the text (bottom center of the screen)
        text_surface = font.render(text, True, (0, 255, 255))  # Light cyan text for visibility
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 30))  # Center at bottom
        current_time = time.time()
        melt_factor = math.sin(current_time * 2) * 5  # Sin wave to simulate melting (smooth oscillation)

        # Apply a bluish gradient effect to the text color over time
        color_value = int(128 + 127 * math.sin(current_time * 0.5))  # Oscillate between 128-255 for fluid color

        # Adjust the text rendering based on color and melting effect
        text_surface = font.render(text, True, (0, color_value, 255))  # Gradient between blue shades
        text_rect = text_surface.get_rect(
            center=(screen_width // 2, screen_height - 30 + melt_factor))  # Move text slightly to simulate melting

        # Create a glowing effect
        glow_surface = font.render(text, True,
                                   (0, max(color_value - 50, 0), 255))  # Light blue for glow (clamped color)
        glow_rect = glow_surface.get_rect(center=(screen_width // 2, screen_height - 30 + melt_factor))

        # Create a shadow effect (dark blue or navy)
        shadow_surface = font.render(text, True, (0, 0, 139))  # Dark blue for shadow
        shadow_rect = shadow_surface.get_rect(
            center=(screen_width // 2 + 4, screen_height - 30 + melt_factor + 4))  # Slight offset
        # Create a glow effect by rendering the text multiple times in a light blue

        # Blit the shadow (slightly offset), then the glow, and then the main text on top
        screen.blit(shadow_surface, shadow_rect)  # Shadow
        screen.blit(glow_surface, glow_rect)  # Glow effect
        screen.blit(text_surface, text_rect)  # Main text on top
        text1 = "WellTrack"
        text_surface1 = font1.render(text1, True, (150, 182, 183))  # Light cyan text for visibility

        # Set the position to top-left
        text_rect1 = text_surface1.get_rect(topleft=(20, 100))  # 10, 10 is the top-left corner with some padding

        # Blit the text at the top-left corner
        screen.blit(text_surface1, text_rect1)
        text2 = "Flow Smarter!"
        text_surface2 = font1.render(text2, True, (150, 182, 183))  # Light cyan text for visibility

        # Set the position to top-left
       # text_rect2 = text_surface2.get_rect(bottomright=(screen_width - 10, screen_height - 10)) # 10, 10 is the top-left corner with some padding

        # Blit the text at the top-left corner
       # screen.blit(text_surface2, text_rect2)
        text3 = "Flow Smarter!"
        text_surface3 = font1.render(text3, True, (150, 182, 183))  # Light cyan text for visibility

        # Set the position to top-left

        text_rect3 = text_surface3.get_rect(topright=(screen_width +30, 100)) # 10, 10 is the top-left corner with some padding

        # Blit the text at the top-left corner
        screen.blit(text_surface3, text_rect3)
        text4 = "Flow Smarter!"
        text_surface4 = font1.render(text4, True, (150, 182, 183))  # Light cyan text for visibility

        # Set the position to top-left
        #text_rect4 = text_surface4.get_rect(bottomleft=(10, screen_height - 10)) # 10, 10 is the top-left corner with some padding

        # Blit the text at the top-left corner
        #screen.blit(text_surface4, text_rect4)

        # Handle thunder and rain effect
        last_flash_time, start_rain = draw_lightning(last_flash_time)

        if start_rain:
            rain_active = True
            rain_start_time = pygame.time.get_ticks()
            rain_sound.play(-1)  # Loop rain sound

        if rain_active:
            # Change the rain color after a specific time (e.g., after 10 seconds)
            if not color_changed and pygame.time.get_ticks() - rain_start_time > color_change_time:
                color_changed = True
                # Change rain color to a new color (light blue)
                for drop in rain_drops:
                    drop.color = new_rain_color

            # Draw the rain with the updated color
            draw_rain(rain_drops)
            if pygame.time.get_ticks() - rain_start_time > 6000:  # Rain lasts for 6 seconds
                rain_active = False
                rain_sound.stop()  # Stop the rain sound

        # Update the display
        pygame.display.update()

        # Control the frame rate
        clock.tick(fps)

    # Clean up
    cap.release()
    pygame.quit()


video_path = r"C:\Users\Lenovo\Downloads\app.mp4"  # Your video path
sound_path = 'water-stream-108384.mp3'  # Your sound path
text = "Efficiency that Flows Across Continents!"  # The text to display

# Play the video with background sound and custom text
play_video(video_path, sound_path, text)
