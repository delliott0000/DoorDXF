from __future__ import annotations

from typing import TYPE_CHECKING

from src.resources.constants import CUTOUT_INSET

if TYPE_CHECKING:
    from src.resources.types import Dim2


metal_sheet_sizes: dict[float, tuple[Dim2, ...]] = {
    1.2: (
        (1000, 2100),
        (1000, 2500),
        (1250, 2100),
        (1250, 2500),
        (1250, 3000),
        (1500, 2100),
        (1500, 2500),
        (1500, 3000),
    ),
    1.5: (
        (1000, 2500),
        (1250, 2200),
        (1250, 2500),
        (1250, 3000),
    ),
    2: ((1250, 2500),),
    3: ((1250, 2500),),
    5: ((1250, 2500),),
    8: ((1250, 2500),),
}


def sheet_from_cut_out(cut_out: Dim2 | None, thickness: float, /) -> Dim2 | None:
    if cut_out is None:
        return None
    for sheet_size in metal_sheet_sizes[thickness]:
        if (
            cut_out[0] + CUTOUT_INSET * 2 <= sheet_size[0]
            and cut_out[1] + CUTOUT_INSET * 2 <= sheet_size[1]
        ):
            return sheet_size
    else:
        raise ValueError(
            f"No available sheet sizes for a {cut_out[0]}*{cut_out[1]}*{thickness} cut out."
        )
