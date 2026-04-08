CENTER_DRILL_PRESETS = {
    "00": {"style": "Plain", "angle": 60.0, "pilot": 0.015625, "body": 0.1250, "pilot_length": 0.015625},
    "0": {"style": "Plain", "angle": 60.0, "pilot": 0.031250, "body": 0.1250, "pilot_length": 0.031250},
    "1": {"style": "Plain", "angle": 60.0, "pilot": 0.046875, "body": 0.1250, "pilot_length": 0.046875},
    "2": {"style": "Plain", "angle": 60.0, "pilot": 0.078125, "body": 0.1875, "pilot_length": 0.078125},
    "3": {"style": "Plain", "angle": 60.0, "pilot": 0.109375, "body": 0.2500, "pilot_length": 0.109375},
    "4": {"style": "Plain", "angle": 60.0, "pilot": 0.125000, "body": 0.3125, "pilot_length": 0.125000},
    "5": {"style": "Plain", "angle": 60.0, "pilot": 0.187500, "body": 0.4375, "pilot_length": 0.187500},
    "6": {"style": "Plain", "angle": 60.0, "pilot": 0.218750, "body": 0.5000, "pilot_length": 0.218750},
    "7": {"style": "Plain", "angle": 60.0, "pilot": 0.250000, "body": 0.6250, "pilot_length": 0.250000},
    "8": {"style": "Plain", "angle": 60.0, "pilot": 0.312500, "body": 0.7500, "pilot_length": 0.312500},
    "9": {"style": "Plain", "angle": 60.0, "pilot": 0.375000, "body": 0.8750, "pilot_length": 0.375000},
    "10": {"style": "Plain", "angle": 60.0, "pilot": 0.500000, "body": 1.2500, "pilot_length": 0.500000},
    "11": {"style": "Bell", "angle": 120.0, "pilot": 0.046875, "body": 0.1250, "bell": 0.1900, "pilot_length": 0.046875},
    "12": {"style": "Bell", "angle": 120.0, "pilot": 0.062500, "body": 0.1875, "bell": 0.2500, "pilot_length": 0.062500},
    "13": {"style": "Bell", "angle": 120.0, "pilot": 0.093750, "body": 0.2500, "bell": 0.3100, "pilot_length": 0.093750},
    "14": {"style": "Bell", "angle": 120.0, "pilot": 0.109375, "body": 0.3125, "bell": 0.4000, "pilot_length": 0.109375},
    "15": {"style": "Bell", "angle": 120.0, "pilot": 0.156250, "body": 0.4375, "bell": 0.5000, "pilot_length": 0.156250},
    "16": {"style": "Bell", "angle": 120.0, "pilot": 0.187500, "body": 0.5000, "bell": 0.5900, "pilot_length": 0.187500},
    "17": {"style": "Bell", "angle": 120.0, "pilot": 0.218750, "body": 0.6250, "bell": 0.6900, "pilot_length": 0.218750},
    "18": {"style": "Bell", "angle": 120.0, "pilot": 0.250000, "body": 0.7500, "bell": 0.7800, "pilot_length": 0.250000},
}


def center_drill_label(size_name: str) -> str:
    preset = CENTER_DRILL_PRESETS[size_name]
    return f"Size {size_name} | {preset['style']} | pilot {preset['pilot']:.4f} in"


def get_center_drill_options(include_custom: bool = False):
    options = list(CENTER_DRILL_PRESETS.keys())
    if include_custom:
        return ["Custom"] + options
    return options
