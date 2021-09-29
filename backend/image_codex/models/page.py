from __future__ import annotations

from typing import Generic, Optional, Sequence, TypeVar

from fastapi.param_functions import Query
from fastapi_pagination.bases import AbstractParams, BasePage, RawParams
from pydantic.main import BaseModel
from pydantic.types import conint

T = TypeVar("T")


class CursorParams(BaseModel, AbstractParams):
    next: Optional[str] = Query(None, description="Next cursor")
    size: int = Query(50, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size,
        )


class CursorPage(BasePage[T], Generic[T]):
    next: Optional[str]
    size: conint(ge=1)  # type: ignore

    __params_type__ = CursorParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: CursorParams,
    ) -> CursorPage[T]:
        return cls(
            total=total,
            items=items,
            next=params.next,
            size=params.size,
        )
