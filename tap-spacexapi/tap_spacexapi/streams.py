"""Stream type classes for tap-spacexapi."""

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_spacexapi.client import SpaceXAPIStream


class StarlinkStream(SpaceXAPIStream):
    """Define custom stream."""
    path = '/starlink'  
    name = "starlink"
    schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("launch", th.StringType),
    th.Property("version", th.StringType),
    th.Property("spaceTrack", th.ObjectType(
        th.Property("OBJECT_ID", th.StringType),
        th.Property("OBJECT_NAME", th.StringType),
        th.Property("CREATION_DATE", th.StringType),
        th.Property("LAUNCH_DATE", th.StringType),
        th.Property("EPOCH", th.StringType),
        th.Property("TIME_SYSTEM", th.StringType),
        th.Property("COUNTRY_CODE", th.StringType),
        th.Property("OBJECT_TYPE", th.StringType),
    ))
).to_dict()