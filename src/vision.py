import cv2
import numpy as np

# take a picture of the scene and save it as a matrix
camera = cv2.VideoCapture(0)
return_value, image = camera.read()

height, width, depth = image.shape
sub_images = [[[] for _ in range(6)] for _ in range(7)]
for i in range(6):
    for j in range(7):
        sub_images[i][j] = image[height // 6 * i:height // 6 * (i + 1), width // 7 * j:width // 7 * (j + 1)]
        
print(sub_images[0])