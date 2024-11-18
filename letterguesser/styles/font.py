"""
Font settings and text sizes for LetterGuesser.

Defines font types, sizes, and line heights used across the application,
ensuring consistency and readability in the UI.
"""

font_base: int = 16

fonts: dict = {
    'fontStack-system': "'Segoe UI', 'Noto Sans', 'Helvetica', 'Arial', 'sans-serif'",
    'text-title-weight-large': 600,
    'text-title-weight-medium': 600,
    'text-title-weight-small': 600,
    'text-title-size-large': f'{font_base * 2}px',
    'text-title-size-medium': f'{font_base * 2}px',
    'text-title-size-small': f'{font_base * 1}px',
    'text-body-size-large': f"{font_base * 1}px",
    'text-body-size-medium': f"{font_base * 0.875}px",
    'text-body-size-small': f"{font_base * 0.75}px"
}

# general settings
font: str = "Geist Mono"
text_large: int = 18
text_medium: int = 16
text_small: int = 14

# line-height
height_multiplier: float = 1.3
text_small_height:  int = int(text_small * height_multiplier)
text_medium_height: int = int(text_medium * height_multiplier)
text_large_height:  int = int(text_large * height_multiplier)
