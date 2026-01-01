"""Configuration loader utility."""

import os
import yaml
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config file (optional)

    Returns:
        Configuration dictionary
    """
    if not config_path:
        config_path = os.path.join(
            os.path.dirname(__file__), "../../config/config.yaml"
        )

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config
