from robot.xbox_state import XboxState


class XboxStateLinux(XboxState):
    def event_button(self, button):
        return button

    def event_axis_motion(self, axis, value):
        self.axis_value[axis] = value

    def event_hat_motion(self, hat, value):
        self.axis_value[hat] = value

    def event_unprocessed(self, event):
        print("Unprocessed event", event)
