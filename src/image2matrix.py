import numpy as np

# given an image of a board with 42 circles placed within 6 rows and 7 columns, where the first circle is 89 pixels from the left and 61 pixels from the top, and the circle centers are 81 pixels apart, 
# for each circle, determine the color of the circle by calculating the average color of the pixels within a 10 pixel radius of the center of the circle
# return a 6x7 matrix representing the colors of the circles, where 1 represents a red circle, 2 represents a yellow circle, and 0 represents an empty circle

import cv2

path = r'img_c4\boardimg6.jpg'
# Read the image
img = cv2.imread(path)
height, width, depth = img.shape
col_step = width // 7
row_step = height // 6

# Define the colors
red = (0, 0, 255)
yellow = (0, 255, 255)
empty = (255, 255, 255)

avg_colors = [[[] for _ in range(7)] for _ in range(6)]
for i in range(6):
    for j in range(7):
        avg_colors[i][j] = np.average(img[i * row_step + 25:(i + 1) * row_step - 25, j * col_step + 25:(j + 1) * col_step - 25], axis=(0, 1))
        
colors = [[0 for _ in range(7)] for _ in range(6)]
for row in range(6):
    for col in range(7):
        # find the difference between the average color of the circle and the red and yellow colors and empty
        red_diff = np.linalg.norm(avg_colors[row][col] - red)
        yellow_diff = np.linalg.norm(avg_colors[row][col] - yellow)
        empty_diff = np.linalg.norm(avg_colors[row][col] - empty)
        
        if red_diff < yellow_diff and red_diff < empty_diff:
            colors[i][j] = 1
        elif yellow_diff < red_diff and yellow_diff < empty_diff:
            colors[i][j] = 2
        else:
            colors[i][j] = 0
        
print(colors)

# Display the image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
