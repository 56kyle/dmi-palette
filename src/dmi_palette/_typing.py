"""Module containing custom types used throughout the dmi_palette package."""
from typing import Literal
from typing import TypeAlias

import numpy as np


ColorRGB: TypeAlias = np.ndarray[tuple[Literal[3]], np.dtype[np.uint8]]
ImgRGB: TypeAlias = np.ndarray[tuple[int, int, Literal[3]], np.dtype[np.uint8]]
