

# given an image of a board with 42 circles placed within 6 rows and 7 columns, where the first circle is 89 pixels from the left and 61 pixels from the top, and the circle centers are 81 pixels apart, 
# for each circle, determine the color of the circle by calculating the average color of the pixels within a 10 pixel radius of the center of the circle
# return a 6x7 matrix representing the colors of the circles, where 1 represents a red circle, 2 represents a yellow circle, and 0 represents an empty circle

import cv2

path = r'img_c4\boardimg6.jpg'
# Read the image
img = cv2.imread(path)

# Define the circle centers
circle_centers = []
for i in range(6):
    for j in range(7):
        circle_centers.append((89 + 81*j, -61 - 81*i))

# Define the circle radius
circle_radius = 10

# Define the colors
red = (0, 0, 255)
yellow = (0, 255, 255)
# the empty circle is white with a tint of blue due to the lighting
empty = (255, 255, 255)

# Define the matrix
matrix = [[0 for i in range(7)] for j in range(6)]

# For each circle, determine the color of the circle by calculating the average color of the pixels within a 10 pixel radius of the center of the circle
for i in range(6):
    for j in range(7):
        # Define the circle
        circle = (circle_centers[i*7 + j], circle_radius)
        # Define the mask
        mask = img.copy()
        mask = cv2.circle(mask, circle[0], circle[1], empty, -1)
        # Calculate the average color of the pixels within the circle
        average_color = cv2.mean(img, mask=mask)
        # Print the average color
        print(average_color)

        # Determine the color of the circle
        if average_color[0] > 200 and average_color[1] > 200 and average_color[2] < 100:
            matrix[i][j] = 1
        elif average_color[0] > 200 and average_color[1] < 100 and average_color[2] < 100:
            matrix[i][j] = 2

# Print the matrix
for i in range(6):
    print(matrix[i])

# Display the image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
