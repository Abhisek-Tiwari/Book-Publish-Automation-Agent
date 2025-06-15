import os
import re

def get_next_version(chapter_id: str, path: str = "data/versions"):
    version_pattern = re.compile(rf"{chapter_id}_v(\d+)_spun\.txt")
    existing_versions = []

    for fname in os.listdir(path):
        match = version_pattern.match(fname)
        if match:
            existing_versions.append(int(match.group(1)))

    next_version = max(existing_versions) + 1 if existing_versions else 1
    return f"v{next_version}"

