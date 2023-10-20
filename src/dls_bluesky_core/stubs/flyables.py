import bluesky.plan_stubs as bps
from bluesky.protocols import Flyable

from dls_bluesky_core.core import MsgGenerator, group_uuid


def fly_and_collect(
    flyer: Flyable,
    flush_period: float = 0.5,
    checkpoint_every_collect: bool = False,
    stream_name: str = "primary",
) -> MsgGenerator:
    yield from bps.kickoff(flyer)
    complete_group = group_uuid("complete")
    yield from bps.complete(flyer, group=complete_group)
    done = False
    while not done:
        try:
            yield from bps.wait(group=complete_group, timeout=flush_period)
        except TimeoutError:
            pass
        else:
            done = True
        yield from bps.collect(
            flyer, stream=True, return_payload=False, name=stream_name
        )
        if checkpoint_every_collect:
            yield from bps.checkpoint()
