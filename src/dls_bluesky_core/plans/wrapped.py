from typing import Any, List, Mapping, Optional, Union

import bluesky.plans as bp
from bluesky.protocols import Readable

from dls_bluesky_core.core import MsgGenerator

"""
Wrappers for Bluesky built-in plans with type hinting and renamed metadata
"""


def count(
    detectors: set[Readable],
    num: int = 1,
    delay: Optional[Union[float, List[float]]] = None,
    metadata: Optional[Mapping[str, Any]] = None,
) -> MsgGenerator:
    """
    Take `n` readings from a device

    Args:
        detectors (Set[Readable]): Readable devices to read
        num (int, optional): Number of readings to take. Defaults to 1.
        delay (Optional[Union[float, List[float]]], optional): Delay between readings.
                                                               Defaults to None.
        metadata (Optional[Mapping[str, Any]], optional): Key-value metadata to include
                                                          in exported data.
                                                          Defaults to None.

    Returns:
        MsgGenerator: _description_

    Yields:
        Iterator[MsgGenerator]: _description_
    """

    yield from bp.count(detectors, num, delay=delay, md=metadata or {})
