from typing import List, Optional

import numpy as np
from scanspec.core import Frames
from scanspec.specs import DURATION


def get_duration(frames: List[Frames]) -> Optional[float]:
    """
    Returns the duration of a number of ScanSpec frames, if known and consistent.

    Args:
        frames (List[Frames]): A number of Frame objects

    Raises:
        ValueError: If any frames do not have a Duration defined.

    Returns:
        duration (float): if all frames have a consistent duration
        None: otherwise

    """
    for fs in frames:
        if DURATION in fs.axes():
            durations = fs.midpoints[DURATION]
            first_duration = durations[0]
            if np.all(durations == first_duration):
                # Constant duration, return it
                return first_duration
            else:
                return None
    raise ValueError("Duration not specified in Spec")
