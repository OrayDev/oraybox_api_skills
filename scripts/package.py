#!/usr/bin/env python3
"""Package the oraybox-http-api skill into a .skill zip archive."""

import os
import re
import shutil
import sys
import zipfile


def read_version(skill_dir):
    """Read version from SKILL.md YAML front matter."""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"^version:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def package_skill():
    skill_dir = "oraybox-http-api"

    if not os.path.isdir(skill_dir):
        print(f"Error: {skill_dir} directory not found", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
        print(f"Error: SKILL.md not found in {skill_dir}", file=sys.stderr)
        sys.exit(1)

    version = read_version(skill_dir)
    if version:
        output = f"{skill_dir}-{version}.skill"
    else:
        output = f"{skill_dir}.skill"

    print(f"Packaging {skill_dir} (version: {version or 'unknown'}) -> {output} ...")

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

    # Also keep a .zip copy for general-purpose archive access
    zip_output = output.replace(".skill", ".zip")
    if os.path.exists(zip_output):
        os.remove(zip_output)
    shutil.copy2(output, zip_output)
    print(f"Copied: {zip_output}")


if __name__ == "__main__":
    package_skill()
