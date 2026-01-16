"""Module containing logic for working with palettes."""
import json
from pathlib import Path
from typing import Any
from typing import Literal
from typing import Optional
from typing import cast

import cv2
import numpy as np

from PIL import Image
from Pylette import Color
from Pylette import Palette
from Pylette import batch_extract_colors
from Pylette import extract_colors
from Pylette.src.types import BatchResult
from Pylette.src.types import ColorSpace

from avulto import DMI
from avulto import Dir
from avulto import IconState
from platformdirs import user_cache_path
from tqdm import tqdm

from dmi_palette._typing import RGB
from dmi_palette.constants import USER_CACHE_FOLDER
from dmi_palette.constants import USER_RUNTIME_FOLDER
from dmi_palette.dmi import ExtractedFrame
from dmi_palette.dmi import extract_frames
from dmi_palette.dmi import get_img_palette


BACKGROUND_COLOR: tuple[int, int, int] = (192, 192, 192)


def batch_extract_icon_frame_palettes(path: Path, max_colors: int = 64, **kwargs: Any) -> list[Palette]:
    frames: list[ExtractedFrame] = extract_frames(path=path)
    images: list[Image.Image] = [frame.to_image() for frame in frames]

    for frame in frames:
        img: Image.Image = frame.to_image()
        images.append(img)

    batch_dmi_to_colors()


# def batch_extract_icon_frame_palettes(root: Path, path: Path) -> list[Palette]:
#     frames: list[ExtractedFrame] = extract_frames(path=path)
#     cached_paths: list[Path] = []
#     relative_base: Path = path.relative_to(root).with_suffix("")
#
#     images: list[Image.Image] = []
#     for frame in frames:
#         # frame_path: Path = Path(USER_CACHE_FOLDER, relative_base, frame.get_relative_slug()).with_suffix(".png")
#         # frame_path.parent.mkdir(parents=True, exist_ok=True)
#         img: Image.Image = frame.to_image()
#         images.append(img)
#         # img.save(frame_path)
#         # cached_paths.append(frame_path)
#     results: list[BatchResult] = batch_extract_colors(images=images, palette_size=16)
#     return [result.palette for result in results if result.palette is not None]


def get_palettes() -> None:
    outputs_folder: Path = USER_CACHE_FOLDER / "outputs"
    paths: list[Path] = list(outputs_folder.rglob("*.png"))
    results: list[BatchResult] = batch_extract_colors(images=paths, palette_size=16)
    for result in results:
        if result.palette is not None:
            palette: Palette = result.palette

            palette_path: Path = result.source.relative_to()
            palette.save()


def get_frame_palette(frame: ExtractedFrame) -> Optional[Palette]:
    """Returns a Palette made from the provided ExtractedFrame."""
    try:
        return frame.to_palette(max_colors=64)
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    icons_folder: Path = Path(r"C:\Users\56kyl\source\repos\goonstation\icons")
    chicken_path: Path = icons_folder / "mob" / "chicken.dmi"
    hand_tools_path: Path = icons_folder / "mob" / "inhand" / "hand_tools.dmi"
    multitool_path: Path = icons_folder / "mob" / "inhand" / "tools" / "multitool.dmi"
    tools_folder: Path = icons_folder / "mob" / "inhand"
    spell_buttons: Path = icons_folder / "mob" / "spell_buttons.dmi"

    output_path: Path = USER_CACHE_FOLDER / "output"

    icon_paths: list[Path] = list(icons_folder.rglob("*.dmi"))
    for path in tqdm(icon_paths):
        img: Image.Image = Image.open(str(path)).convert("RGBA")
        try:
            batch_extract_icon_frame_palettes(root=icons_folder, path=path)
        except Exception as e:
            print(e)
