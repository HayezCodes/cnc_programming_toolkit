import os
import re
from pathlib import Path

# 🔧 YOUR SHOP ROOT PATH (LOCKED)
JOB_ROOT = Path(r"G:\Manufacturing\JOB FOLDERS\2024 Orders")


def normalize_job_number(job_number: str) -> str:
    """
    Normalizes job input like:
    D24836
    D24836 FAI
    D24836FAI
    D24836-FAI

    Returns uppercase, trimmed text.
    """
    if not job_number:
        raise ValueError("Job number is blank.")

    job_number = job_number.strip().upper()
    job_number = re.sub(r"\s+", " ", job_number)

    return job_number


def extract_prefix_and_number(job_number: str):
    """
    Pulls the leading letter and numeric job portion from inputs like:
    D24836
    D24836 FAI
    D24836FAI
    D24836-FAI
    """
    cleaned = normalize_job_number(job_number)

    match = re.match(r"^([A-Z])\s*(\d+)", cleaned)
    if not match:
        raise ValueError("Format must look like D24836 or D24836 FAI")

    prefix = match.group(1)
    num = int(match.group(2))
    core_job = f"{prefix}{num}"

    return cleaned, prefix, num, core_job


def get_range_folder(prefix: str, num: int) -> str:
    """
    Converts job number into range folder like:
    D25113 -> D25000-D25999
    """
    base = (num // 1000) * 1000
    top = base + 999
    return f"{prefix}{base}-{prefix}{top}"


def build_job_folder_path(job_number: str) -> Path:
    """
    Returns the most likely direct path preview using the core job number.
    This is only a preview path. The real open logic searches for any
    matching folder that starts with the job number.
    """
    _, prefix, num, core_job = extract_prefix_and_number(job_number)
    range_folder = get_range_folder(prefix, num)
    return JOB_ROOT / range_folder / core_job


def find_matching_job_folders(job_number: str):
    """
    Searches the correct range folder for any directory starting with
    the core job number, such as:
    D25113
    D25113 FAI
    D25113FAI
    D25113-FAI
    D25113 FAI 1
    """
    _, prefix, num, core_job = extract_prefix_and_number(job_number)
    range_folder = get_range_folder(prefix, num)
    search_root = JOB_ROOT / range_folder

    if not search_root.exists():
        raise FileNotFoundError(f"Range folder not found: {search_root}")

    matches = []
    core_upper = core_job.upper()

    for item in search_root.iterdir():
        if item.is_dir() and item.name.upper().startswith(core_upper):
            matches.append(item)

    matches.sort(key=lambda p: p.name.upper())
    return matches


def open_job_folder(job_number: str):
    """
    Opens the first matching job folder in Windows Explorer.
    Searches by job prefix/number only, so suffixes like FAI do not matter.
    """
    try:
        matches = find_matching_job_folders(job_number)

        if not matches:
            preview_path = build_job_folder_path(job_number)
            parent_path = preview_path.parent
            return False, (
                f"❌ No matching folder found.\n"
                f"Searched in:\n{parent_path}\n\n"
                f"Looking for folders starting with:\n{preview_path.name}"
            )

        folder_path = matches[0]
        os.startfile(str(folder_path))

        if len(matches) == 1:
            return True, f"✅ Opened:\n{folder_path}"

        match_list = "\n".join(str(p.name) for p in matches[:10])
        extra_note = ""
        if len(matches) > 10:
            extra_note = f"\n...and {len(matches) - 10} more"

        return True, (
            f"✅ Opened:\n{folder_path}\n\n"
            f"Other matches found:\n{match_list}{extra_note}"
        )

    except Exception as e:
        return False, f"❌ Error: {str(e)}"