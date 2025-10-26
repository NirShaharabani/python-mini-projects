"""Small utility to extract ZIP archives.

This module provides a tiny CLI to extract a .zip file into a directory
named after the archive (by default) or into a user-specified output
directory.

Usage example:
    python extract_zip_files.py -l archive.zip

The script exits with a non-zero code on errors and prints messages to
stderr for failure cases.
"""

from __future__ import annotations

import argparse
import os
import sys
import zipfile
from typing import Optional


def extract(zip_path: str, output_dir: Optional[str] = None) -> None:
    """Extract a ZIP archive to the given output directory.

    If ``output_dir`` is None, the archive will be extracted to a
    subdirectory of the current working directory named after the archive
    (archive base name without the .zip extension).

    Raises:
        FileNotFoundError: if the ``zip_path`` does not exist.
        ValueError: if the file does not have a ``.zip`` extension.
        zipfile.BadZipFile: if the archive is not a valid ZIP file.
    """
    if not zip_path.endswith(".zip"):
        raise ValueError("Not a zip file: %s" % zip_path)

    if not os.path.exists(zip_path):
        raise FileNotFoundError("Zip file not found: %s" % zip_path)

    archive_name = os.path.splitext(os.path.basename(zip_path))[0]
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), archive_name)

    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(output_dir)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="extract_zip_files",
        description=(
            "Extract a .zip archive to a directory "
            "(defaults to archive name)"
        ),
    )
    parser.add_argument(
        "-l",
        "--zippedfile",
        required=True,
        help="Path to the zipped .zip file to extract",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        help=(
            "Optional output directory. If omitted, a directory named "
            "after the archive is used."
        ),
    )
    return parser


def main() -> int:
    """Parse arguments and run extraction. Returns an exit code."""
    parser = _build_parser()
    args = parser.parse_args()

    zip_path = args.zippedfile
    output = args.output

    try:
        extract(zip_path, output)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    except zipfile.BadZipFile as exc:
        print("Invalid zip file:", str(exc), file=sys.stderr)
        return 4

    print("Extracted successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
