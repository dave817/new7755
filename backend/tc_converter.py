"""
Traditional Chinese Converter
Uses OpenCC to ensure all chatbot messages are in Traditional Chinese
"""
from typing import Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Global converter instance
_converter = None


def get_converter():
    """
    Get or initialize the OpenCC converter (Simplified to Traditional Chinese)

    Returns:
        OpenCC converter instance or None if initialization fails
    """
    global _converter

    if _converter is not None:
        return _converter

    try:
        from opencc import OpenCC
        # s2twp: Simplified Chinese to Traditional Chinese (Taiwan standard with phrases)
        # This is the most comprehensive conversion for Traditional Chinese
        _converter = OpenCC('s2twp')
        logger.info("OpenCC converter initialized successfully")
        return _converter
    except ImportError:
        logger.warning(
            "OpenCC not installed. Please run 'pip install opencc-python-reimplemented' "
            "or use setup.bat to install dependencies."
        )
        return None
    except Exception as e:
        logger.error(f"Failed to initialize OpenCC converter: {e}")
        return None


def convert_to_traditional(text: Optional[str]) -> str:
    """
    Convert any Simplified Chinese text to Traditional Chinese

    Args:
        text: Text that may contain Simplified Chinese

    Returns:
        Text converted to Traditional Chinese (if converter is available),
        otherwise returns original text
    """
    if not text:
        return text or ""

    converter = get_converter()
    if converter is None:
        # If OpenCC is not available, return original text
        logger.debug("Converter not available, returning original text")
        return text

    try:
        # Convert the text
        converted = converter.convert(text)

        # Log if conversion made changes (helpful for debugging)
        if converted != text:
            logger.debug(f"Converted text: {len(text)} -> {len(converted)} chars")

        return converted
    except Exception as e:
        logger.error(f"Error converting text: {e}")
        # Return original text if conversion fails
        return text


def ensure_traditional_chinese(func):
    """
    Decorator to automatically convert function return values to Traditional Chinese

    Usage:
        @ensure_traditional_chinese
        def generate_message():
            return "some text that might be in simplified chinese"
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # Handle string returns
        if isinstance(result, str):
            return convert_to_traditional(result)

        # Handle dict returns (convert all string values)
        elif isinstance(result, dict):
            return {
                key: convert_to_traditional(value) if isinstance(value, str) else value
                for key, value in result.items()
            }

        # Return as-is for other types
        return result

    return wrapper
