from robot.xbox_controller import XboxController
from time import sleep


def robot(controller):
    print("robot", controller.state.state_string())

    if controller.state.button_down_milliseconds(XboxController.BUTTON_XBOX):
        return False

    sleep(XboxController.EVENT_LOOP_DELAY)

    return True


controller = XboxController().connect()

controller.run(robot)
