from typing import Any, List, Mapping, Optional, Union

import bluesky.plans as bp
import bluesky.preprocessors as bpp
from bluesky.protocols import Readable
from dodal.plans.data_session_metadata import attach_data_session_metadata_decorator

from dls_bluesky_core.core import MsgGenerator

"""
Wrappers for Bluesky built-in plans with type hinting and renamed metadata
"""


def count(
    detectors: List[Readable],
    num: int = 1,
    delay: Optional[Union[float, List[float]]] = None,
    baseline: Optional[List[Readable]] = None,
    metadata: Optional[Mapping[str, Any]] = None,
) -> MsgGenerator:
    """
    Take `n` readings from a device

    Args:
        detectors (List[Readable]): Readable devices to read
        num (int): Number of readings to take. Defaults to 1.
        delay (Optional[Union[float, List[float]]]): Delay between readings.
                                                        Defaults to None.
        baseline (Optional[List[Readable]]): List of devices to read at start
                                                        and end of scan
        metadata (Optional[Mapping[str, Any]]): Key-value metadata to include
                                                        in exported data.
                                                        Defaults to None.

    Returns:
        MsgGenerator: _description_

    Yields:
        Iterator[MsgGenerator]: _description_
    """
    baseline = baseline or []

    @bpp.baseline_decorator(baseline)
    @attach_data_session_metadata_decorator(provider=None)
    def inner_plan() -> MsgGenerator:
        yield from bp.count(detectors, num, delay=delay, md=metadata)

    yield from inner_plan()
