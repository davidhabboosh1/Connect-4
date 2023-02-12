# Connect 4 Robot

## Introduction

A robot that plays Connect 4 against you!

## How to Use

1. Clone the repository

2. Run `python3 main.py`

3. Place the robot in front of the leftmost column.

4. Place the camera from your perspective on the other side of the board.

5. Play Connect 4 against the robot! It will move when it has detected that you have placed a piece.

## What It Does

The robot uses a webcam to detect the current state of the board, which is used to determine the best move the robot can play. The robot moves and drops the piece.

## How We Built It

We used OpenCV to detect the board and the pieces. We used an Arduino to control the motors which drive the wheels and the servos which deploy pieces. These 

## Challenges We Ran Into

We first tried to use a Raspberry Pi to control the robot, but we ran into issues with the Pi's GPIO pins. We then switched to an Arduino, which we had more experience with.

Another challenge that we had was with image detection. Since none of us had experience with image processing, we had to consult many outside resources to accomplish this. One that we found particularly helpful was [this repo](https://github.com/Matt-Jennings-GitHub/ConnectFour-ComputerVisionAI)

## Accomplishments That We're Proud Of

We are proud to have a working robot that can traverse columns and drop pieces at will. We are also proud of our algorithm implementation, which allows the robot to play at a reasonable level.

## What We Learned

We learned many new tools and techniques, including OpenCV, game solving algorithms such as Monte Carlo and minimax, and how to design a robotics project from the ground up.

## What's Next for Connect 4 Robot

We would like to improve the robot's ability to detect the board and pieces, since our algorithm is not perfect despite performing well. We would also like to improve the robot's ability to play the game, perhaps training a neural network on many played games.