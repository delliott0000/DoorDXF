from __future__ import annotations

from typing import TYPE_CHECKING

from src.resources.constants import Colour

if TYPE_CHECKING:
    from src.resources.types import Dim2, Modelspace


def draw_rectangle(
    msp: Modelspace, origin: Dim2, w: float, h: float, /, *, color: int = Colour.PLAIN
) -> None:
    msp.add_lwpolyline(
        (
            origin,
            (origin[0] + w, origin[1]),
            (origin[0] + w, origin[1] + h),
            (origin[0], origin[1] + h),
        ),
        close=True,
    ).dxf.color = color
