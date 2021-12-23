#!/usr/bin/env python3

from datetime import datetime, timedelta
from typing import Tuple
from util import utc_now


class Odometer:
    def __init__(self):
        import board        # type: ignore
        import digitalio    # type: ignore

        self._reed_switch = digitalio.DigitalInOut(board.D16)
        self._reed_switch.direction = digitalio.Direction.INPUT
        self._reed_switch.pull = digitalio.Pull.UP

        self._OPEN_STATE = True
        self._DEBOUNCE = timedelta(milliseconds=100)

        self._previous_time = utc_now()
        self._previous_state = self._OPEN_STATE

        self.total_rotations = 0

    def check_rotations(self) -> Tuple[int, datetime]:
        current_time = utc_now()
        delta = current_time - self._previous_time
        if delta < self._DEBOUNCE:
            return (0, current_time)

        current_state = self._reed_switch.value
        if current_state != self._previous_state:
            self._previous_time = current_time
            self._previous_state = current_state
            if current_state != self._OPEN_STATE:
                self.total_rotations += 1
                # print(f'count: {self.total_rotations}\tdelta: {delta.total_seconds() * 1000}ms')
                return (1, current_time)

        return (0, current_time)


class MockOdometer:
    def __init__(self):
        self._previous_time = utc_now()

        self._DEBOUNCE = timedelta(milliseconds=100)

        self.total_rotations = 0

    def check_rotations(self) -> Tuple[int, datetime]:
        import random
        current_time = utc_now()
        delta = current_time - self._previous_time

        if delta < self._DEBOUNCE:
            return (0, current_time)

        if random.choices([True, False], weights=[1, 1000], k=1)[0] is True:
            self._previous_time = current_time
            self.total_rotations += 1
            print(f'count: {self.total_rotations}\tdelta: {delta.total_seconds() * 1000}ms')
            return (1, current_time)

        return (0, current_time)
