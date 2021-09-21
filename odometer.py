#!/usr/bin/env python3

from datetime import datetime, timedelta
from typing import Tuple
from util import utc_now
import board        # type: ignore
import digitalio    # type: ignore


class Odometer:
    def __init__(self):
        self.reed_switch = digitalio.DigitalInOut(board.D16)
        self.reed_switch.direction = digitalio.Direction.INPUT
        self.reed_switch.pull = digitalio.Pull.UP

        self.OPEN_STATE = True
        self.DEBOUNCE = timedelta(milliseconds=100)

        self.previous_time = utc_now()
        self.previous_state = self.OPEN_STATE
        self.total_rotations = 0

    def check_rotations(self) -> Tuple[int, datetime]:
        current_time = utc_now()
        delta = current_time - self.previous_time
        if delta < self.DEBOUNCE:
            return (0, current_time)

        current_state = self.reed_switch.value
        if current_state != self.previous_state:
            self.previous_time = current_time
            self.previous_state = current_state
            if current_state != self.OPEN_STATE:
                self.total_rotations += 1
                print(f'count: {self.total_rotations}\tdelta: {delta.total_seconds() * 1000}ms')
                return (1, current_time)

        return (0, current_time)
