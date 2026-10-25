"""Conversion between RLBot controller values and Rocket League input bytes."""

from __future__ import annotations

import struct
from typing import Protocol


class ControllerState(Protocol):
    """The controller fields consumed by Rocket League's FVehicleInputs."""

    throttle: float
    steer: float
    pitch: float
    yaw: float
    roll: float
    handbrake: bool
    jump: bool
    boost: bool
    use_item: bool


def controller_to_input(controller: ControllerState) -> bytearray:
    """Encode a controller state as the 32-byte FVehicleInputs layout.

    The layout and the target address are game-build-dependent. This function
    only serializes the supplied values; it never reads or writes process memory.
    """

    inputs = bytearray(32)
    inputs[0:4] = struct.pack("<f", controller.throttle)
    inputs[4:8] = struct.pack("<f", controller.steer)
    inputs[8:12] = struct.pack("<f", controller.pitch)
    inputs[12:16] = struct.pack("<f", controller.yaw)
    inputs[16:20] = struct.pack("<f", controller.roll)
    inputs[20:24] = struct.pack("<f", -controller.pitch)
    inputs[24:28] = struct.pack("<f", controller.yaw)

    flags = 0
    flags |= int(bool(controller.handbrake)) << 0
    flags |= int(bool(controller.jump)) << 1
    flags |= int(bool(controller.boost)) << 2
    flags |= int(bool(controller.boost)) << 3
    flags |= int(bool(getattr(controller, "use_item", False))) << 4
    inputs[28:32] = struct.pack("<I", flags)

    return inputs
