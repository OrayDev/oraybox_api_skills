#!/usr/bin/env python3
"""Package the oraybox-http-api skill into a .skill zip archive."""

import os
import sys
import zipfile


def package_skill():
    skill_dir = "oraybox-http-api"
    output = f"{skill_dir}.skill"

    if not os.path.isdir(skill_dir):
        print(f"Error: {skill_dir} directory not found", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
        print(f"Error: SKILL.md not found in {skill_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Packaging {skill_dir} -> {output} ...")

    if os.path.exists(output):
        os.remove(output)

    exclude = {"__pycache__", ".DS_Store", ".git"}

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude]
            for file in files:
                if file.endswith(".pyc") or file == ".DS_Store":
                    continue
                filepath = os.path.join(root, file)
                arcname = filepath
                zf.write(filepath, arcname)

    size = os.path.getsize(output)
    print(f"Done: {output} ({size} bytes)")


if __name__ == "__main__":
    package_skill()
