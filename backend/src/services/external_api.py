import httpx
from loguru import logger

from core.config import settings


class CatAPIService:
    """Service for interacting with TheCatAPI."""

    def __init__(self) -> None:
        self.base_url = settings.cat_api_url
        self.timeout = 10.0

    async def validate_breed(self, breed: str) -> bool:
        """Validate cat breed using TheCatAPI."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url)
                response.raise_for_status()

                breeds = response.json()

                breed_lower = breed.lower()
                valid_breeds = {
                    b.get("name", "").lower() for b in breeds if isinstance(b, dict)
                }

                is_valid = breed_lower in valid_breeds

                if not is_valid:
                    logger.warning(f"Invalid breed '{breed}' not found in TheCatAPI")

                return is_valid

        except httpx.TimeoutException:
            logger.error(f"Timeout while validating breed '{breed}' with TheCatAPI")
            return True

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while validating breed '{breed}': {e}")
            return True

        except Exception as e:
            logger.error(f"Unexpected error while validating breed '{breed}': {e}")
            return True

    async def get_all_breeds(self) -> list[dict]:
        """Get all available cat breeds."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url)
                response.raise_for_status()
                return response.json()

        except Exception as e:
            logger.error(f"Error fetching cat breeds: {e}")
            return []
