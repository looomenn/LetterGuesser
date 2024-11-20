"""
Font settings and text sizes for LetterGuesser.

Defines font types, sizes, and line heights used across the application,
ensuring consistency and readability in the UI.
"""

font_base: int = 16
fonts: dict = {
    'fontStack_system': "'SF Pro Text', "
                        "'Segoe UI', "
                        "'Noto Sans', "
                        "'Helvetica', "
                        "'Arial', 'sans-serif'",
    'text_title_weight_large': 600,
    'text_title_weight_medium': 600,
    'text_title_weight_small': 600,
    'text_title_size_large': f'{font_base * 2}px',
    'text_title_size_medium': f'{font_base * 2}px',
    'text_title_size_small': f'{font_base * 1}px',
    'text_body_size_large': f"{font_base * 1}px",
    'text_body_size_medium': f"{font_base * 0.875}px",
    'text_body_size_small': f"{font_base * 0.75}px"
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
