import pygame

from robot.xbox_controller import XboxController

controller = XboxController().connect()

print("Controller connected")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            print(f"Controller axis {event.axis} value {event.value}")
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} pressed on controller {event.joy}")

            if event.button == XboxController.BUTTON_XBOX:
                running = False
