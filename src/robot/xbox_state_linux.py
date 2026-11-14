import time

from robot.xbox_state import XboxState


class XboxStateLinux(XboxState):
    def event_button_remap(self, button):
        if button == 3:
            return XboxState.BUTTON_X

        if button == 4:
            return XboxState.BUTTON_Y

        if button == 6:
            return XboxState.BUTTON_LEFT_BUMPER

        if button == 7:
            return XboxState.BUTTON_RIGHT_BUMPER

        if button == 10:
            return XboxState.BUTTON_VIEW

        if button == 11:
            return XboxState.BUTTON_MENU

        if button == 12:  # number not verified--causes QUIT somehow
            return XboxState.BUTTON_XBOX

        if button == 13:
            return XboxState.BUTTON_LEFT_JOYSTICK

        if button == 14:
            return XboxState.BUTTON_RIGHT_JOYSTICK

        return button

    def event_axis_remap(self, axis):
        if axis == 4:
            return XboxState.AXIS_RIGHT_TRIGGER

        if axis == 5:
            return XboxState.AXIS_LEFT_TRIGGER

        return axis

    def event_hat_motion_click_down(self, down_button, no_button):
        self.button_down_at[down_button] = time.perf_counter()
        self.button_down_at[no_button] = 0

    def event_hat_motion_click(self, minus_one_value, plus_one_value, value):
        if value == -1:
            self.event_hat_motion_click_down(minus_one_value, plus_one_value)
        elif value == 1:
            self.event_hat_motion_click_down(plus_one_value, minus_one_value)
        else:
            self.button_down_at[minus_one_value] = 0
            self.button_down_at[plus_one_value] = 0

    def event_button(self, button):
        return self.event_button_remap(button)

    def event_axis_motion(self, axis, value):
        self.axis_value[self.event_axis_remap(axis)] = value

    def event_hat_motion(self, hat, value):
        self.event_hat_motion_click(XboxState.BUTTON_LEFT, XboxState.BUTTON_RIGHT, value[0])
        self.event_hat_motion_click(XboxState.BUTTON_BACKWARD, XboxState.BUTTON_FORWARD, value[1])

    def event_unprocessed(self, event):
        print("Unprocessed event", event)
