"""User-facing error messages, in one place.

The exact wording is part of the contract: g07 pins these strings, so a
one-character change has to break a test.
"""


class SampleProjError(Exception):
    """Base class for everything this project raises at its own users."""


class ConfigError(SampleProjError):
    """A configuration value cannot be used."""


class ParseError(SampleProjError):
    """Input did not match the record format."""


#: Message templates. Kept as constants so a test can pin the text without
#: reaching into a formatting call site.
MSG_UNKNOWN_KEY = "unknown config key: {key}"
MSG_NOT_AN_INT = "config value for {key} must be a whole number, got {value!r}"
MSG_EMPTY_RECORD = "record is empty"
MSG_MISSING_SEPARATOR = "record {line!r} has no '=' separator"
MSG_BLANK_FIELD = "record {line!r} has a blank field name"
