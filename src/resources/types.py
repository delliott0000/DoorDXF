from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from ezdxf.layouts import Modelspace

    from src.core.doorset import DoorSet

    Dim2 = tuple[float, float]
    DXFRule = Callable[[DoorSet, Modelspace], None]
