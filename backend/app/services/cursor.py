import base64
import json
from dataclasses import dataclass
from datetime import datetime

from fastapi import HTTPException, status


@dataclass(frozen=True)
class CursorPayload:
    last_updated_at: datetime
    last_id: int
    fence_updated_at: datetime
    fence_id: int
    category: str | None


def encode_cursor(payload: CursorPayload) -> str:
    data = {
        "last_updated_at": payload.last_updated_at.isoformat(),
        "last_id": payload.last_id,
        "fence_updated_at": payload.fence_updated_at.isoformat(),
        "fence_id": payload.fence_id,
        "category": payload.category,
    }
    raw = json.dumps(data, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_cursor(cursor: str) -> CursorPayload:
    try:
        padded = cursor + ("=" * (-len(cursor) % 4))
        data = json.loads(base64.urlsafe_b64decode(padded.encode("ascii")))
        return CursorPayload(
            last_updated_at=datetime.fromisoformat(data["last_updated_at"]),
            last_id=int(data["last_id"]),
            fence_updated_at=datetime.fromisoformat(data["fence_updated_at"]),
            fence_id=int(data["fence_id"]),
            category=data.get("category"),
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid cursor.",
        ) from exc

