import pygame
import time


class XboxState:
    JOYSTICK_DRIFT = 0.18

    def __init__(self):
        self.axis_value = [0.0, 0.0, 0.0, 0.0, -1.0, -1.0]
        self.button_down_at = [0] * 16
        pass

    def show_value_string(self, value):
        return "{:6.2f}".format(value)

    def state_string(self, extra_string=None):
        s = ""
        s = s + self.show_value_string(self.left_x())
        s = s + self.show_value_string(self.left_y())
        s = s + self.show_value_string(self.right_x())
        s = s + self.show_value_string(self.right_y())
        s = s + self.show_value_string(self.left_trigger())
        s = s + self.show_value_string(self.right_trigger())
        if extra_string is not None:
            s = s + " " + extra_string

        for button in range(16):
            down_seconds = self.button_down_seconds(button)

            if down_seconds > 0:
                s += f" button{button:3d} down: {down_seconds:4.2f} seconds"

        return s

    def print_state_string(self, extra_string=None):
        print(self.state_string(extra_string))

    def event(self, event, debugging=False):
        if event.type == pygame.JOYBUTTONUP:
            self.button_down_at[event.button] = 0
        elif event.type == pygame.JOYBUTTONDOWN:
            self.button_down_at[event.button] = time.perf_counter()
        elif event.type == pygame.JOYAXISMOTION:
            value = event.value

            if abs(value) < XboxState.JOYSTICK_DRIFT:
                value = 0.0

            self.axis_value[event.axis] = round(value, 2)
        else:
            print("Unprocessed event:", event)

        if debugging:
            print(self.state_string())

    def dictionary(self):
        d = {}
        d["left_x"] = self.left_x()
        d["left_y"] = self.left_y()
        d["right_x"] = self.right_x()
        d["right_y"] = self.right_y()
        d["left_trigger"] = self.left_trigger()
        d["right_trigger"] = self.right_trigger()

        for button in range(16):
            d[str(button)] = self.button_down_milliseconds(button)

        d["a_button"] = self.button_down_milliseconds(0)
        d["b_button"] = self.button_down_milliseconds(1)
        d["x_button"] = self.button_down_milliseconds(2)
        d["y_button"] = self.button_down_milliseconds(3)
        d["view_button"] = self.button_down_milliseconds(4)
        d["xbox_button"] = self.button_down_milliseconds(5)
        d["menu_button"] = self.button_down_milliseconds(6)
        d["left_stick_click"] = self.button_down_milliseconds(7)
        d["right_stick_click"] = self.button_down_milliseconds(8)
        d["left_bumper"] = self.button_down_milliseconds(9)
        d["right_bumper"] = self.button_down_milliseconds(10)
        d["d_pad_up"] = self.button_down_milliseconds(11)
        d["d_pad_down"] = self.button_down_milliseconds(12)
        d["d_pad_left"] = self.button_down_milliseconds(13)
        d["d_pad_right"] = self.button_down_milliseconds(14)

        return d

    def left_x(self):
        return self.axis_value[0]

    def left_y(self):
        return self.axis_value[1]

    def left_axis(self):
        return self.left_x(), self.left_y()

    def right_x(self):
        return self.axis_value[2]

    def right_y(self):
        return self.axis_value[3]

    def right_axis(self):
        return self.right_x(), self.right_y()

    def adjusted_trigger_value(self, value):
        return round((value + 1.0) / 2.0, 2)

    def left_trigger(self):
        return self.adjusted_trigger_value(self.axis_value[4])

    def right_trigger(self):
        return self.adjusted_trigger_value(self.axis_value[5])

    def left_trigger_raw(self):
        return self.axis_value[4]

    def right_trigger_raw(self):
        return self.axis_value[5]

    def button_down_seconds(self, button):
        if self.button_down_at[button] <= 0:
            return 0

        return time.perf_counter() - self.button_down_at[button]

    def button_down_milliseconds(self, button):
        return int(self.button_down_seconds(button) * 1000.0)
