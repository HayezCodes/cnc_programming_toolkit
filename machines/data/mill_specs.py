
MILL_SPECS = {
    "652 Makino A51": {
        "control": "Makino Pro6",
        "rpm_max": None,
        "notes": [
            "No G95",
            "No B moves",
            "H offset = tool number, D offset = tool number + 100"
        ]
    },

    "654 Okuma Genos M560-V": {
        "control": "OSP",
        "rpm_max": 12000,
        "notes": [
            "Programs format EM####.MIN",
            "Rotary axis is A",
            "Post edited to output G10 after G11 coordinate shift"
        ]
    },

    "655 Haas VF6": {
        "control": "Haas NGC",
        "rpm_max": None,
        "notes": [
            "Programs format EM####.NC",
            "Local subprograms use M97",
            "Remove G90 G53 X-30. Y0. when rotary fixture hits the door"
        ]
    },

    "656 Haas VF3": {
        "control": "Haas NGC",
        "rpm_max": None,
        "notes": [
            "Programs format O######.NC",
            "Only one M code on a line",
            "Move M8 earlier because coolant pump is slow"
        ]
    },

    "657 Haas VF5": {
        "control": "Haas NGC",
        "rpm_max": 10000,
        "notes": [
            "Has A axis",
            "Programs format O######.NC"
        ]
    },

    "Cincinnati Arrow Mill": {
        "control": "Fanuc-style",
        "rpm_max": None,
        "notes": [
            "Post supports external subprograms (M98)",
            "Still needs shop notes"
        ]
    }
}
