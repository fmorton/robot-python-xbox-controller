import math
import os
import pygame
import time

from robot.xbox_state import XboxState


class XboxController:
    EVENT_LOOP_DELAY = 0.05
    WAITING_LOOP_DELAY = 1.0
    CLOCK_TICKS = 20

    BUTTON_A = 0
    BUTTON_B = 1
    BUTTON_X = 2
    BUTTON_Y = 3
    BUTTON_VIEW = 4  #  left middle button
    BUTTON_XBOX = 5  #  center middle button
    BUTTON_SHARE = 6  # right middle button
    BUTTON_LEFT_JOYSTICK = 7
    BUTTON_RIGHT_JOYSTICK = 8
    BUTTON_LEFT_BUMPER = 9
    BUTTON_RIGHT_BUMPER = 10
    BUTTON_FORWARD = 11
    BUTTON_BACKWARD = 12
    BUTTON_LEFT = 13
    BUTTON_RIGHT = 14

    def __init__(self):
        self.connected = False
        self.controller = None
        self.controller_name = None
        self.device_index = None
        self.state = XboxState()
        self.clock = pygame.time.Clock()

        os.environ["SDL_VIDEODRIVER"] = "dummy"

        pygame.init()
        pygame.joystick.init()

    def _connect_event(self, event):
        self.device_index = event.device_index
        self.controller = pygame.joystick.Joystick(self.device_index)
        self.controller_name = self.controller.get_name()
        self.connected = True

        return self

    def connect(self, wait_for_controller_message="Waiting for Xbox Controller"):
        if wait_for_controller_message:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYDEVICEADDED:
                        return self._connect_event(event)

                print(wait_for_controller_message)

                time.sleep(XboxController.WAITING_LOOP_DELAY)

    @classmethod
    def quit_event(cls, event):
        if event.type == pygame.QUIT:
            return True

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 15:
                return True

        return False

    def run(self, run_method, debugging=False):
        running = True

        while running:
            for event in pygame.event.get():
                if self.quit_event(event):
                    return False
                else:
                    self.state.event(event, debugging)

            running = run_method(self)

    def tick(self, frame_rate):
        self.clock.tick(frame_rate)

    @classmethod
    def wheel_speeds(cls, x_axis, y_axis, max_speed=1.0):
        """
        Converts controller axes to differential wheel speeds.
        y_axis: forward/backward (-1 to 1)
        x_axis: left/right (-1 to 1)
        """
        # Simple mapping:
        # Forward: Y is negative, so invert it
        # Turn: X is positive to the right

        speed = -y_axis
        turn = x_axis

        # Calculate speeds
        left_speed = speed + turn
        right_speed = speed - turn

        # Normalize/Clamp values to -1.0 to 1.0
        left_speed = max(-1.0, min(1.0, left_speed)) * max_speed
        right_speed = max(-1.0, min(1.0, right_speed)) * max_speed

        return round(left_speed, 2), round(right_speed, 2)

    @classmethod
    def wheel_speed_and_angle(cls, x_axis, y_axis, max_speed=1.0):
        if abs(x_axis) < 0.25:
            x_axis = 0.0
        if abs(y_axis) < 0.25:
            y_axis = 0.0

        speed = math.sqrt(x_axis**2 + y_axis**2)

        if speed > 1.0:
            speed = 1.0

        angle_rad = math.atan2(-y_axis, x_axis)
        angle_deg = math.degrees(angle_rad)

        # if angle_deg < 0:
        #    angle_deg += 360

        # print("Axis:", x_axis, y_axis, "  speed:", speed, "  angle", angle_deg)
        return round(speed, 2), round(angle_deg, 2)
