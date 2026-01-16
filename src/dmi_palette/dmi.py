"""Module containing logic for working with DMI files throughout the dmi_palette package."""
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any
from typing import Generator
from typing import Iterable
from typing import Optional

from PIL import Image
from Pylette import Palette
from Pylette import extract_colors
from avulto import DMI
from avulto import Dir
from avulto import IconState



DIRECTION_NAMES: dict[Dir, str] = {
    Dir.NORTH: "north",
    Dir.SOUTH: "south",
    Dir.EAST: "east",
    Dir.WEST: "west",
    Dir.NORTHWEST: "northwest",
    Dir.NORTHEAST: "northeast",
    Dir.SOUTHEAST: "southeast",
    Dir.SOUTHWEST: "southwest",
}


@dataclass(frozen=True)
class ExtractedFrame:
    state_name: str
    direction: Dir
    frame: int
    data: bytes
    size: tuple[int, int]

    def get_relative_slug(self) -> Path:
        """Returns a slug path to represent the extracted state direction frame."""
        return Path(self.state_name, f"{self.get_direction_str()}_{self.frame}")

    def get_direction_str(self) -> str:
        """Returns a string representing the direction."""
        return DIRECTION_NAMES[self.direction]

    def to_image(self) -> Image.Image:
        """Returns the current frame as a PIL Image object."""
        return Image.frombytes("RGBA", size=self.size, data=self.data)

    def to_palette(self, max_colors: int, resize: bool = False, **kwargs: Any) -> Palette:
        """Returns the current frame as a color Palette."""
        img: Image.Image = self.to_image()
        return get_img_palette(img=img, max_colors=max_colors, resize=resize, **kwargs)


def get_icon_palette(path: Path, **kwargs: Any) -> Optional[Palette]:
    """Returns a palette for the given icon Image."""
    img: Image.Image = Image.open(path).convert("RGBA")
    return get_img_palette(img=img, **kwargs)



def get_icon_direction_palette(path: Path, direction: Dir, **kwargs: Any) -> Optional[Palette]:
    """Returns a palette for the given icon Image in one orientation across all frames."""
    dmi: DMI = DMI.from_file(str(path))
    img

    for state in dmi.states():
        for extracted_frame in _iter_state_direction_frames(
            state=state, size=(dmi.icon_width, dmi.icon_height), direction=direction
        ):
            extracted_frame.to_palette()



    direction_frames: list[ExtractedFrame] = extract_frames(path=path)
    extracted_frame: ExtractedFrame = _extract_frame(
        state=state,
        direction=direction,
        frame=frame,
        size=(dmi.icon_width, dmi.icon_height),
    )




def _iter_state_direction_frames(
    state: IconState, size: tuple[int, int], direction: Optional[Dir] = None, frame: Optional[int] = None,
) -> Generator[ExtractedFrame, None, None]:
    """Yields extracted frames from the given direction across frames."""
    directions: list[Dir] = state.dirs if direction is None else [direction]
    frames: list[int] = list(range(1, state.frames)) if frame is None else [frame]
    for direction in directions:
        for frame in frames:
            yield _extract_frame(state=state, direction=direction, frame=frame, size=size)


def get_icon_frame_palette(path: Path, frame: int, **kwargs: Any) -> Optional[Palette]:
    """Return a palette for the given icon Image in one frame across all orientations."""
    dmi: DMI = DMI.from_file(str(path))


def get_icon_direction_frame_palette(path: Path, direction: Dir, frame: int, **kwargs: Any) -> Optional[Palette]:
    """Returns a palette for the given icon Image in one orientation on one frame."""


def get_img_palette(img: Image.Image, max_colors: int, resize: bool = False, **kwargs: Any) -> Optional[Palette]:
    """Returns a palette for the given PIL Image."""
    rgb_colors: Optional[list[tuple[int, tuple[int, int, int]]]] = img.convert(mode="RGB").getcolors()
    if rgb_colors is None:
        return None

    # RGB adds a color for transparent portions
    total_colors: int = len(rgb_colors) - 1
    palette_size: int = min(total_colors, max_colors)
    if palette_size == 0:
        return None

    palette: Palette = extract_colors(image=img, palette_size=palette_size, resize=resize, **kwargs)
    return palette






def extract_frames(path: Path, ) -> list[ExtractedFrame]:
    """Extracts all permutations of IconState, direction, and frame from the given DMI file."""
    dmi: DMI = DMI.from_file(path)
    frames: list[ExtractedFrame] = []
    for state in dmi.states():
        for direction in state.dirs:
            for frame in range(1, state.frames + 1):
                extracted_frame: ExtractedFrame = _extract_frame(
                    state=state,
                    direction=direction,
                    frame=frame,
                    size=(dmi.icon_width, dmi.icon_height),
                )
                frames.append(extracted_frame)
    return frames


def _extract_frame(state: IconState, direction: Dir, frame: int, size: tuple[int, int]) -> ExtractedFrame:
    data: bytes = state.data_rgba8(frame, direction)
    return ExtractedFrame(
        state_name=state.name,
        direction=direction,
        frame=frame,
        data=data,
        size=size
    )







