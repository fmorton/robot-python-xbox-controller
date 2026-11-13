import threading
import time

from robot.xbox_controller import XboxController

class XboxControllerThread:
    def __init__(self, controller):
        self.controller = controller

        self.thread = threading.Thread(
            target=controller.run, args=(self.process_event,), daemon=True
        )

        self.thread.start()

    def process_event(self, controller):
        time.sleep(XboxController.EVENT_LOOP_DELAY)

        return True
