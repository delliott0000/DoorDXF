from __future__ import annotations

from typing import TYPE_CHECKING

from src.core.dxf_utils import draw_rectangle
from src.resources.constants import CUTOUT_INSET

if TYPE_CHECKING:
    from src.core.doorset import DoorSet
    from src.resources.types import DXFRule, Modelspace


class DXFRuleManager:
    front_active_rules: list[DXFRule] = []
    rear_active_rules: list[DXFRule] = []
    front_passive_rules: list[DXFRule] = []
    rear_passive_rules: list[DXFRule] = []

    @classmethod
    def front_active(cls, func: DXFRule, /):
        cls.front_active_rules.append(func)

    @classmethod
    def rear_active(cls, func: DXFRule, /):
        cls.rear_active_rules.append(func)

    @classmethod
    def front_passive(cls, func: DXFRule, /):
        cls.front_passive_rules.append(func)

    @classmethod
    def rear_passive(cls, func: DXFRule, /):
        cls.rear_passive_rules.append(func)


@DXFRuleManager.front_active
def hinges(door: DoorSet, msp: Modelspace, /) -> None:
    w, h = 30, 80
    inset_x, inset_y = 40, 100

    # Top
    draw_rectangle(msp, (CUTOUT_INSET + inset_x, CUTOUT_INSET + inset_y), w, h)
    # Bottom
    draw_rectangle(
        msp,
        (CUTOUT_INSET + inset_x, CUTOUT_INSET + door.active_leaf_y - inset_y - h),
        w,
        h,
    )
    # Centre
    draw_rectangle(
        msp, (CUTOUT_INSET + inset_x, CUTOUT_INSET + (door.active_leaf_y - h) / 2), w, h
    )
