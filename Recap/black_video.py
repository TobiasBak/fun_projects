import cv2
import numpy as np

# Define the video parameters
width, height = 1920, 1080  # Video resolution
fps = 60.0  # Frames per second
video_length = 60  # Video length in seconds

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Define the codec
video = cv2.VideoWriter('ambientVideos/2.mp4', fourcc, fps, (width, height))

# Create a black image
black_image = np.zeros((height, width, 3), dtype=np.uint8)

# Write the black image to the video for the desired number of frames
for _ in range(int(fps * video_length)):
    video.write(black_image)
