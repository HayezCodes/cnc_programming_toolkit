# CNC Programming Toolkit - Agent System + Rules

# =========================
# AGENT ROLES
# =========================

## Architecture Agent
Responsible for file structure, modular design, and safe integration of new features.

## Calculator Agent
Handles all calculator logic including:
- Triangle
- Keyway
- Chamfer
- Drill Breakthrough
- Center Drill Depth
- Spot Drill Depth

## Threads Agent
Manages:
- Thread data
- Tap drill logic
- OD/ID modeling diameters
- TPI and metric pitch handling

## UI + Machines Agent
Controls:
- Streamlit layout
- Sidebar/navigation
- Machines tab and machine-specific notes

# =========================
# CORE RULES (CRITICAL)
# =========================

- Do not modify unrelated files.
- Reuse existing helpers, functions, and patterns before creating new logic.
- Preserve current layout, spacing, and mobile readability unless explicitly asked to redesign.
- Avoid unnecessary dependencies.
- Before finishing, verify no regressions were introduced outside the requested scope.
- Never break working features
- Always return full copy-paste-ready files
- Maintain shop-friendly logic
- Do not modify unrelated files
- Preserve layout and UI consistency
- Reuse existing helpers before creating new logic
- Do not add clutter or unnecessary sections

# =========================
# WORKING STYLE
# =========================

- Prefer targeted edits over full rewrites
- Inspect relevant files before editing
- Keep code clean, readable, and practical
- Follow existing app structure and patterns
- Avoid introducing unnecessary dependencies

# =========================
# TOOLKIT PRIORITIES
# =========================

This app is focused on real CNC programming support:
- speeds and feeds
- machining calculators
- threads and modeling support
- checklist workflow
- standards and machine notes
- tool chooser system

# =========================
# USER SHOP PREFERENCES
# =========================

- Lathe feeds use IPR
- Mill feeds use IPM
- Roughing inserts: DNMG
- Finishing inserts: VNMG

Material behavior:
- Softer materials → PF inserts
- Harder materials → MR / MF / MRR
- Exotics → SM inserts (when needed)

Mill tooling scope:
- spot drills
- taps
- endmills

UI:
- clean, uncluttered
- no unnecessary sections or blank space
- maintain consistent layout across pages

# =========================
# FILE EDITING RULES
# =========================

- Only edit files related to the task
- Do not break page-to-page consistency
- Do not duplicate logic if helpers already exist
- Keep naming consistent with existing patterns

# =========================
# RESPONSE FORMAT
# =========================

When completing a task:

1. List files changed
2. Explain what changed
3. State assumptions (if any)
4. Provide full updated files (if applicable)
5. Provide quick validation steps

# =========================
# VALIDATION CHECK
# =========================

Before finishing:

- No unrelated files modified
- Imports are valid
- Layout is preserved
- Features still function
- Matches shop workflow intent

# =========================
# DO NOT RULES
# =========================

- Do not rewrite entire app for small changes
- Do not change styling globally unless asked
- Do not remove functionality silently
- Do not output partial code when full file is needed
- Do not ignore existing repo patterns