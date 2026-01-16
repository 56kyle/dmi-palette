"""Module containing constants used throughout the dmi_palette package."""
from pathlib import Path

from platformdirs import user_cache_path
from platformdirs import user_config_path
from platformdirs import user_log_path
from platformdirs import user_runtime_path


FILE_SAFE_DATETIME_FORMAT: str = "%Y-%m-%d_%H-%M-%S"


APP_NAME: str = "dmi-palette"
APP_AUTHOR: str = "56kyle"


USER_CONFIG_FOLDER: Path = user_config_path(appname=APP_NAME, appauthor=APP_AUTHOR, ensure_exists=True)
USER_CACHE_FOLDER: Path = user_cache_path(appname=APP_NAME, appauthor=APP_AUTHOR, ensure_exists=True)
USER_RUNTIME_FOLDER: Path = user_runtime_path(appname=APP_NAME, appauthor=APP_AUTHOR, ensure_exists=True)
USER_LOG_FOLDER: Path = user_log_path(appname=APP_NAME, appauthor=APP_AUTHOR, ensure_exists=True)
