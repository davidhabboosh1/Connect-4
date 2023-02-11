# This program will use OpenCV to detect a 6x7 Connect 4 board and the red and yellow pieces on it. 
# When segmenting the image, first it finds the blue board (rectangle), and then for each of the 6x7 cells, find whether the cell is empty (0), red (1), or yellow (2)
# The final answer should be a 2-dimensional matrix  which is 6 by 7 depicting the status of the board.

# The steps for this program go as follows:
# 1. Read in the image
# 2. Find the blue board
# 3. Find the red and yellow pieces
# 4. Find the status of each cell
# 5. Print the status of the board (2-dimensional matrix), and display the image with the board and pieces

# Import the necessary packages
import numpy as np
import argparse
import cv2
import math
import time
import imutils

# Define the lower and upper boundaries of the blue board in the HSV color space
lower = np.array([100, 100, 100])
upper = np.array([140, 255, 255])

# Define the lower and upper boundaries of the red pieces in the HSV color space
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Define the lower and upper boundaries of the yellow pieces in the HSV color space
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# Define the lower and upper boundaries of the empty cells in the HSV color space, being between dark blue and light blue due to the lighting
lower_empty = np.array([90, 100, 100])
upper_empty = np.array([110, 255, 255])

# Read in the image
path = r'img_c4\boardimg6.jpg'
image = cv2.imread(path)

# Resize the image
image = imutils.resize(image, width=600)

# Convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Find the blue board in the image
mask = cv2.inRange(hsv, lower, upper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)

# Find the contours in the mask
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# # Find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
# c = max(cnts, key=cv2.contourArea)
# ((x, y), radius) = cv2.minEnclosingCircle(c)
# M = cv2.moments(c)
# center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

# # Draw the circle and centroid on the image, then update the list of tracked points
# cv2.circle(image, (int(x), int(y)), int(radius),
#     (0, 255, 255), 2)
# cv2.circle(image, center, 5, (0, 0, 255), -1)

# Find the red and yellow pieces in the image
mask_red = cv2.inRange(hsv, lower_red, upper_red)
mask_red = cv2.erode(mask_red, None, iterations=2)
mask_red = cv2.dilate(mask_red, None, iterations=2)
mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
mask_yellow = cv2.erode(mask_yellow, None, iterations=2)
mask_yellow = cv2.dilate(mask_yellow, None, iterations=2)

# Find the empty cells in the image
mask_empty = cv2.inRange(hsv, lower_empty, upper_empty)
mask_empty = cv2.erode(mask_empty, None, iterations=2)
mask_empty = cv2.dilate(mask_empty, None, iterations=2)

# Find the contours in the mask
cnts_red = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts_red = imutils.grab_contours(cnts_red)
cnts_yellow = cv2.findContours(mask_yellow.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts_yellow = imutils.grab_contours(cnts_yellow)
cnts_empty = cv2.findContours(mask_empty.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts_empty = imutils.grab_contours(cnts_empty)


# Find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
for c in cnts_yellow:
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    cv2.circle(image, (int(x), int(y)), int(radius),
        (0, 100, 255), 2)
    cv2.circle(image, center, 5, (0, 0, 255), -1)

for c in cnts_red:
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    cv2.circle(image, (int(x), int(y)), int(radius),
        (0, 255, 255), 2)
    cv2.circle(image, center, 5, (0, 0, 255), -1)

for c in cnts_empty:
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    cv2.circle(image, (int(x), int(y)), int(radius),
        (255, 255, 255), 2)
    cv2.circle(image, center, 5, (0, 0, 255), -1)


# Now that we have computed the minimum enclosing circle and centroid, we can find the status of each cell
# First, we need to find the center of each cell

# Find the center of the board
center_board = (int(x), int(y))

# Find the center of each cell
# First, find the center of the first cell
center_cell_1 = (int(center_board[0] - 3*radius), int(center_board[1] - 3*radius))

# Find the center of the other cells
center_cell = []
for i in range(6):
    for j in range(7):
        center_cell.append((int(center_cell_1[0] + 2*j*radius), int(center_cell_1[1] + 2*i*radius)))

# Find the status of each cell
# First, find the status of the first cell
# Find the distance between the center of the first cell and the center of the red pieces
distance_red = []
for i in range(len(cnts_red)):
    distance_red.append(math.sqrt((center_cell_1[0] - cnts_red[i][0][0][0])**2 + (center_cell_1[1] - cnts_red[i][0][0][1])**2))

# Find the distance between the center of the first cell and the center of the yellow pieces
distance_yellow = []
for i in range(len(cnts_yellow)):
    distance_yellow.append(math.sqrt((center_cell_1[0] - cnts_yellow[i][0][0][0])**2 + (center_cell_1[1] - cnts_yellow[i][0][0][1])**2))

distance_empty = []
for i in range(len(cnts_empty)):
    distance_empty.append(math.sqrt((center_cell_1[0] - cnts_empty[i][0][0][0])**2 + (center_cell_1[1] - cnts_empty[i][0][0][1])**2))

# Find the status of the first cell
if len(distance_red) == 0 and len(distance_yellow) == 0 and len(distance_empty) == 0:
    status_cell_1 = 0
elif len(distance_red) == 0 and len(distance_yellow) == 0 and len(distance_empty) != 0:
    status_cell_1 = 1
elif len(distance_red) == 0 and len(distance_yellow) != 0 and len(distance_empty) == 0:
    status_cell_1 = 2
elif len(distance_red) != 0 and len(distance_yellow) == 0 and len(distance_empty) == 0:
    status_cell_1 = 3
else:
    status_cell_1 = 4

# Find the status of the other cells
status_cell = []
for i in range(len(center_cell)):
    # Find the distance between the center of the other cells and the center of the red pieces
    distance_red = []
    for j in range(len(cnts_red)):
        distance_red.append(math.sqrt((center_cell[i][0] - cnts_red[j][0][0][0])**2 + (center_cell[i][1] - cnts_red[j][0][0][1])**2))

    # Find the distance between the center of the other cells and the center of the yellow pieces
    distance_yellow = []
    for j in range(len(cnts_yellow)):
        distance_yellow.append(math.sqrt((center_cell[i][0] - cnts_yellow[j][0][0][0])**2 + (center_cell[i][1] - cnts_yellow[j][0][0][1])**2))

    # Find the distance between the center of the other cells and the center of the empty cells
    distance_empty = []
    for j in range(len(cnts_empty)):
        distance_empty.append(math.sqrt((center_cell[i][0] - cnts_empty[j][0][0][0])**2 + (center_cell[i][1] - cnts_empty[j][0][0][1])**2))

    # Find the status of the other cells
    if len(distance_red) == 0 and len(distance_yellow) == 0 and len(distance_empty) == 0:
        status_cell.append(0)
    elif len(distance_red) == 0 and len(distance_yellow) == 0 and len(distance_empty) != 0:
        status_cell.append(1)
    elif len(distance_red) == 0 and len(distance_yellow) != 0 and len(distance_empty) == 0:
        status_cell.append(2)
    elif len(distance_red) != 0 and len(distance_yellow) == 0 and len(distance_empty) == 0:
        status_cell.append(3)
    else:
        status_cell.append(4)

# Add the status of the first cell to the status of the other cells
status_cell.insert(0, status_cell_1)

# Show the image
cv2.imshow("Image", image)
cv2.waitKey(0)

# kill all open windows
cv2.destroyAllWindows()

