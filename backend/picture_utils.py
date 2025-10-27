"""
Utility functions for managing character pictures
"""
import os
import random
from typing import Optional
from pathlib import Path


class PictureManager:
    """Manages character pictures for different genders"""

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize the picture manager

        Args:
            base_path: Base directory containing picture folders (defaults to project_root/pictures)
        """
        if base_path is None:
            # Get the project root directory (parent of backend/)
            project_root = Path(__file__).parent.parent
            self.base_path = project_root / "pictures"
        else:
            self.base_path = Path(base_path)

        self.female_path = self.base_path / "female"
        self.male_path = self.base_path / "male"

        # Debug logging
        print(f"📁 PictureManager initialized:")
        print(f"   Base path: {self.base_path}")
        print(f"   Female path exists: {self.female_path.exists()}")
        print(f"   Male path exists: {self.male_path.exists()}")

    def get_random_picture(self, gender: str) -> Optional[str]:
        """
        Get a random picture path based on character gender

        Args:
            gender: Character gender (男/女)

        Returns:
            Relative path to a random picture, or None if no pictures found
        """
        # Determine which folder to use based on gender
        if gender == "女":
            picture_dir = self.female_path
            gender_folder = "female"
        elif gender == "男":
            picture_dir = self.male_path
            gender_folder = "male"
        else:
            return None

        # Check if directory exists
        if not picture_dir.exists():
            print(f"⚠️ Warning: Picture directory {picture_dir} does not exist")
            return None

        # Get all image files (common extensions)
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        try:
            pictures = [
                f for f in os.listdir(picture_dir)
                if Path(f).suffix.lower() in image_extensions
            ]
        except Exception as e:
            print(f"❌ Error listing directory {picture_dir}: {e}")
            return None

        if not pictures:
            print(f"⚠️ Warning: No pictures found in {picture_dir}")
            return None

        # Select a random picture
        random_picture = random.choice(pictures)

        # Return the URL path (relative to the static files mount)
        picture_url = f"/pictures/{gender_folder}/{random_picture}"
        print(f"🖼️ Selected picture for {gender}: {picture_url}")
        return picture_url

    def picture_exists(self, gender: str) -> bool:
        """
        Check if pictures exist for the given gender

        Args:
            gender: Character gender (男/女)

        Returns:
            True if pictures exist, False otherwise
        """
        if gender == "女":
            picture_dir = self.female_path
        elif gender == "男":
            picture_dir = self.male_path
        else:
            return False

        if not picture_dir.exists():
            return False

        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        pictures = [
            f for f in os.listdir(picture_dir)
            if Path(f).suffix.lower() in image_extensions
        ]

        return len(pictures) > 0


# Global instance
picture_manager = PictureManager()
