from typing import Optional

import pytest

from dls_bluesky_core.core import in_micros, step_to_num


@pytest.mark.parametrize("us,s", [(4_000_001, 5), (4_999_999, 5), (4_000, 1),
                                  (-4_000_001, -4), (-4_999_999, -4), (-4_000, 0),
                                  (4_000_000.1, 5), (4_999_999.9, 5), (0.1, 1),
                                  (-4_000_000.5, -4), (-4_999_999.9, -4), (-4.05, 0)])
def test_in_micros(us: float, s: int):
    assert in_micros(us) is s


@pytest.mark.parametrize("start,stop,step,expected_num,truncated_stop",
                         [(0, 0, 1, 1, None),  # start=stop, 1 point at start
                          (0, 0.5, 1, 1, 0),  # step>length, 1 point at start
                          (0, 1, 1, 2, None),  # stop=start+step, 1 point at start, 1 at stop
                          (0, 0.99, 1, 2, 1),  # stop >= start + 0.99*step, included
                          (0, 0.98, 1, 1, 0),  # stop < start + 0.99*step, not included
                          (0, 1.01, 1, 2, 1),  # stop >= start + 0.99*step, included
                          (0, 1.75, 0.25, 8, 1.75)
                          ])
def test_step_to_num(start: float, stop: float, step: float, expected_num: int, truncated_stop: Optional[float]):
    truncated_stop = stop if truncated_stop is None else truncated_stop
    actual_start, actual_stop, num = step_to_num(start, stop, step)
    assert actual_start == start
    assert actual_stop == truncated_stop
    assert num == expected_num
