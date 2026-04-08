
MACHINES = {
    "417 Cincinnati Lathe": {
        "machine_type": "Lathe",
        "overview": [
            "Cincinnati lathe used for shaft work, face-driver work, grooves, and threads.",
            "Programmer has to pay attention to gear range, face-driver prep, and threading format.",
            "Use this page as a machine-rule page, not a generic machine description."
        ],
        "program_behavior": [
            "1200 RPM max in high gear, 300 RPM max in low gear.",
            "Uses misc values to force high gear (M42).",
            "Backwards rough and backwards finish tools are part of the normal tool layout on jobs that need them.",
            "Face-driver work needs a starter cut to seat the shaft into the drive blades."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "Thread pitch address is set to use F, not E.",
            "Post changed G32 to G33.",
            "Cantext functions include 5 = return tailstock and 6 = advance tailstock.",
            "Work offset logic is forced G54 for main spindle and G55 for sub spindle in the post."
        ],
        "code_rules": [
            "Thread code format @ longhand.",
            "Equal depths.",
            "Number of cuts @ 8-15.",
            "Number of spring cuts usually 1.",
            "Flank infeed angle @ 0."
        ],
        "shop_notes": [
            "Facing is done with finish tool and shortened end point to stop before center (approx. .5\" per side typically).",
            "Use misc values to force high gear (M42).",
            "For groove target: create \"I\" shaped line .500\" from defined shoulder closest to groove.",
            "Make line lengths .5\" each.",
            "For finish groove path: select groove tool, feed rate @ .25 and set to inches per minute, spindle @ 0, coolant off, turn lead-in and lead-out off.",
            "Go to geometry and change at point.",
            "Select horizontal line, add as a comment after \"/ M00\".",
            "Always do pulley end first."
        ],
        "workholding": [
            "Siemens shafts: offset pulley end face .030 in Mastercam before aligning model to Z to leave stock on face for cleaning up drive blade marks.",
            "Starter cut for face drivers: make sure to feed @ .010 for first .1 inch on roughing to seat shaft into drive blades.",
            "When roughing first side on face drivers, go past left end of part .100\"."
        ],
        "tooling": [
            "1. Rough",
            "2. Finish",
            "3. Backwards rough",
            "4. Backwards finish",
            "5. Groove",
            "6. Thread"
        ],
        "posting_cimco": [
            "Verify gear selection and RPM cap before release.",
            "Verify any tailstock code output when cantext is used.",
            "Backplot groove target path and any face-driver starter cut edits.",
            "Verify longhand threading output and cut count."
        ],
        "offset_logic": [
            "Main spindle / sub spindle work offset behavior follows the post setting.",
            "Verify actual setup before release."
        ],
        "mastercam_rules": [
            "Edit groove geometry exactly as noted for the I-shaped target line method.",
            "For rough OD toolpath on face-driver work, edit the path manually where needed to control feed and seating cut."
        ],
        "special_notes": [
            "The 1200/300 gear limitation is a hard planning item.",
            "This machine needs programmer attention, especially on face-driver jobs and thread output."
        ]
    },

    "421 Mazak QTS-300": {
        "machine_type": "Lathe",
        "overview": [
            "Primary production Mazak lathe.",
            "Face-driven machine with important restrictions versus the other QTS-300 machines.",
            "One of the main daily-use lathes."
        ],
        "program_behavior": [
            "Beginning of program should contain #101, #102, #103.",
            "Steady rest timing is critical when used.",
            "All steady rest moves should be followed by G98 G4 X1.0."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "General tailstock codes exist in the post, but machine-specific note for 421 is that this lathe is face driven.",
            "Thread pitch address is set to use F, not E.",
            "Use Mcam work offset logic in the post.",
            "Post has cantext functions for tailstock advance and return."
        ],
        "code_rules": [
            "DO NOT DO ANY END WORK OR TAILSTOCK MOVES.",
            "Avoid G28 W0 — use safe Z retract.",
            "Verify G50 spindle limit before release.",
            "Verify CSS behavior and threading cycles manually."
        ],
        "shop_notes": [
            "Feeds in IPR.",
            "Default roughing insert = DNMG.",
            "Default finishing insert = VNMG.",
            "PF for softer materials; MR / MF / MRR for harder materials; SM for some exotics.",
            "Use CSS for roughing when appropriate."
        ],
        "workholding": [
            "This lathe is face driven.",
            "Starter cut for face drivers: make sure to feed @ .010 for first .1 on roughing to seat shaft into drive blades.",
            "On rough OD toolpath: edit toolpath, select second point and change feed to .010, add point after second using created line from face of part, edit new point and change feed to .010, edit point after added point and change feed to .015.",
            "421 can go to end of part when roughing OD for second-side steady-rest preparation."
        ],
        "tooling": [
            "Tool list 421 (FACE DRIVEN)",
            "1. R.H. rough (rough passes should take .12-.20 a pass)",
            "2. open",
            "3. Finish",
            "4. open",
            "5. R.H thread",
            "6. open",
            "7. L.H. thread",
            "8. L.H. finish",
            "9. Groove (triangle)",
            "10. Open",
            "11. L.H. Groove",
            "12. Spare"
        ],
        "posting_cimco": [
            "Verify #101, #102, #103 at program start.",
            "Verify no end work or tailstock output.",
            "Verify any steady-rest code and dwell.",
            "Backplot full program before release."
        ],
        "offset_logic": [
            "Standard shop lathe offset structure.",
            "Verify offsets against setup sheet."
        ],
        "mastercam_rules": [
            "Verify stock and origin match the actual face-driven setup.",
            "Verify groove / thread / roughing edits are made before posting."
        ],
        "special_notes": [
            "This machine is not a normal QTS-300 clone from a programming standpoint.",
            "Treat the face-driven restriction as a hard rule."
        ]
    },

    "423 Mazak QTS-300": {
        "machine_type": "Lathe",
        "overview": [
            "Primary production Mazak QTS-300.",
            "Three-jaw chuck machine with steady-rest use and normal endwork capability.",
            "Very high-value daily programming machine."
        ],
        "program_behavior": [
            "Beginning of program should contain #101, #102, #103.",
            "Steady rest uses macros / misc values.",
            "All steady rest moves should be followed by G98 G4 X1.0."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "General tailstock codes exist in the post.",
            "Thread pitch address is set to use F, not E.",
            "Use Mcam work offset logic in the post."
        ],
        "code_rules": [
            "Steady Rest Codes (421, 423, 424):",
            "M05 (Make sure spindle is off)",
            "M9 (Make sure coolant is off)",
            "M98 P'A'00'B' (A= Current Position, B= Next Position)",
            "M87 (Close steady rest)",
            "G98 G4 X1.0 (X= Dwell For Rest To Close)",
            "M00 or M01 (Program stop to confirm rest)"
        ],
        "shop_notes": [
            "423 can go back 2\" from chuck when roughing OD for second-side steady-rest prep.",
            "Always try to use steady rest on second side of parts for TIR.",
            "Steady rest cannot get within 13.75\" of the tailstock, so move tailstock away from part before moving rest to end of part if rest band is within 3\" of end.",
            "Minimum distance from face of the chuck to tailstock with standard center is about 16\".",
            "With \"long\" tailstock ______."
        ],
        "workholding": [
            "Specific to 423 (3 jaw chuck).",
            "423 steady-rest table: Rest Width 1\", Min Width 1.5\", Min S.R. to Chuck 3.75\", Min S.R. to Tailstock 9\", Typ Band Length for Face 3\", Typ Band Distance to Collet 1.5\"."
        ],
        "tooling": [
            "Tool list 423, 424",
            "1. Rough (rough passes should take .12-.20 a pass)",
            "2. Center",
            "3. Finish",
            "4. Drill",
            "5. RH thread",
            "6. Drill for tap",
            "7. LH thread",
            "8. bore",
            "9. Groove (triangle)",
            "10. Tap",
            "11. Groove",
            "12. spare"
        ],
        "posting_cimco": [
            "Verify #101, #102, #103 at start.",
            "Verify steady-rest macro numbering and dwell.",
            "Verify tailstock timing on any rest move.",
            "Backplot full program before release."
        ],
        "offset_logic": [
            "Standard shop lathe offset structure.",
            "Verify offsets against setup."
        ],
        "mastercam_rules": [
            "Verify stock, origin, and operation order.",
            "Leave enough rollback on the OD for second-side rest placement."
        ],
        "special_notes": [
            "423 is one of the core shop machines and deserves full verification every post."
        ]
    },

    "424 Mazak QTS-300": {
        "machine_type": "Lathe",
        "overview": [
            "Primary production Mazak QTS-300.",
            "Collet-chuck machine with steady-rest use and different reach rules than 423.",
            "Daily-use lathe."
        ],
        "program_behavior": [
            "Beginning of program should contain #101, #102, #103.",
            "Steady rest uses macros / misc values.",
            "All steady rest moves should be followed by G98 G4 X1.0."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "General tailstock codes exist in the post.",
            "Thread pitch address is set to use F, not E.",
            "Use Mcam work offset logic in the post."
        ],
        "code_rules": [
            "Steady Rest Codes (421, 423, 424):",
            "M05 (Make sure spindle is off)",
            "M9 (Make sure coolant is off)",
            "M98 P'A'00'B' (A= Current Position, B= Next Position)",
            "M87 (Close steady rest)",
            "G98 G4 X1.0 (X= Dwell For Rest To Close)",
            "M00 or M01 (Program stop to confirm rest)"
        ],
        "shop_notes": [
            "424 can go back 2\" from collet when roughing OD for second-side steady-rest prep.",
            "Always try to use steady rest on second side of parts for TIR.",
            "Steady rest cannot get within 5\" of the tailstock, so move tailstock away from part before moving rest to end of part if rest band is within 3\" of end.",
            "Length from standard length tailstock to the face of the collet is 10\".",
            "With the \"long\" tailstock, ______.",
            "The stop inside the collet lets the part go into the collet from .500\" to around 2.500\".",
            "(10.5\" is probably a safe min. part length)"
        ],
        "workholding": [
            "Specific to 424 (collet chuck).",
            "424 steady-rest table: Rest Width 1\", Min Width 1.5\", Min S.R. to Collet 3.75\", Min S.R. to Tailstock 3\", Typ Band Length for Face 3\", Typ Band Distance to Collet 1.5\"."
        ],
        "tooling": [
            "Tool list 423, 424",
            "1. Rough (rough passes should take .12-.20 a pass)",
            "2. Center",
            "3. Finish",
            "4. Drill",
            "5. RH thread",
            "6. Drill for tap",
            "7. LH thread",
            "8. bore",
            "9. Groove (triangle)",
            "10. Tap",
            "11. Groove",
            "12. spare"
        ],
        "posting_cimco": [
            "Verify #101, #102, #103 at start.",
            "Verify steady-rest macro numbering and dwell.",
            "Verify collet / tailstock clearance assumptions.",
            "Backplot full program before release."
        ],
        "offset_logic": [
            "Standard shop lathe offset structure.",
            "Verify offsets against setup."
        ],
        "mastercam_rules": [
            "Verify stock, origin, and operation order.",
            "Leave enough rollback on the OD for second-side rest placement."
        ],
        "special_notes": [
            "424 reach and collet-stop realities matter when planning the setup."
        ]
    },

    "426 Cincinnati Lathe": {
        "machine_type": "Lathe",
        "overview": [
            "Uses the same programmer note set as 417 in the uploaded notes/post group.",
            "Treat as a Cincinnati lathe page sharing the same core restrictions until you split it further."
        ],
        "program_behavior": [
            "1200 RPM max in high gear, 300 RPM max in low gear.",
            "Uses misc values to force high gear (M42)."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "Thread pitch address is set to use F, not E.",
            "Post changed G32 to G33."
        ],
        "code_rules": [
            "Use the same thread / face-driver rules as 417 unless machine-specific differences are confirmed."
        ],
        "shop_notes": [
            "Review 417/426 shared note page for groove target, threading, and Siemens shaft prep."
        ],
        "workholding": [
            "Face-driver and shaft-prep logic may apply depending on setup."
        ],
        "tooling": [
            "Shared with 417 until separated."
        ],
        "posting_cimco": [
            "Verify machine-specific limits before release."
        ],
        "offset_logic": [
            "Verify actual setup offsets."
        ],
        "mastercam_rules": [
            "Use the 417 logic as the baseline."
        ],
        "special_notes": [
            "Split this into its own page later if new notes are captured."
        ]
    },

    "430 Mazak QTS-250": {
        "machine_type": "Lathe",
        "overview": [
            "Mazak QTS-250 family machine.",
            "These machines do not have a steady rest."
        ],
        "program_behavior": [
            "Max spindle speed [G50] W/ Tailstock: 2000.",
            "Max spindle speed [G50] W/O Tailstock: 1000."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "General tailstock codes exist in the post.",
            "Thread pitch address is set to use F, not E."
        ],
        "code_rules": [
            "Reference for program math from Flowserve program 10822001.",
            "102 is part OAL.",
            "103 is baseline print part length – part you are making."
        ],
        "shop_notes": [
            "These machines do not have a steady rest."
        ],
        "workholding": [
            "Verify tailstock use before final spindle limit selection."
        ],
        "tooling": [
            "1. OD",
            "2. Rough Face & OD (WNMG 80 Deg Inserts) 432",
            "3. Finish Face & OD (WNMG 80 Deg Inserts) 331",
            "4. ID",
            "5. OD Groove",
            "6. ID Rough Bore",
            "7. OD",
            "8. ID Finish Bore or Drill (Watch for Clearance)",
            "9. OD",
            "10. ID or Drill (Watch for Clearance)",
            "11. OD",
            "12. ID Finish Bore or Tap"
        ],
        "posting_cimco": [
            "Verify G50 spindle limit based on tailstock condition.",
            "Verify any math driven by #102 / #103 variables."
        ],
        "offset_logic": [
            "Verify actual setup offsets."
        ],
        "mastercam_rules": [
            "Watch clearance on ID finish bore / drill tools."
        ],
        "special_notes": [
            "No steady-rest support on this machine."
        ]
    },

    "431 Mazak QTS-250": {
        "machine_type": "Lathe",
        "overview": [
            "Mazak QTS-250 family machine.",
            "These machines do not have a steady rest."
        ],
        "program_behavior": [
            "Max spindle speed [G50] W/ Tailstock: 2000.",
            "Max spindle speed [G50] W/O Tailstock: 1000."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "General tailstock codes exist in the post.",
            "Thread pitch address is set to use F, not E."
        ],
        "code_rules": [
            "Reference for program math from Flowserve program 10822001.",
            "102 is part OAL.",
            "103 is baseline print part length – part you are making."
        ],
        "shop_notes": [
            "These machines do not have a steady rest."
        ],
        "workholding": [
            "Verify tailstock use before final spindle limit selection."
        ],
        "tooling": [
            "1. OD",
            "2. Rough Face & OD (WNMG 80 Deg Inserts) 432",
            "3. Finish Face & OD (WNMG 80 Deg Inserts) 331",
            "4. ID",
            "5. OD Groove",
            "6. ID Rough Bore",
            "7. OD",
            "8. ID Finish Bore or Drill (Watch for Clearance)",
            "9. OD",
            "10. ID or Drill (Watch for Clearance)",
            "11. OD",
            "12. ID Finish Bore or Tap"
        ],
        "posting_cimco": [
            "Verify G50 spindle limit based on tailstock condition.",
            "Verify any math driven by #102 / #103 variables."
        ],
        "offset_logic": [
            "Verify actual setup offsets."
        ],
        "mastercam_rules": [
            "Watch clearance on ID finish bore / drill tools."
        ],
        "special_notes": [
            "No steady-rest support on this machine."
        ]
    },

    "432 Mazak QTS-450 MY": {
        "machine_type": "Lathe",
        "overview": [
            "Mazak QTS-450 MY with turning and live-tool work.",
            "Used for turning, threading, grooves, face drill/tap, and keyway / woodruff support.",
            "One of the most important multi-use lathes to capture in the app."
        ],
        "program_behavior": [
            "Max diameter for steady rest to clamp on is 7.5\".",
            "Steady rest can be set flush against tailstock.",
            "Steady rest center locates 39.5\" from chuck end on op1.",
            "Rest location 37.5\" from chuck end on op2 on one note page, and 35.5\" from chuck end on op2 on a later updated steady-rest page (changed from 37.5 R.W. 1/22/2026).",
            "Cut rest band 2\"-5\" from the tail stock end."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "General tailstock codes exist in the post.",
            "Thread pitch address is set to use F, not E.",
            "Machine will not read G91 on incremental moves.",
            "Use address substitutions for incremental data: X-axis = Address U, Z-axis = Address W, C-axis = Address H, Y-axis = Address V."
        ],
        "code_rules": [
            "LOCAL SUB PROGRAM FORMAT",
            "Prep code as need",
            "M98 Q0001 (M98=JUMP TO SUB PROGRAM, Q=LINE NUMBER TO JUMP TO, L is number of times to repeat )",
            "(Code as needed for part)",
            "(\"H\" can be used for incremental c axis rotation if needed)",
            "M30 (end of program)",
            "At the end of the program",
            "N0001 ( line number to jump to )",
            "(Code as needed to cut part )",
            "M99 (jump back to M97, P can be used if need to jump back to different sequence )",
            "% (end of program, only put at end of last sub program)",
            "SUB PROGRAM FORMAT (NOT LOCAL)",
            "M98 P15 Q1 ( P is program number, Q is the sequence number to jump to, L is number of time to repeat )",
            "M99 (P can be used if need to jump back to different sequence number )",
            "%"
        ],
        "shop_notes": [
            "Tool list:",
            "1. OD thread RH",
            "2. Rough (rough passes should take .15 - .25 a pass)",
            "3. Finish",
            "4. Backward rough",
            "5. Backward finish",
            "6. Center",
            "7. Drill",
            "8. Boring bar, TCMT 2 1.5 1-UF",
            "9. Live tooling, USE for face drills and face tap",
            "10. END MILL",
            "11. END MILL",
            "12. OD groove / RH thread",
            "Max diameter to put through spindle: 4.5\"",
            "Max grip length of chuck jaws: 3.55\"",
            "End mills he has collets for as of 1/9/2024: 3/16, 6mm, 1/4, 3/8, 1/2 (does he have a 5/16 holder?)",
            "For milling keyway use tool number 10.6 or 11.6.",
            "TAP or FACE DRILL HOLES USE T9.11",
            "DO OFF CENTER END WORK FIRST (BEFORE MILLING KEYWAYS).",
            "NOTE: If doing woodruff keys, do them below the part or the x will over travel when the y moves."
        ],
        "workholding": [
            "When roughing OD on first side, rough to biggest diameter and stop 2\" from end of part when gripper jaws. 4\" from chuck for hard jaws (very long part).",
            "Specific to second operation on large diameter parts, if the section that was chucked on the first operation is larger than 10-10.5 inches it could strike the right side of the steady rest on the second operation.",
            "To get around this the operator will manually center the second end, start by turning the chucked section down to near the steady rest diameter then face and recenter.",
            "Note: C angle must have a decimal point."
        ],
        "tooling": [
            "See tool list in shop notes."
        ],
        "posting_cimco": [
            "Verify any subprogram format carefully.",
            "Verify no G91 assumptions exist in code.",
            "Verify steady-rest locations against current setup sheet.",
            "Verify live-tool and off-center work sequence before release."
        ],
        "offset_logic": [
            "Verify setup zero and any rest location from the zero point."
        ],
        "mastercam_rules": [
            "If using local subprogram logic, keep jump sequence clean and intentional.",
            "For incremental output, remember the machine does not read G91 and uses address substitutions instead."
        ],
        "special_notes": [
            "There is a note conflict on op2 rest location (37.5 vs 35.5). Use the latest shop-confirmed number tomorrow before relying on the app.",
            "This page is intentionally detailed because this machine does a lot."
        ]
    },

    "433 Mazak QTS-350": {
        "machine_type": "Lathe",
        "overview": [
            "Mazak QTS-350 family machine with steady-rest support.",
            "Used for standard shaft processing with rough, finish, drilling, threads, grooves, and tap work."
        ],
        "program_behavior": [
            "These machines have 4 teachable locations for rest moves and multiple sub programs to move them from each position.",
            "Rest move sub program numbers should start with current rest location, then 2 zeros, then next rest location followed by 4 zeros.",
            "Example: 2003000. This will move the steady rest from position 2 to position 3."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "General tailstock codes exist in the post.",
            "Thread pitch address is set to use F, not E."
        ],
        "code_rules": [
            "Steady Rest Misc Values",
            "Macro # definitions",
            "1 = inserts comments to tell operator to manually move rest.",
            "2 = inserts code to open steady rest",
            "3 = inserts code to close steady rest",
            "Otherwise enter macro to move rest (example: 10020000)",
            "Close rest after move",
            "0 = will not input M87 after moving steady rest",
            "1 = Will input M87 after moving steady rest",
            "All steady rests moves should always be followed by: G98 G4 X1.0"
        ],
        "shop_notes": [
            "Tool list:",
            "1. Rough (rough passes should take about .20 a pass)",
            "2. Center",
            "3. Finish",
            "4. Bore (Use CDHH120605 HP520B for center chamfers)",
            "5. RH thread",
            "6. Drill for tap",
            "7. LH thread",
            "8. Finish bore",
            "9. Groove (triangle)",
            "10. Tap",
            "11. Groove",
            "12. spare",
            "Standard process:",
            "Cut rest band (3\" long, start 5.5 from end of part)",
            "Close steady rest",
            "Stop spindle, stop coolant",
            "Retract tailstock",
            "Do all end work",
            "Advance tailstock",
            "Rough OD back from biggest diameter to 5\" from end of part in chuck/collet",
            "This will be used for rest band on second side",
            "Rough and finish OD",
            "Cut any grooves",
            "Do all threads"
        ],
        "workholding": [
            "When roughing make sure to go back far enough on biggest diameter so they have somewhere to put steady rest on second side.",
            "Chuck (433): can rough OD back 2\"-3\" from end of part if using jaw stop.",
            "Collet (434): can rough OD back 3\"-6\" from end of part depending on stop used.",
            "Always try to use steady rest on second side of parts for TIR.",
            "Rest width: 1.75\". Minimum to shoulder: 1.50\"."
        ],
        "tooling": [
            "See tool list in shop notes."
        ],
        "posting_cimco": [
            "Verify steady-rest subprogram numbering.",
            "Verify G98 G4 X1.0 appears after rest moves.",
            "Verify tailstock / spindle / coolant order around rest handling."
        ],
        "offset_logic": [
            "Verify actual setup and rest location origin."
        ],
        "mastercam_rules": [
            "Build enough rollback on the largest OD for second-side rest use."
        ],
        "special_notes": [
            "This family has a more formal rest-motion structure than some other lathes."
        ]
    },

    "434 Mazak QTS-350": {
        "machine_type": "Lathe",
        "overview": [
            "Mazak QTS-350 family machine with steady-rest support.",
            "Collet variant / collet-use notes differ from 433."
        ],
        "program_behavior": [
            "These machines have 4 teachable locations for rest moves and multiple sub programs to move them from each position.",
            "Rest move sub program numbers should start with current rest location, then 2 zeros, then next rest location followed by 4 zeros."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "General tailstock codes exist in the post.",
            "Thread pitch address is set to use F, not E."
        ],
        "code_rules": [
            "Use the same rest misc-value structure as 433.",
            "All steady rest moves should always be followed by G98 G4 X1.0."
        ],
        "shop_notes": [
            "Use the 433/434 processing standard unless setup requires otherwise."
        ],
        "workholding": [
            "Collet (434): can rough OD back 3\"-6\" from end of part depending on stop used.",
            "Rest width: 1.75\". Minimum to shoulder: 1.50\"."
        ],
        "tooling": [
            "Shared 433/434 tool list."
        ],
        "posting_cimco": [
            "Verify rest motion, tailstock timing, and end-work order."
        ],
        "offset_logic": [
            "Verify actual setup and rest location origin."
        ],
        "mastercam_rules": [
            "Leave enough rollback for second-side rest use."
        ],
        "special_notes": [
            "Split this page further later if 434-specific notes keep growing."
        ]
    },

    "436 Okuma LB4000": {
        "machine_type": "Lathe",
        "overview": [
            "Okuma LB4000 EX with Y-axis, live angle holder, tailstock, and steady-rest support.",
            "Used for turning plus live-tool work including woodruff and end mill operations."
        ],
        "program_behavior": [
            "Steady rest is 2.5\" wide on this machine.",
            "Steady rest zero location is face of shaft.",
            "Watch for rest clearance with turret when open.",
            "Watch for rest clearance with tailstock.",
            "Max sub spindle speed 6000 RPM."
        ],
        "post_limits": [
            "Post includes machining mode designation functions G270/G271/G272.",
            "Post has coolant behavior notes: coolant is always needed before the spindle starts otherwise it heats up quickly and may burn off.",
            "Post has gear selection configured for lathe only.",
            "Post coolant format is separate lines."
        ],
        "code_rules": [
            "Programs must start with a letter A. ( I guess this was changed to T at some point, remember to ask steve about this R.W. 4/8/25)",
            "Program might have to start with",
            "G13",
            "G270",
            "CLEAR",
            "DRAW",
            "NOTE: return y to 0 before end of operation. R.W. 1/12/2026",
            "NOTE: WHEN MILLING THE X ARE IN RADIUS R.W. 4/8/2025"
        ],
        "shop_notes": [
            "1. Rough  DNMG 442-PR",
            "2. Finish  DNMG 432FW",
            "3. REVERSED  DNMG-442-PR",
            "4. Spot Drill",
            "5. REVERSED  DNMG432FW",
            "6. Boring Bar",
            "7. Empty",
            "8. Live – WOODRUFF CUTTER",
            "9. Groove",
            "10. LIVE- 9/32 END MILL",
            "11. tool",
            "12. Live – 3/8 END MILL",
            "NOTE: if doing woodruff keys, do them below the part or the x will over travel when the y moves. (Y- number)",
            "Program can not start with a G13 (upper turret) Delete from program. Robert w. 3/20/2026",
            "Program have to start with",
            "G270",
            "CLEAR",
            "DRAW",
            "A G74 drill cycle must have a D value, (peck amount) Robert w. 3/20/2026"
        ],
        "workholding": [
            "Watch rest clearance with turret and tailstock before release."
        ],
        "tooling": [
            "See shop notes for current loaded pattern."
        ],
        "posting_cimco": [
            "Verify start format tomorrow before trusting old notes because one note conflicts on G13/A/T start behavior.",
            "Verify G74 peck cycles include D value.",
            "Verify coolant starts before spindle."
        ],
        "offset_logic": [
            "Steady-rest zero location is face of shaft."
        ],
        "mastercam_rules": [
            "When milling, X values are in radius.",
            "Return Y to 0 before end of operation."
        ],
        "special_notes": [
            "There is a conflict between older and newer start-code notes. Treat the latest confirmed shop practice as the source of truth tomorrow."
        ]
    },

    "652 Makino A51": {
        "machine_type": "Mill",
        "overview": [
            "Makino A51 4X HMC with strict machine-specific rules.",
            "This machine is rule-heavy and should always override generic mill habits."
        ],
        "program_behavior": [
            "Programs format O####.NC.",
            "Subprogram type in the post is external sub programs (M98).",
            "Subprogram numbering starts at 1000.",
            "TWP (G68.2) is off in the post."
        ],
        "post_limits": [
            "THE G95 FEED PER REV CODE CAUSES THE MILL TO ALARM OUT.",
            "WHEN USING TOOL OFFSETS (G41/G42), PROGRAM SHOULD BE TO THE CENTER LINE OF THE TOOL (WEAR IN MASTERCAM).",
            "THE OFFSETS THE M11 (UNLOCK), B0, M10 (LOCK), B NEEDS TO BE ZERO.",
            "FOR OFFSETS THE H# IS THE TOOL NUMBER, FOR D# ITS THE TOOL NUMBER+100",
            "M26 CODE IS FOR THROUGH SPINDLE COOLANT"
        ],
        "code_rules": [
            "WHEN TAPING CAN BE IN FEED PER REV OR FEED PER MIN, JUST MUST HAVE THE CORRECT G CODE FOR FEED.SEE HIDE CODE, ROBERT",
            "M60 AT START AND ENDING",
            "The program should not have an B moves."
        ],
        "shop_notes": [
            "As of 2/6/2025:",
            "When running from the vice, the left end (left side of vice) is normally the part origin. This is because the left end has a stop he can push the part against.",
            "The face on the left side is normally G54, the body diameter is G55, the face on the right end is G56.",
            "In the machine only, the left (G54) is B90, the body keyway (G55) is B180, the right end (G56) is B270."
        ],
        "workholding": [
            "Verify fixture orientation carefully.",
            "From the perspective of the \"top\" view and with the \"top\" plane set as the WCS, the part should be as shown in the note images.",
            "The left end of the part is on the right side, the body keyway is on the \"up\" side of the screen."
        ],
        "tooling": [
            "H = tool number",
            "D = tool number + 100"
        ],
        "posting_cimco": [
            "Verify no G95 appears.",
            "Verify no B moves appear.",
            "Verify H and D output.",
            "Verify M26 and M60 placement.",
            "Verify subprogram calls if used."
        ],
        "offset_logic": [
            "G54 = left end face",
            "G55 = body diameter / body keyway",
            "G56 = right end face",
            "In machine terms the corresponding B positions are B90 / B180 / B270."
        ],
        "mastercam_rules": [
            "A plane is made on each of the faces that you are milling on, the planes need to have their \"z\" in line with the spindle/tool.",
            "When viewed from the perspective of the spindle/tool the +y is up and +x is to the right.",
            "The \"left end\" plane has the offset changed to 0, the body plane has the offset changed to 1, the right end plane has the offset set as 2."
        ],
        "special_notes": [
            "This machine should always be checked manually in CIMCO before release."
        ]
    },

    "654 Okuma Genos M560-V": {
        "machine_type": "Mill",
        "overview": [
            "Okuma Genos M560-V mill with rotary chuck and V-block use.",
            "Important machine for keyways, flats, hexes, and rotated work."
        ],
        "program_behavior": [
            "PROGRAMS FORMAT EM####.MIN",
            "X0 RIGHT END FOR VBLOCKS, ON THE LEFT FOR THE ROTORY CHUCK",
            "Y0 CENTER LINE OF SHAFT",
            "Z0 TOP OF DIAMETER. (AS OF 10/14/2024 THIS IS FOR THE ROTORY FIXTURE ALSO R.W. )",
            "2/12/2025 MAX SPINDLE SPEED 12000 RPM NOT THE 15000 WE HAD. R.W."
        ],
        "post_limits": [
            "Post supports subprograms.",
            "6/27/2025 ROBERT W.- EDIT TO POST OUT \"G10\" AFTER \"G11\" COORDINATE SYSTEM SHIFT.",
            "Subprogram type in post is external sub programs (M98).",
            "Tool offset override is matched in the post."
        ],
        "code_rules": [
            "ROTORY AXIS IS \"A\"",
            "THE M53 OR M54 MIGHT HAVE TO BE AT THE END OF THE CYCLE",
            "CHECK THAT TAP HAS THE SPINDLE TURNED ON ! 6/30/2025"
        ],
        "shop_notes": [
            "ROTORY CHUCK:",
            "MAX DIA TO FIT THROUGH THE ROTORY CHUCK IS ABOUT 2.750. MAX LENGTH THAT CAN GO THROUGH THE CHUCK IS 17\".",
            "29\" IS THE MAX LENGTH FROM THE FACE OF THE CHUCK.",
            "26\" IS THE MAX LENGTH FROM THE FACE OF THE JAWS",
            "V BLOCKS:",
            "28\" IS THE MAX LENGTH OF PART IF THERE ARE KEYWAYS ON BOTH ENDS OF A PART.",
            "THE PART CAN OVER HANG THE TABLE 10\" ON THE LEFT SIDE (NOT CUTTING KEYWAYS ON THAT END)",
            "THE PART CAN OVER HANG 8.5\" ON THE RIGHT SIDE (WITH OUT HITTING THE CHUCK)"
        ],
        "workholding": [
            "PART SIZE FOR DOUBLE V-BLOCK:",
            "The max diameter that can rest in the double V-block is 2.5\".",
            "When resting on a 2.5\" diameter the max the largest diameter can be is 5.3\". Any larger and the part will hit the table.",
            "With the rest diameter size of 1/2\" the largest diameter that will fit with out hitting the table is reduced to 2.5\"."
        ],
        "tooling": [
            "Verify actual machine loadout before release."
        ],
        "posting_cimco": [
            "Verify any rotated work code.",
            "Verify G10 after G11 output if using coordinate system shift.",
            "Verify tap cycles have spindle on."
        ],
        "offset_logic": [
            "X/Y/Z zero logic depends on V-block vs rotary chuck, and must be checked before posting."
        ],
        "mastercam_rules": [
            "OKUMA SUB PROGRAM EXAMPLES",
            "N5",
            "(NORMAL PREP CODE TO CALL TOOL AND TURN ON SPINDLE )",
            "A0 (ANGLE TO MILL FIRST FLAT)",
            "CALL O1001 (MUST BE O THEN 4 LETTERS OR NUMBERS )",
            "A180. (ANGLE FOR NEXT FLAT )",
            "CALL O1001 (CALL SUB PROGRAM)",
            "(NORMAL CODE TO STOP TOOL)",
            "(REST OF PROGRAM AS NEEDED)",
            "M30 (MUST HAVE M30 HERE)",
            "O1001 (SUB PROGRAM FOR FLAT OR HEX )",
            "(CODE AS NEEDED)",
            "RTS (RETURN TO SENDER)",
            "654 OKUMA G11 WORK COORDINATE ROTATE EXAMPLE",
            "CALL O1000 (RUN SUB PROGRAM 1000 IN FIRST LOCATION)",
            "G00 G90 G11 X0. Y0. P45. ( G90 FOR ABSOLUTE JUST IN CASE, G11 ROTATE CODE, X&Y LOCATION TO ROTATE AROUND, IN THIS CASE THE CENTER OF THE PART, ANGLE TO ROTATE )",
            "(RUN SUB PROGRAM AGAIN AS NEEDED)",
            "G10 ( CANCEL G11, MUST BE ON A LINE WITH NO OTHER G CODES )"
        ],
        "special_notes": [
            "This machine page should help prevent bad assumptions on part length and V-block size."
        ]
    },

    "655 Haas VF6": {
        "machine_type": "Mill",
        "overview": [
            "Haas VF6 used for shaft work, rotary fixture work, woodruffs, keyways, and rotated milling."
        ],
        "program_behavior": [
            "PROGRAMS FORMAT EM####.NC",
            "X zero right end face of shaft, unless using rotary fixture",
            "Y zero center line of shaft",
            "Z zero is center of the shaft"
        ],
        "post_limits": [
            "Post supports local subprograms (M97).",
            "Subprogram numbering starts at 1001.",
            "Tool offset override is matched in the post."
        ],
        "code_rules": [
            "Rotary fixture on right side of table so cords do not hit tools/tool changer, programs seem to be programed from the left end in the x+ direction.",
            "The Rotary fixture has a through hole that the shaft can fit through as long as it is less then 3.5 or 4\" in diameter.",
            "Max length from face of jaw to tailstock is 30\".",
            "Must remove G90 G53 X-30. Y0. from end of the program (the rotary fixture hits the door).",
            "Note off set #1 is on the left and counts up as you go right."
        ],
        "shop_notes": [
            "GENERAL NOTES:",
            "add a 2 sec dwell on woodruff . (G04 P2.0)",
            "DRILL G83 CAN NOT HAVE A DRILL Q OF 0",
            "FOR DRILLS, G98 canned cycle initial point return, g99 canned cycle R plane return, ( don’t crash)",
            "When Turing part to add",
            "G91 G28 Z0",
            "G90 G53 X-30. Y0.",
            "M00 (TURN PART  DEG)"
        ],
        "workholding": [
            "To use double v block the diameter that rest in the v must be smaller than about 2.4\". the largest diameter that is not in the v block must be smaller than 5.250",
            "Double v block v's are approximately 6\" apart",
            "For the single v block the diameter that rest in the v must be smaller than 8.250."
        ],
        "tooling": [
            "Verify actual machine loadout before release."
        ],
        "posting_cimco": [
            "Verify end-of-program home move does not hit the door with the rotary fixture.",
            "Verify G83 Q values.",
            "Verify woodruff dwell."
        ],
        "offset_logic": [
            "Offset #1 is on the left and counts up as you go right."
        ],
        "mastercam_rules": [
            "655 HAAS SUB PROGRAM EXAMPLE PROGRAM EM10544.OP2)",
            "NORMAL START OF PAROGRAM",
            "M97 P1(P IS THE N NUMBER TO JUMP TO )",
            "REST OF G CODE",
            "M30 (END OF PROGRAM SO THAT SUBPROGRAM CODE CAN NOT BE RAN OUT OF ORDER)",
            "(SUB PROGRAM /////////////////////////////////)",
            "N1 (CODE AS NEEDED )",
            "M99 (THE M99 RETURNS TO M97 LINE)",
            "% (THIS % NEEDS TO BE HERE SO THE MILL READS THE PROGRAM )",
            "655 Haas G68 WORK COORDINATE ROTATE EXAMPLE (PROGRAM EM5928.NC  JOB D19514DET-2 )",
            "M97 P1001 (RUN SUB PROGRAM 1001 IN FIRST LOCATION)",
            "G00 G90 G98 X0. Y0. R45. (G90 FOR ABSOLUTE JUST IN CASE, G98 ROTATE CODE, X&Y LOCATION TO ROTATE AROUND, IN THIS CASE THE CENTER OF THE PART, ANGLE TO ROTATE )",
            "G69 G90 X0 Y0 (CANCEL G68, IM NOT SURE WHY YOU HAVE TO PUT THE LOCATION IN FOR THIS CODE BUT THAT IS HOW IT IS SHOWN IN THE HAAS BOOK )"
        ],
        "special_notes": [
            "Keep an eye on rotary-fixture clearance and end-home moves."
        ]
    },

    "656 Haas VF3": {
        "machine_type": "Mill",
        "overview": [
            "Haas VF-3/20 mill using similar tool numbering logic to 655 but only 20 pockets."
        ],
        "program_behavior": [
            "Use the same tool numbers 655 mill, it has 100+ tool numbers but only 20 tool pockets",
            "PROGRAMS FORMAT O######.NC , it looks like the program number must start with O then can be letters or numbers up to 5 more digits long.",
            "Must have Oxxxx program number at the top of the program",
            "only one mxx code on a line, robert w. 12/15/2025 M8 AND m3"
        ],
        "post_limits": [
            "Post supports local subprograms (M97).",
            "Subprogram numbering starts at 1001.",
            "Tool offset override is matched in the post."
        ],
        "code_rules": [
            "X zero right end face of shaft",
            "Y zero center line of shaft",
            "Z zero is center of the shaft",
            "Start off sets offset at G110 and counts up as you go from right front to left back.",
            "The coolant pump is slow to turn on, move m8 up in program, consider deleting all m9, they are not needed the M01 and M30 both turn off the coolant.",
            "Change the home position at the end of program to x-.020",
            "when Turing part to add",
            "G91 G28 Z0",
            "G90 G53 X-20. Y0.",
            "M00 (TURN PART  DEG)"
        ],
        "shop_notes": [
            "The first note in the program is displayed in the program directory.",
            "Rotary fixture on right side of table So cords do not hit tools/tool changer, programs seem to be programed from the left end in the x+ direction.",
            "Max length from face of chuck to tailstock is 22\".",
            "Note G110 is on the left and counts up as you go right"
        ],
        "workholding": [
            "Verify rotary-fixture clearance and tailstock length."
        ],
        "tooling": [
            "Use 655 numbering logic but manage the 20-pocket limit."
        ],
        "posting_cimco": [
            "Verify single M-code-per-line output around spindle/coolant.",
            "Verify end-home move X-.020 / G53 X-20 logic.",
            "Verify slow coolant pump workaround."
        ],
        "offset_logic": [
            "G110 starts on the left and counts as you go right / through the setup."
        ],
        "mastercam_rules": [
            "Verify offset numbering matches machine pocket / setup plan."
        ],
        "special_notes": [
            "This mill can trip you up faster than 655 because of pocket count and M-code formatting."
        ]
    },

    "657 Haas VF5": {
        "machine_type": "Mill",
        "overview": [
            "Haas VF5 with A axis. Note says machine has a 10000 RPM spindle."
        ],
        "program_behavior": [
            "10000rpm spindle",
            "PROGRAMS FORMAT O######.NC , it looks like the program number must start with O"
        ],
        "post_limits": [
            "No post file uploaded for 657 in this batch, so this page is based on the machine note image only."
        ],
        "code_rules": [
            "Change the home position at the end of program to x-.020",
            "when Turing part to add",
            "G91 G28 Z0",
            "G90 G53 X-30. Y0.",
            "M00 (TURN PART  DEG)"
        ],
        "shop_notes": [
            "It has an a axis, I believe this is the direction the A turns the part when positive."
        ],
        "workholding": [
            "Verify actual rotary / A-axis orientation before release."
        ],
        "tooling": [
            "Verify actual loadout."
        ],
        "posting_cimco": [
            "Verify A-axis sign and home move."
        ],
        "offset_logic": [
            "Verify actual setup offsets."
        ],
        "mastercam_rules": [
            "Use the note image as a reminder on A-axis positive direction until a real post/rule page is built."
        ],
        "special_notes": [
            "This page is intentionally lighter because only the note image was supplied."
        ]
    },

    "Cincinnati Arrow Mill": {
        "machine_type": "Mill",
        "overview": [
            "Cincinnati Millicron 3X VMC / Cincinnati Arrow style machine entry.",
            "Only post file was supplied in this batch, not a dedicated note page."
        ],
        "program_behavior": [
            "Post supports subprograms."
        ],
        "post_limits": [
            "Subprogram type in post is external subprograms (M98).",
            "Tool offset override is not matched in the post.",
            "Subprogram numbering starts at 1000."
        ],
        "code_rules": [
            "Verify actual shop rules before first use because this page is post-driven right now."
        ],
        "shop_notes": [
            "Add machine-specific shop notes as they are captured."
        ],
        "workholding": [
            "Verify actual setup."
        ],
        "tooling": [
            "Verify actual machine loadout."
        ],
        "posting_cimco": [
            "Backplot and inspect output carefully until notes are added."
        ],
        "offset_logic": [
            "Verify actual offset behavior."
        ],
        "mastercam_rules": [
            "Verify origin and post selection before release."
        ],
        "special_notes": [
            "This page still needs real shop notes."
        ]
    },

    "411 Manual Lathe": {
        "machine_type": "Manual Lathe",
        "overview": [
            "Manual machine reference page."
        ],
        "program_behavior": ["Not applicable."],
        "post_limits": ["Not applicable."],
        "code_rules": ["Not applicable."],
        "shop_notes": ["Use for manual-machine reference only."],
        "workholding": ["Verify setup manually."],
        "tooling": ["Manual tooling reference placeholder."],
        "posting_cimco": ["Not applicable."],
        "offset_logic": ["Not applicable."],
        "mastercam_rules": ["Not applicable."],
        "special_notes": ["Add manual-machine-specific notes later."]
    },

    "413 Manual Lathe": {
        "machine_type": "Manual Lathe",
        "overview": [
            "Manual machine reference page."
        ],
        "program_behavior": ["Not applicable."],
        "post_limits": ["Not applicable."],
        "code_rules": ["Not applicable."],
        "shop_notes": ["Use for manual-machine reference only."],
        "workholding": ["Verify setup manually."],
        "tooling": ["Manual tooling reference placeholder."],
        "posting_cimco": ["Not applicable."],
        "offset_logic": ["Not applicable."],
        "mastercam_rules": ["Not applicable."],
        "special_notes": ["Add manual-machine-specific notes later."]
    }
}
