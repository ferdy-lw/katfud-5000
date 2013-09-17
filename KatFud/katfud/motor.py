import time
from threading import Thread
import logging
log = logging.getLogger(__name__)

from pyramid.events import subscriber, ApplicationCreated

import runtime


# GPIO numbers
RELAY_GPIO = 17
LED_GPIO = 22
BUTTON_GPIO = 27

count = 1
motor_on = False


def button_trigger(gpio_id, value):
    global count, motor_on

    import RPIO as GPIO
    log.debug("Got button value :{}".format(value))
    if motor_on:
        log.debug("motor on")
        if value == 1 and count > 1:  # Wait at least 1 tick too
            count = 1
            motor_on = False
            GPIO.output(RELAY_GPIO, False)
            runtime.runtime.numberFeeds += 1


def main_loop():
    global count, motor_on

    import RPIO as GPIO
    GPIO.add_interrupt_callback(BUTTON_GPIO, button_trigger, edge='both', threaded_callback=True)
    GPIO.wait_for_interrupts(threaded=True)  # , epoll_timeout=.25)

    try:

        while True:
            GPIO.output(LED_GPIO, not GPIO.input(LED_GPIO))
            time.sleep(.5)
            count += 1

            # log.debug("button val: {}".format(GPIO.input(BUTTON_GPIO)))

            if not motor_on:
                if runtime.runtime.is_feed_time(set_next_run=True):  # this WILL bump the next feed time
                    log.debug("feed time and not motor")
                    count = 1
                    motor_on = True
                    GPIO.output(RELAY_GPIO, True)

    except Exception as e:
        log.exception("Exception during run loop? {}".format(e))


def run_now():
    global count, motor_on

    import RPIO as GPIO
    if not motor_on:
        log.debug("run_now!")
        runtime.runtime.set_last_ran()
        count = 1
        motor_on = True
        GPIO.output(RELAY_GPIO, True)


@subscriber(ApplicationCreated)
def start_motor_loop(event):

    if event.app.registry.settings['katfud.non_pi']:
        log.warning("Not running on PI - no motor control")
        return

    import RPIO as GPIO

    GPIO.setup(RELAY_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # HW pull down

    loop_thread = Thread(target=main_loop, name='GPIO loop')
    loop_thread.daemon = True
    loop_thread.start()

    log.info("Started KatFud Motor loop")
