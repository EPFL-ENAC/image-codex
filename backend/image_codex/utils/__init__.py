"""
Shared constants and functions
"""
from .cloudinary import *  # noqa: F401,F403
from .config import *  # noqa: F401,F403
from .fastapi import *  # noqa: F401,F403
from .pil import *  # noqa: F401,F403


def map_dms_to_dd(d: float, m: float, s: float) -> float:
    """
    Convert degrees, minutes, seconds (DMS) coordinates to decimal degrees (DD)
    """
    sign = -1 if d < 0 else 1
    return sign * (float(d) + float(m)/60.0 + float(s)/3600.0)
