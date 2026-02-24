#!/usr/bin/env python3
import sys
import time
import termios
import tty

from ros_robot_controller_sdk import Board

# ---- TUNE THESE ----
BASE_SPEED = 1.0      # motor speed in r/s (float)
TURN_SCALE = 0.6      # turning reduces one side speed
LEFT_MOTORS = [1, 3]
RIGHT_MOTORS = [2, 4]
# --------------------

def getch():
    """Read one character from stdin (no Enter needed)."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def set_diff(board, left_speed, right_speed):
    speeds = []
    for m in LEFT_MOTORS:
        speeds.append([m, float(left_speed)])
    for m in RIGHT_MOTORS:
        speeds.append([m, float(right_speed)])
    board.set_motor_speed(speeds)

def stop_all(board):
    speeds = [[1, 0.0], [2, 0.0], [3, 0.0], [4, 0.0]]
    board.set_motor_speed(speeds)

def main():
    board = Board()

    print("WASD SDK drive (no ROS)")
    print("W/S = forward/reverse, A/D = turn, Space = stop, Q = quit")

    left = 0.0
    right = 0.0

    try:
        stop_all(board)
        while True:
            ch = getch().lower()

            if ch == "w":
                left = BASE_SPEED
                right = BASE_SPEED
            elif ch == "s":
                left = -BASE_SPEED
                right = -BASE_SPEED
            elif ch == "a":
                left = -BASE_SPEED * TURN_SCALE
                right = BASE_SPEED * TURN_SCALE
            elif ch == "d":
                left = BASE_SPEED * TURN_SCALE
                right = -BASE_SPEED * TURN_SCALE
            elif ch == " ":
                left = 0.0
                right = 0.0
            elif ch == "q":
                break
            else:
                continue  # ignore other keys

            set_diff(board, left, right)
            print(f"\rL={left:+.2f}  R={right:+.2f}   ", end="", flush=True)

    finally:
        print("\nStopping motors...")
        stop_all(board)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
