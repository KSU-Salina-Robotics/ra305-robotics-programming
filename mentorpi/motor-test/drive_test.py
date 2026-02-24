from ros_robot_controller_sdk import Board
import time

board = Board()   # opens /dev/rrc at 1,000,000 baud

try:
    # Drive motor 1 and 2 forward at 1 r/s
    board.set_motor_speed([[1, 1.0], [2, 1.0], [3, 1.0], [4, 1.0]])
    time.sleep(2)

    # Reverse
    board.set_motor_speed([[1, -1.0], [2, -1.0], [3, -1.0], [4, -1.0]])
    time.sleep(2)

    # Stop
    board.set_motor_speed([[1, 0.0], [2, 0.0], [3, 0.0], [4, 0.0]])

finally:
    board.set_motor_speed([[1, 0.0], [2, 0.0], [3, 0.0], [4, 0.0]])
