
LATHE_SPECS = {
    "417 Cincinnati Lathe": {
        "control": "Fanuc-style",
        "rpm_max": 1200,
        "notes": [
            "1200 RPM max in high, 300 RPM max in low",
            "Uses misc values to force high gear (M42)",
            "Thread format is longhand"
        ]
    },

    "421 Mazak QTS-300": {
        "control": "Mazatrol Smart",
        "rpm_max": 4000,
        "notes": [
            "Face driven",
            "Program should contain #101, #102, #103",
            "DO NOT DO ANY END WORK OR TAILSTOCK MOVES"
        ]
    },

    "423 Mazak QTS-300": {
        "control": "Mazatrol Smart",
        "rpm_max": 4000,
        "notes": [
            "3 jaw chuck machine",
            "Program should contain #101, #102, #103",
            "Steady-rest moves require G98 G4 X1.0"
        ]
    },

    "424 Mazak QTS-300": {
        "control": "Mazatrol Smart",
        "rpm_max": 4000,
        "notes": [
            "Collet chuck machine",
            "Program should contain #101, #102, #103",
            "Steady-rest moves require G98 G4 X1.0"
        ]
    },

    "426 Cincinnati Lathe": {
        "control": "Fanuc-style",
        "rpm_max": 1200,
        "notes": [
            "Shared note group with 417",
            "1200 RPM max in high, 300 RPM max in low"
        ]
    },

    "430 Mazak QTS-250": {
        "control": "Mazatrol",
        "rpm_max": 2000,
        "notes": [
            "No steady rest",
            "Max spindle speed with tailstock 2000",
            "Max spindle speed without tailstock 1000"
        ]
    },

    "431 Mazak QTS-250": {
        "control": "Mazatrol",
        "rpm_max": 2000,
        "notes": [
            "No steady rest",
            "Max spindle speed with tailstock 2000",
            "Max spindle speed without tailstock 1000"
        ]
    },

    "432 Mazak QTS-450 MY": {
        "control": "Mazatrol",
        "rpm_max": 1000,
        "notes": [
            "Machine will not read G91 on incremental moves",
            "Uses live tooling and keyway work",
            "Verify current steady-rest location values"
        ]
    },

    "433 Mazak QTS-350": {
        "control": "Mazatrol",
        "rpm_max": 3000,
        "notes": [
            "Uses teachable steady-rest positions",
            "Rest width 1.75",
            "Minimum to shoulder 1.50"
        ]
    },

    "434 Mazak QTS-350": {
        "control": "Mazatrol",
        "rpm_max": 3000,
        "notes": [
            "Uses teachable steady-rest positions",
            "Rest width 1.75",
            "Minimum to shoulder 1.50"
        ]
    },

    "436 Okuma LB4000": {
        "control": "OSP",
        "rpm_max": 6000,
        "notes": [
            "Steady rest is 2.5 wide",
            "G74 drill cycle must have D peck value",
            "Coolant should be on before spindle starts"
        ]
    }
}
