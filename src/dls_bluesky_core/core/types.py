from functools import wraps
from typing import Any, Callable, Generator, Optional, TypeVar, TypedDict

from bluesky import Msg
from pydantic import BaseModel

#  'A true "plan", usually the output of a generator function'
MsgGenerator = Generator[Msg, Any, None]
#  'A function that generates a plan'
PlanGenerator = Callable[..., MsgGenerator]


class SampleMetadata(BaseModel):
    """Definition of schema relating to sample metadata."""

    name: Optional[str]
    chemical_formula: Optional[str]


class MetadataWithSampleInfo(TypedDict, total=False):
    sample: SampleMetadata


T = TypeVar("T")


def with_sample_information(
    callable: Callable[..., T]
) -> Callable[[..., Optional[SampleMetadata]], T]:
    @wraps(callable, updated=["__dict__"])
    def wrapped_callable(*args, **kwargs) -> T:
        sample = kwargs.get("metadata", {}).get("sample", {})
        sa = SampleMetadata(**sample)
        kwargs.setdefault("metadata", {})["sample"] = sa
        return callable(*args, **kwargs)

    return wrapped_callable
