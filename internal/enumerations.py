import enum


class EmbedType(enum.Enum):
    """Enum representing the type of embed being used."""
    FAIL = 0xFF0000
    SUCCESS = 0x32CD32
    WARNING = 0xFFFF00
    BOT = 0xA9A9A9


class Table(enum.Enum):
    """Enum for tables in the database."""
    ECONOMY = ("id", "bank", "cash", "debt")
    DETAILS = ("id", "zodiac", "bday")
    INVENTORIES = ("id", "stock", "chicken", "heist tools")    # actual name in table is `heist`
    NOTES = ("id", "raw_text")
    SHOP = ("item_id", "item_name", "stock", "price")
    PINS = ("pin_id", "synopsis", "jump_url", "author", "date", "name")