from __future__ import annotations

from typing import TYPE_CHECKING

import ezdxf as dxflib

from src.core.bom import sheet_from_cut_out
from src.resources.constants import CUTOUT_INSET, Colour

if TYPE_CHECKING:
    from src.core.doorset import DoorSet
    from src.resources.types import Dim2, DXFRule, Modelspace


# # # # # # # # # #
# HELPER FUNCTIONS
# # # # # # # # # #


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


# # # # # # # # # #
# DXF RULE TRACKER
# # # # # # # # # #


class DXFRuleManager:
    front_active_rules: list[DXFRule] = []
    rear_active_rules: list[DXFRule] = []
    front_passive_rules: list[DXFRule] = []
    rear_passive_rules: list[DXFRule] = []

    @classmethod
    def front_active(cls, func: DXFRule, /) -> DXFRule:
        cls.front_active_rules.append(func)
        return func

    @classmethod
    def rear_active(cls, func: DXFRule, /) -> DXFRule:
        cls.rear_active_rules.append(func)
        return func

    @classmethod
    def front_passive(cls, func: DXFRule, /) -> DXFRule:
        cls.front_passive_rules.append(func)
        return func

    @classmethod
    def rear_passive(cls, func: DXFRule, /) -> DXFRule:
        cls.rear_passive_rules.append(func)
        return func


# # # # # # # # # #
# DXF RULES
# # # # # # # # # #


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


# # # # # # # # # #
# DRAW DXFS
# # # # # # # # # #


def draw_dxfs(door: DoorSet, /) -> None:
    struct = {
        name: {
            "cutout": getattr(door, f"{name}_leaf_cutout"),
            "thickness": door.leaf_thickness,
            "rules": getattr(DXFRuleManager, f"{name}_rules"),
        }
        for name in ("front_active", "rear_active", "front_passive", "rear_passive")
    }

    for name, guide in struct.items():
        cutout = guide["cutout"]
        sheet = sheet_from_cut_out(cutout, guide["thickness"])
        rules = guide["rules"]

        if cutout is None or sheet is None:
            continue

        document = dxflib.new("R2010")
        msp = document.modelspace()

        # Sheet Edges (for reference; to be ignored when cutting)
        draw_rectangle(msp, (0, 0), *sheet, color=Colour.RED)  # type: ignore
        # Cutout edges
        draw_rectangle(msp, (CUTOUT_INSET, CUTOUT_INSET), *cutout)  # type: ignore

        for rule in rules:
            rule(door, msp)

        document.saveas(f"output/{name}.dxf")
