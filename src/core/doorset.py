from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from src.resources.types import Dim2


class DoorType(Enum):
    Single = 0
    Double = 1


class DoorSet:

    def __init__(self, **kwargs: Any):
        self.__door_type = DoorType(kwargs.get("door_type", DoorType.Single))

        self.__so_x: float = kwargs.get("so_x", 1000)
        self.__so_y: float = kwargs.get("so_y", 2100)

        if self.__door_type == DoorType.Double:
            self.__leaf_split = (self.leaf_sum_x / 2, self.leaf_sum_x / 2)
        else:
            self.__leaf_split = None

        self.frame_thickness: float = kwargs.get("frame_thickness", 1.5)
        self.leaf_thickness: float = kwargs.get("leaf_thickness", 1.2)

    @property
    def so_x(self) -> float:
        return self.__so_x

    @so_x.setter
    def so_x(self, value: float):
        self.__so_x = value
        if self.__door_type == DoorType.Double:
            self.__leaf_split = (self.leaf_sum_x / 2, self.leaf_sum_x / 2)

    @property
    def so_y(self) -> float:
        return self.__so_y

    @so_y.setter
    def so_y(self, value: float):
        self.__so_y = value

    @property
    def frame_so_diff_x(self) -> float:
        return 15

    @property
    def frame_so_diff_y(self) -> float:
        return 10

    @property
    def leaf_sum_frame_diff_x(self) -> float:
        if self.__door_type == DoorType.Single:
            return 92
        else:
            return 95

    @property
    def leaf_sum_frame_diff_y(self) -> float:
        return 50

    @property
    def frame_x(self) -> float:
        return self.so_x - self.frame_so_diff_x

    @frame_x.setter
    def frame_x(self, value: float):
        self.so_x = value + self.frame_so_diff_x

    @property
    def frame_y(self) -> float:
        return self.so_y - self.frame_so_diff_y

    @frame_y.setter
    def frame_y(self, value: float):
        self.so_y = value + self.frame_so_diff_y

    @property
    def leaf_sum_x(self) -> float:
        return self.frame_x - self.leaf_sum_frame_diff_x

    @property
    def active_leaf_x(self) -> float:
        if self.__door_type == DoorType.Single:
            return self.leaf_sum_x
        else:
            return self.__leaf_split[0]

    @active_leaf_x.setter
    def active_leaf_x(self, value: float):
        if self.__door_type == DoorType.Single:
            self.so_x = value + self.leaf_sum_frame_diff_x + self.frame_so_diff_x
        elif value >= self.leaf_sum_x:
            raise ValueError("Active leaf width value out of range.")
        else:
            self.__leaf_split = value, self.leaf_sum_x - value

    @property
    def active_leaf_y(self) -> float:
        return self.frame_y - self.leaf_sum_frame_diff_y

    @property
    def passive_leaf_x(self) -> float | None:
        if self.__door_type == DoorType.Double:
            return self.__leaf_split[1]

    @passive_leaf_x.setter
    def passive_leaf_x(self, value: float):
        if self.__door_type == DoorType.Single:
            pass
        elif value >= self.leaf_sum_x:
            raise ValueError("Passive leaf width value out of range.")
        else:
            self.__leaf_split = self.leaf_sum_x - value, value

    @property
    def passive_leaf_y(self) -> float | None:
        if self.__door_type == DoorType.Double:
            return self.frame_y - self.leaf_sum_frame_diff_y

    @property
    def front_active_leaf_cutout(self) -> Dim2:
        return self.active_leaf_x + 120, self.active_leaf_y

    @property
    def rear_active_leaf_cutout(self) -> Dim2:
        return self.active_leaf_x + 87, self.active_leaf_y

    @property
    def front_passive_leaf_cutout(self) -> Dim2 | None:
        try:
            return self.passive_leaf_x + 148, self.passive_leaf_y
        except TypeError:
            return

    @property
    def rear_passive_leaf_cutout(self) -> Dim2 | None:
        try:
            return self.passive_leaf_x + 59, self.passive_leaf_y
        except TypeError:
            return
