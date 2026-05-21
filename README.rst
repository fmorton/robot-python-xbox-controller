========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - package
      - | |version| |wheel| |supported-versions|
.. |docs| image:: https://readthedocs.org/projects/robot-python-xbox-controller/badge/?style=flat
    :target: https://robot-xbox-controller.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/fmorton/robot-python-xbox-controller/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/fmorton/robot-python-xbox-controller/actions

.. |codecov| image:: https://codecov.io/gh/fmorton/robot-xbox-controller/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/fmorton/robot-xbox-controller

.. |version| image:: https://img.shields.io/pypi/v/robot-xbox-controller.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/robot-xbox-controller

.. |wheel| image:: https://img.shields.io/pypi/wheel/robot-xbox-controller.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/robot-xbox-controller

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/robot-xbox-controller.svg
    :alt: Supported versions
    :target: https://pypi.org/project/robot-xbox-controller

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/robot-xbox-controller.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/robot-xbox-controller


.. end-badges

Library for xbox controllers.

* Free software: MIT License

Installation
============

::

    pip install robot-xbox-controller

You can also install the in-development version with::

    pip install https://github.com/fmorton/robot-xbox-controller/archive/main.zip



Xbox Controller Example
=======================

.. code-block:: python

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


Xbox Controller Example Using run() and the Controller State
============================================================

The run() loop maintains the state of the controllers and all buttons for processing by your supplied method, "robot" in the example below.

.. code-block:: python

  from robot.xbox_controller import XboxController
  from time import sleep


  def robot(controller):
    print("runner", controller.state.state_string())

    if controller.state.button_down_milliseconds(XboxController.BUTTON_XBOX):
        return False

    sleep(XboxController.EVENT_LOOP_DELAY)

    return True


  controller = XboxController().connect()

  controller.run(robot)



The controller.state has the following methods to retrieve the selections.

.. code-block:: python

  controller.state.left_x()        # returns x value of left controller (-1 means max forward/1 max backward)
  controller.state.left_y()        # returns y value of left controller (-1 means max left/1 max right)
  controller.state.left_axis()     # returns left_x, left_y

  controller.state.right_x()       # returns x value of right controller (-1 means max forward/1 max backward)
  controller.state.right_y()       # returns y value of right controller (-1 means max left/1 max right)
  controller.state.right_axis()    # returns right_x, right_y

  controller.state.left_trigger()       # returns left trigger value (0 to 1 if fully pressed)
  controller.state.right_trigger()      # returns right trigger value (0 to 1 if fully pressed)

  controller.state.left_trigger_raw()   # returns left trigger unadjusted value (-1 to 1 if fully pressed)
  controller.state.right_trigger_raw()   # returns right trigger unadjusted value (-1 to 1 if fully pressed)

  controller.state.button_down_seconds(button)       # how many seconds "button" has been pressed
  controller.state.button_down_milliseconds(button)  # how many milliseconds "button" has been pressed



The following button constant values are available in XboxController:

.. code-block:: python

  BUTTON_A = 0
  BUTTON_B = 1
  BUTTON_X = 2
  BUTTON_Y = 3
  BUTTON_VIEW = 4   #  left middle button
  BUTTON_XBOX = 5   #  center middle button
  BUTTON_SHARE = 6  # right middle button
  BUTTON_LEFT_JOYSTICK = 7
  BUTTON_RIGHT_JOYSTICK = 8
  BUTTON_LEFT_BUMPER = 9
  BUTTON_RIGHT_BUMPER = 10
  BUTTON_FORWARD = 11
  BUTTON_BACKWARD = 12
  BUTTON_LEFT = 13
  BUTTON_RIGHT = 14



Testing
=======

To run all the tests run::

    pytest -s
