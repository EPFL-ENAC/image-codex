from typing import Optional


def get_format(type: str) -> Optional[str]:
    if type == 'image/jpeg':
        return 'JPEG'
    return None
