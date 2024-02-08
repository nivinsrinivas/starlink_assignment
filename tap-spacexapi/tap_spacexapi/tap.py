"""SpaceXAPI tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# Import your custom stream types here:
from tap_spacexapi.streams import SpaceXAPIStream, StarlinkStream

STREAM_TYPES = [StarlinkStream]



class TapSpaceXAPI(Tap):
    """SpaceXAPI tap class."""

    name = "tap-spacexapi"

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""

        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
