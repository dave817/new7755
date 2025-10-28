"""
Text Cleaning Utility for LINE Bot Responses
Removes unwanted action tags and system artifacts while preserving Chinese content
"""

import re
import logging

logger = logging.getLogger(__name__)


def clean_response_text(text: str) -> str:
    """
    Clean AI response text by removing system artifacts and action tags

    Removes:
    - English action tags (teleport, Dampen, iteleport, etc.)
    - Standalone English words at the start of lines
    - System tags and metadata

    Keeps:
    - All Chinese text and descriptions (like 傳送了一個動態表情包...)
    - English names used naturally in conversation
    - Emojis and special characters

    Args:
        text: Raw AI response text

    Returns:
        Cleaned text safe to send to users
    """
    if not text:
        return text

    original_text = text

    # Pattern 1: Remove standalone English words at the start of lines or after newlines
    # Examples: "teleport\n", "Dampen\n", "iteleport\n"
    text = re.sub(r'^[a-zA-Z]+\n', '', text, flags=re.MULTILINE)

    # Pattern 2: Remove English words immediately before opening parenthesis with Chinese
    # Examples: "(teleport", "iteleport(", "Dampen("
    text = re.sub(r'\b[a-zA-Z]+\s*\(', '(', text)

    # Pattern 3: Remove standalone lowercase English action words (but keep proper names like "Dave", "D")
    # This targets words like: teleport, dampen, activate, trigger, etc.
    # Keep: Single capital letters (names like "D") or capitalized words (names like "Dave")
    text = re.sub(r'(?<![a-zA-Z])(?:[a-z]{2,}[a-zA-Z]*)(?![a-zA-Z])', '', text)

    # Pattern 4: Remove common action/system tags that might appear
    # Add more patterns as you discover them
    action_tags = [
        r'\bteleport\b',
        r'\bDampen\b',
        r'\biteleport\b',
        r'\bactivate\b',
        r'\btrigger\b',
        r'\bsummon\b',
        r'\bcast\b',
        r'\binvoke\b',
        r'\bperform\b',
        r'\bexecute\b',
        r'\binitiate\b',
    ]

    for tag in action_tags:
        text = re.sub(tag, '', text, flags=re.IGNORECASE)

    # Pattern 5: Remove extra whitespace created by deletions
    # But preserve intentional spacing in Chinese text
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove multiple blank lines
    text = re.sub(r' +', ' ', text)  # Collapse multiple spaces
    text = text.strip()  # Remove leading/trailing whitespace

    # Pattern 6: Remove any remaining isolated parentheses from incomplete tags
    text = re.sub(r'\(\s*\)', '', text)  # Remove empty parentheses

    # Log if significant cleaning occurred (for debugging)
    if len(original_text) - len(text) > 10:
        logger.info(f"Text cleaning removed {len(original_text) - len(text)} characters")
        logger.debug(f"Original: {original_text[:100]}...")
        logger.debug(f"Cleaned: {text[:100]}...")

    return text


def remove_system_tags(text: str) -> str:
    """
    Remove any XML-like or bracket-based system tags

    Examples: <action>, [system], {metadata}

    Args:
        text: Text that may contain system tags

    Returns:
        Text with system tags removed
    """
    # Remove XML-like tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove square bracket tags (but keep Chinese content in brackets)
    text = re.sub(r'\[[a-zA-Z0-9_]+\]', '', text)

    # Remove curly brace tags
    text = re.sub(r'\{[a-zA-Z0-9_]+\}', '', text)

    return text


def clean_for_line(text: str) -> str:
    """
    Complete cleaning pipeline for LINE messages

    This is the main function to use for cleaning AI responses
    before sending to LINE users

    Args:
        text: Raw AI response

    Returns:
        Fully cleaned text ready for LINE
    """
    # Step 1: Remove system tags
    text = remove_system_tags(text)

    # Step 2: Remove action tags and artifacts
    text = clean_response_text(text)

    # Step 3: Final validation - ensure we have content
    if not text or text.isspace():
        logger.warning("Text cleaning resulted in empty text!")
        return "..."  # Fallback to avoid sending empty message

    return text
