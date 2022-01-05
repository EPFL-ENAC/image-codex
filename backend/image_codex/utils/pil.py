from typing import Optional


def get_pil_format(mimetype: Optional[str]) -> Optional[str]:
    if mimetype is None:
        return None
    elif mimetype == "image/jpeg":
        return "JPEG"
    elif mimetype == "application/pdf":
        return "PDF"
    return None
