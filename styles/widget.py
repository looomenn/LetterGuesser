""" Widget-related variables """

# --------- Button ---------
BUTTON_HEIGHT: int = 40
BUTTON_WIDTH: int = 200

# widget/button/default
BUTTON_DEFAULT_FG_COLOR = ("#FCFCFC", "#1F2023")
BUTTON_DEFAULT_TEXT = ('#1A1A1A', '#FFFFFF')
BUTTON_DEFAULT_BORDER = ('#E1E1E2', "#3D3D3D")

BUTTON_DEFAULT_FG_COLOR_HOVER = ("#E1E1E2", "#272d35")
BUTTON_DEFAULT_BORDER_HOVER = BUTTON_DEFAULT_BORDER

BUTTON_DEFAULT_FG_COLOR_DISABLED = ("#FCFCFC", "#333333")
BUTTON_DEFAULT_TEXT_DISABLED = ('#CDCDCE', '#585858')
BUTTON_DEFAULT_BORDER_DISABLED = ('#D0D7DE', "#30363D")

# widget/button/primary
BUTTON_PRIMARY_FG_COLOR = ("#2463EB", "#50A1FF")
BUTTON_PRIMARY_TEXT = ('#FFFFFF', '#141414')
BUTTON_PRIMARY_BORDER = ('#235ad1', "#65acff")

BUTTON_PRIMARY_FG_COLOR_HOVER = ("#357AE9", "#2C87F6")
BUTTON_PRIMARY_BORDER_HOVERED = ('#2463EB', "#52A3FF")

BUTTON_PRIMARY_FG_COLOR_DISABLED = ("#F4F4F5", "#333333")
BUTTON_PRIMARY_TEXT_DISABLED = ('#CDCDCE', '#585858')
BUTTON_PRIMARY_BORDER_DISABLED = BUTTON_PRIMARY_FG_COLOR_DISABLED

# widget/button/danger
BUTTON_DANGER_FG_COLOR = ('#DC2828', '#FF9494')
BUTTON_DANGER_TEXT = ('#FFFFFF', '#141414')
BUTTON_DANGER_BORDER = BUTTON_DANGER_FG_COLOR

BUTTON_DANGER_FG_COLOR_HOVER = ("#FF6565", "#FA4D4D")
BUTTON_DANGER_BORDER_HOVER = BUTTON_DEFAULT_FG_COLOR_HOVER

BUTTON_DANGER_FG_COLOR_DISABLED = ("#F4F4F5", "#333333")
BUTTON_DANGER_TEXT_DISABLED = ('#CDCDCE', '#585858')
BUTTON_DANGER_BORDER_DISABLED = BUTTON_DEFAULT_FG_COLOR
