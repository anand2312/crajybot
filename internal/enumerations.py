import enum


class EmbedType(enum.Enum):
    """Enum representing the type of embed being used."""

    FAIL = 0xFF0000  # red
    SUCCESS = 0x32CD32  # lime green
    WARNING = 0xFFFF00  # yellow
    BOT = 0xA9A9A9  # gray
    INFO = 0xF4C2C2  # baby pink


class Table(enum.Enum):
    """Enum for tables in the database."""

    ECONOMY = ("id", "bank", "cash", "debt")
    USER_DETAILS = ("id", "zodiac", "bday")
    INVENTORIES = (
        "id",
        "stock",
        "chicken",
        "heist tools",
    )  # actual name in table is `heist`
    NOTES = ("id", "raw_text")
    SHOP = ("item_id", "item_name", "stock", "price")
    PINS = ("pin_id", "synopsis", "jump_url", "author", "pin_date", "name")
    TAGS = ("tag_name", "tag_content", "tag_author")
    ROLE_NAMES = ("name_id", "role_name", "author")
