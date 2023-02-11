# This program will use OpenCV to detect a 6x7 Connect 4 board and the red and yellow pieces on it. 
# Using OpenCV object detection, it will then determine the state of the board and will update a 2D array with the state of the board 
# with 0 representing an empty space, 1 representing a red piece, and 2 representing a yellow piece.

import cv2
import numpy as np
import math
import time
import os
import sys
import argparse
import random

path = r'img_c4\boardimg.jpg'

src = cv2.imread(path)

# Function to detect the red and yellow pieces on the board, as well as the empty spaces being white
def detectPieces(image):
    # Convert the image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of red and yellow in HSV, adjusting the values based on the lighting conditions
    # The values for red are split into two ranges because of the way OpenCV represents colors in HSV, so we need to combine them, and we do that by adding them together
    lower_red = np.array([0,100,100])
    upper_red = np.array([10,255,255])

    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])

    lower_white = np.array([226, 28, 80])
    upper_white = np.array([0,0,255])


    # Threshold the HSV image to get only red and yellow colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image
    res_red = cv2.bitwise_and(image,image, mask= mask_red)
    res_yellow = cv2.bitwise_and(image,image, mask= mask_yellow)
    res_white = cv2.bitwise_and(image,image, mask= mask_white)

    # Convert the images to grayscale
    gray_red = cv2.cvtColor(res_red, cv2.COLOR_BGR2GRAY)
    gray_yellow = cv2.cvtColor(res_yellow, cv2.COLOR_BGR2GRAY)
    gray_white = cv2.cvtColor(res_white, cv2.COLOR_BGR2GRAY)

    # Blur the images
    blur_red = cv2.GaussianBlur(gray_red, (5, 5), 0)
    blur_yellow = cv2.GaussianBlur(gray_yellow, (5, 5), 0)
    blur_white = cv2.GaussianBlur(gray_white, (5, 5), 0)

    # Threshold the images
    ret_red, thresh_red = cv2.threshold(blur_red, 60, 255, cv2.THRESH_BINARY)
    ret_yellow, thresh_yellow = cv2.threshold(blur_yellow, 60, 255, cv2.THRESH_BINARY)
    ret_white, thresh_white = cv2.threshold(blur_white, 60, 255, cv2.THRESH_BINARY)

    # Find the contours of the red pieces
    contours_red, hierarchy_red = cv2.findContours(thresh_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_red = sorted(contours_red, key=cv2.contourArea, reverse=True)

    # Find the contours of the yellow pieces
    contours_yellow, hierarchy_yellow = cv2.findContours(thresh_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow = sorted(contours_yellow, key=cv2.contourArea, reverse=True)

    # Find the contours of the white pieces
    contours_white, hierarchy_white = cv2.findContours(thresh_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the center of the red pieces
    centers_red = []
    for c in contours_red:
        # Get the moments of the contour
        M = cv2.moments(c)

        # Get the center of the contour
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers_red.append((cX, cY))
        else:
            cX, cY = 0, 0

    # Find the center of the yellow pieces
    centers_yellow = []
    for c in contours_yellow:
        # Get the moments of the contour
        M = cv2.moments(c)

        # Get the center of the contour
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers_yellow.append((cX, cY))
        else:
            cX, cY = 0, 0
    
    # Find the center of the white pieces
    centers_white = []
    for c in contours_white:
        # Get the moments of the contour
        M = cv2.moments(c)

        # Get the center of the contour
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers_white.append((cX, cY))
        else:
            cX, cY = 0, 0

    # Return the centers of the red and yellow and white pieces
    return centers_red, centers_yellow, centers_white

# Function to detect the board and return the center of the board with coordinates cX and cY
def detectBoard(image):
    cX, cY = 0, 0
    # Convert the image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of green in HSV, adjusting the values based on the lighting conditions
    lower_green = np.array([40,100,100])
    upper_green = np.array([70,255,255])

    # Threshold the HSV image to get only green colors
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and original image
    res_green = cv2.bitwise_and(image,image, mask= mask_green)

    # Convert the image to grayscale
    gray_green = cv2.cvtColor(res_green, cv2.COLOR_BGR2GRAY)

    # Blur the image
    blur_green = cv2.GaussianBlur(gray_green, (5, 5), 0)

    # Threshold the image
    ret_green, thresh_green = cv2.threshold(blur_green, 60, 255, cv2.THRESH_BINARY)

    # Find the contours of the board
    contours_green, hierarchy_green = cv2.findContours(thresh_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the center of the board
    for c in contours_green:
        # Get the moments of the contour
        M = cv2.moments(c)

        # Get the center of the contour
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

    # Return the center of the board with coordinates cX and cY
    return cX, cY

# Function to determine the state of the board
def determineBoardState(centers_red, centers_yellow, centers_white, cX, cY):
    # Create a 2D array to store the state of the board
    board = [[0 for x in range(7)] for y in range(6)]

    # Determine the state of the board
    for center in centers_red:
        # Determine the column of the red piece
        if center[0] < cX - 150:
            column = 0
        elif center[0] < cX - 50:
            column = 1
        elif center[0] < cX + 50:
            column = 2
        elif center[0] < cX + 150:
            column = 3
        elif center[0] < cX + 250:
            column = 4
        elif center[0] < cX + 350:
            column = 5
        else:
            column = 6

        # Determine the row of the red piece
        if center[1] < cY - 150:
            row = 0
        elif center[1] < cY - 50:
            row = 1
        elif center[1] < cY + 50:
            row = 2
        elif center[1] < cY + 150:
            row = 3
        elif center[1] < cY + 250:
            row = 4
        elif center[1] < cY + 350:
            row = 5
        else:
            row = 6

        # Update the state of the board
        board[row - 1][column] = 1

    for center in centers_yellow:
        # Determine the column of the yellow piece
        if center[0] < cX - 150:
            column = 0
        elif center[0] < cX - 50:
            column = 1
        elif center[0] < cX + 50:
            column = 2
        elif center[0] < cX + 150:
            column = 3
        elif center[0] < cX + 250:
            column = 4
        elif center[0] < cX + 350:
            column = 5
        else:
            column = 6

        # Determine the row of the yellow piece
        if center[1] < cY - 150:
            row = 0
        elif center[1] < cY - 50:
            row = 1
        elif center[1] < cY + 50:
            row = 2
        elif center[1] < cY + 150:
            row = 3
        elif center[1] < cY + 250:
            row = 4
        elif center[1] < cY + 350:
            row = 5
        else:
            row = 6

        # Update the state of the board
        board[row - 1][column] = 2

    for center in centers_white:
        # Determine the column of the white piece
        if center[0] < cX - 150:
            column = 0
        elif center[0] < cX - 50:
            column = 1
        elif center[0] < cX + 50:
            column = 2
        elif center[0] < cX + 150:
            column = 3
        elif center[0] < cX + 250:
            column = 4
        elif center[0] < cX + 350:
            column = 5
        else:
            column = 6

        # Determine the row of the white piece
        if center[1] < cY - 150:
            row = 0
        elif center[1] < cY - 50:
            row = 1
        elif center[1] < cY + 50:
            row = 2
        elif center[1] < cY + 150:
            row = 3
        elif center[1] < cY + 250:
            row = 4
        elif center[1] < cY + 350:
            row = 5
        else:
            row = 6

        # Update the state of the board
        board[row - 1][column] = 0

    # Return the state of the board
    return board

# Function to display the state of the board and displays the object centers
def displayBoardState(board):
    # Display the state of the board
    for row in board:
        print(row)

    # Display the centers of the red pieces
    for center in centers_red:
        cv2.circle(src, center, 5, (0, 0, 255), -1)

    # Display the centers of the yellow pieces
    for center in centers_yellow:
        cv2.circle(src, center, 5, (0, 255, 255), -1)

    # Display the centers of the white pieces
    for center in centers_white:
        cv2.circle(src, center, 5, (255, 255, 255), -1)

    # Encircle the clusters of pieces with a circle of the same color
    for center in centers_red:
        cv2.circle(src, center, 50, (0, 0, 255), 2)

    for center in centers_yellow:
        cv2.circle(src, center, 50, (0, 255, 255), 2)

    for center in centers_white:
        cv2.circle(src, center, 50, (255, 255, 255), 2)

    # Display the center of the board
    cv2.circle(src, (cX, cY), 5, (255, 0, 0), -1)

    # Display the image
    cv2.imshow("Image", src)

    # Wait for a key press
    cv2.waitKey(0)

    # Close all windows
    cv2.destroyAllWindows()

# Main function
if __name__ == "__main__":

    # Read the image
    path = r'img_c4\boardimg6.jpg'
    src = cv2.imread(path)

    # Detect the pieces and the board

    centers_red, centers_yellow, centers_white = detectPieces(src)

    cX, cY = detectBoard(src)

    # Determine the state of the board
    board = determineBoardState(centers_red, centers_yellow, centers_white, cX, cY)

    # Display the state of the board
    displayBoardState(board)