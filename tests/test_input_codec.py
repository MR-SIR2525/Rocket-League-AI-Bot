import struct
import unittest
from types import SimpleNamespace

from rlmarlbot.input_codec import controller_to_input


class ControllerToInputTests(unittest.TestCase):
    def test_encodes_the_documented_32_byte_layout(self):
        controller = SimpleNamespace(
            throttle=1.0,
            steer=-0.5,
            pitch=0.25,
            yaw=-0.75,
            roll=0.125,
            handbrake=True,
            jump=False,
            boost=True,
            use_item=True,
        )

        encoded = controller_to_input(controller)

        self.assertEqual(len(encoded), 32)
        self.assertEqual(
            struct.unpack("<7fI", encoded),
            (1.0, -0.5, 0.25, -0.75, 0.125, -0.25, -0.75, 0b11101),
        )

    def test_use_item_defaults_to_false_for_standard_rlbot_controllers(self):
        controller = SimpleNamespace(
            throttle=0.0,
            steer=0.0,
            pitch=0.0,
            yaw=0.0,
            roll=0.0,
            handbrake=False,
            jump=False,
            boost=False,
        )

        encoded = controller_to_input(controller)

        self.assertEqual(struct.unpack("<I", encoded[28:32])[0], 0)


if __name__ == "__main__":
    unittest.main()
