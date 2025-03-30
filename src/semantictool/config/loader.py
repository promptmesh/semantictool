import os
import httpx
import yaml
from pathlib import Path
from urllib.parse import unquote

from .models import ConfigLocation, config


def file_url_to_path(url: str) -> Path:
    if not url.startswith("file://"):
        raise ValueError("Invalid file URL")

    path = url[7:]

    if os.name == "nt" and path.startswith("/") and path[2:3] == ":":
        path = path[1:]  # Strip extra slash before Windows drive letter

    return Path(unquote(path)).resolve()


def load_config(location: ConfigLocation) -> config:
    url = str(location.path)

    if url.startswith("file://"):
        file_path = file_url_to_path(url)
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with file_path.open('r', encoding='utf-8') as f:
            loaded = yaml.safe_load(f) or {}

    elif url.startswith("http://") or url.startswith("https://"):
        try:
            resp = httpx.get(url, timeout=5.0)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise ConnectionError(f"Failed to fetch config from {url}: {e}")

        loaded = yaml.safe_load(resp.text) or {}

    else:
        raise ValueError(f"Unsupported config URL scheme: {url}")

    return config.model_validate(loaded)


def get_config_location() -> ConfigLocation:
    location = os.getenv("CONFIG_LOCATION", "file:///config.yaml")
    return ConfigLocation.model_validate({"path": location})


CONFIG: config = load_config(get_config_location())