import operator
from functools import reduce
from typing import Any, Dict, List, Mapping, Optional, Sequence

import bluesky.plan_stubs as bps
import bluesky.plans as bp
import bluesky.preprocessors as bpp
from bluesky.protocols import Movable, Readable
from cycler import Cycler, cycler
from ophyd_async.core import Device
from ophyd_async.core.flyer import ScanSpecFlyable
from scanspec.specs import Repeat, Spec

from ..core import MsgGenerator
from ..stubs.flyables import fly_and_collect

"""
Plans related to the use of the `ScanSpec https://github.com/dls-controls/scanspec`
library for constructing arbitrarily complex N-dimensional trajectories, similar to
Diamond's "mapping scans" using ScanPointGenerator.
"""


def scan(
    detectors: List[Readable],
    axes_to_move: Mapping[str, Movable],
    spec: Spec[str],
    metadata: Optional[Mapping[str, Any]] = None,
) -> MsgGenerator:
    """
    Scan wrapping `bp.scan_nd`

    Args:
        detectors: List of readable devices, will take a reading at
                                    each point
        axes_to_move: All axes involved in this scan, names and
            objects
        spec: ScanSpec modelling the path of the scan
        metadata: Key-value metadata to include
                                                          in exported data, defaults to
                                                          None.

    Returns:
        MsgGenerator: Plan

    Yields:
        Iterator[MsgGenerator]: Bluesky messages
    """

    _md = {
        "plan_args": {
            "detectors": list(map(repr, detectors)),
            "axes_to_move": {k: repr(v) for k, v in axes_to_move.items()},
            "spec": repr(spec),
        },
        "plan_name": "scan",
        "shape": spec.shape(),
        **(metadata or {}),
    }

    cycler = _scanspec_to_cycler(spec, axes_to_move)
    yield from bp.scan_nd(detectors, cycler, md=_md)


def scanspec_fly(
    flyer: ScanSpecFlyable,
    hw_spec: Spec[ScanSpecFlyable],
    sw_dets: Optional[Sequence[Device]] = None,
    sw_spec: Optional[Spec[Device]] = None,
    # TODO: How to allow in Blueapi REST call?
    # TODO: Allow defining processors for @BeforeScan/@AfterScan equivalent logic?
    # setup_detectors: Optional[Collection[Msg]] = None,
    # flush_period: float = 0.5,  # TODO: Should we allow overriding default?
    metadata: Optional[Dict[str, Any]] = None,
) -> MsgGenerator:
    """
    TODO

    Args:
        flyer (ScanSpecFlyable):
            A Flyable that traces the path of hw_spec Spec at every point of sw_spec.
        hw_spec (Spec[Device]):
            The 'inner scan' performed at each point of the outer scan.
        sw_dets (Optional[Sequence[Device]]):
            Any detectors to be triggered at every point of an outer scan.
        sw_spec (Optional[Spec[Device]]):
            The 'outer scan' trajectory to be followed by any non-flying motors.
            Defaults to a one-shot no-op Spec.
        # setup_detectors (Iterator[Msg]):
            Any Msgs required to set up the detectors  # TODO: Make a pre-processor?
        # flush_period (float):  # TODO: Allow non-default?
            Timeout for calls to complete when the flyer is kicked off.
        metadata (Optional[Dict[str, Any]]):
            Key-value metadata to include in exported data, defaults to None.

    Returns:
        MsgGenerator: _description_

    Yields:
        Iterator[MsgGenerator]: _description_
    """
    sw_dets = sw_dets or []
    sw_spec = sw_spec or Repeat()
    detectors: Sequence[Device] = [flyer] + sw_dets
    plan_args = {
        "flyer": repr(flyer),
        "hw_spec": repr(hw_spec),
        "sw_dets": [repr(det) for det in sw_dets],
        "sw_spec": repr(sw_spec),
    }

    _md = {
        "plan_args": plan_args,
        "detectors": [det.name for det in detectors],
        "hints": {},  # TODO: Dimension hints from ScanSpec?
    }
    _md.update(metadata or {})

    @bpp.stage_decorator(detectors)
    @bpp.run_decorator(md=_md)
    def hw_scanspec_fly() -> MsgGenerator:
        # yield from setup_detectors
        yield from bps.declare_stream(*sw_dets, name="sw")
        yield from bps.declare_stream(flyer, name="hw")
        for point in sw_spec.midpoints():
            # Move flyer to start too
            point[flyer] = hw_spec
            # TODO: need to make pos_cache optional in this func
            yield from bps.move_per_step(point, dict())
            yield from bps.trigger_and_read(sw_dets)
            yield from bps.checkpoint()
            yield from fly_and_collect(flyer, checkpoint_every_collect=True)

    return (yield from hw_scanspec_fly())


def _scanspec_to_cycler(spec: Spec[str], axes: Mapping[str, Movable]) -> Cycler:
    """
    Convert a scanspec to a cycler for compatibility with legacy Bluesky plans such as
    `bp.scan_nd`. Use the midpoints of the scanspec since cyclers are normally used
    for software triggered scans.

    Args:
        spec: A scanspec
        axes: Names and axes to move

    Returns:
        Cycler: A new cycler
    """

    midpoints = spec.frames().midpoints
    midpoints = {axes[name]: points for name, points in midpoints.items()}

    # Need to "add" the cyclers for all the axes together. The code below is
    # effectively: cycler(motor1, [...]) + cycler(motor2, [...]) + ...
    return reduce(operator.add, map(lambda args: cycler(*args), midpoints.items()))
