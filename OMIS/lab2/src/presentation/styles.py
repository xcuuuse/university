DARK_BLUE = "#1A00A8"
BUTTON_BLUE = "#5470FF"
BUTTON_DISABLED = "#A9B5F7"
CARD_GREY = "#C8D0DA"
TEXT_DARK = "#2B2B33"
TEXT_LIGHT = "#FFFFFF"
OVERLAY_RGBA = (26, 0, 168, 150)

STATUS_COLORS = {
    "free": BUTTON_BLUE,
    "booked": "#F5A623",
    "occupied": "#8A8FA8",
}

STATUS_TEXT = {
    "free": "СВОБОДНО",
    "booked": "ЗАБРОНИРОВАНО",
    "occupied": "ЗАНЯТО",
}

DARK_BACKGROUND = f"background-color: {DARK_BLUE};"

CARD_STYLE = f"""
    QFrame#card {{
        background-color: {CARD_GREY};
        border-radius: 18px;
    }}
    QFrame#card QLabel {{
        color: {TEXT_DARK};
        background: transparent;
    }}
"""


def format_datetime(value) -> str:
    return value.strftime("%d.%m.%Y %H:%M")


def format_price(value: float) -> str:
    return f"{value:g} р/ч"


def format_duration(hours: float) -> str:
    total_minutes = int(hours * 60)
    return f"{total_minutes // 60} ч {total_minutes % 60:02d} мин"