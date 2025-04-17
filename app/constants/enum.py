from enum import Enum


class MessageStatus(str, Enum):
    pass


class TimeZone(Enum):
    ASIA_TOKYO = "Asia/Tokyo"
    ASIA_HO_CHI_MINH = "Asia/Ho_Chi_Minh"
    EUROPE_LONDON = "Europe/London"
    AMERICA_NEW_YORK = "America/New_York"


class MessageType(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    VOICE = "voice"
