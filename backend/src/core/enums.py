from enum import Enum


class Environment(str, Enum):
    """Application environment enum."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
