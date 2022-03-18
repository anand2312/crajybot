import enum


class EmbedType(enum.Enum):
    """Enum representing the type of embed being used."""

    FAIL = 0xFF0000  # red
    SUCCESS = 0x32CD32  # lime green
    WARNING = 0xFFFF00  # yellow
    BOT = 0xA9A9A9  # gray
    INFO = 0xF4C2C2  # baby pink
