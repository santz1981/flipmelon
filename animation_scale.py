"""Deterministic responsive logo sizing for a fullscreen FlipmelonOS animation."""

def logo_width(screen_width: int, screen_height: int) -> int:
    """Reference: 500 px at 1920 x 1080; contain within the viewport."""
    if screen_width <= 0 or screen_height <= 0:
        raise ValueError("Screen dimensions must be positive")
    return round(500 * min(screen_width / 1920, screen_height / 1080))


def logo_height(screen_width: int, screen_height: int) -> int:
    """Original 1400x300 Lottie composition aspect ratio."""
    return round(logo_width(screen_width, screen_height) * 300 / 1400)
