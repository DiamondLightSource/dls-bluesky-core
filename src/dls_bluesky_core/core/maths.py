from typing import Tuple

import numpy as np


def step_to_num(start: float, stop: float, step: float) -> Tuple[float, float, int]:
    """
    Standard handling for converting from start, stop, step to start, stop, num
    Forces step to be same direction as length
    Includes a final point if it is within 1% of the end point (consistent with GDA)

    Args:
        start (float):
            Start of length, will be returned unchanged
        stop (float):
            End of length, if length/step does not divide cleanly will be returned
            extended up to 1% of step, or else truncated.
        step (float):
            Length of a step along the line formed from start to stop.
            If stop < start, will be coerced to be backwards.

    Returns:
        start, truncated_stop, num = Tuple[float, float, int]
        start will be returned unchanged
        truncated_stop = start + num * step
        num is the maximal number of steps that could fit into the length.

    """
    # Make step be the right direction
    step = abs(step) if stop > start else -abs(step)
    # If stop is within 1% of a step then include it
    num = int((stop - start) / step + 0.01)
    return start, start + num * step, num


def in_micros(t: float) -> int:
    """
    Converts between units of microT and units of T.
    For example, from microseconds to seconds.

    Args:
        t (float): A time in microseconds, or other measurement in units of microU
    Returns:
        t (int): A time in seconds rounded up to the nearest whole second,
        or other measurement in units of U, rounded up to the nearest whole U.
    """
    return np.ceil(t / 1e6)
