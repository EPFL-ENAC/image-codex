"""
Shared constants and functions
"""
from typing import Tuple, Optional

from .cloudinary import *  # noqa: F401,F403
from .fastapi import *  # noqa: F401,F403
from .pil import *  # noqa: F401,F403


def map_dms_to_dd(dms: Optional[Tuple[float, float, float]], ref: Optional[str]) -> Optional[float]:
    """
    Convert degrees, minutes, seconds (DMS) coordinates to decimal degrees (DD)
    """
    if ref is None or dms is None:
        return None

    sign = -1 if ref == 'S' or ref == 'W' else 1
    return sign * (float(dms[0]) + float(dms[1])/60.0 + float(dms[2])/3600.0)
