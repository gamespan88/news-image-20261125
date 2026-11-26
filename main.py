"""Delivery program for the news-image-20261125 entry.

The picture is drawn at build time by build_image.py and committed to this
repository as entry.png. The grader's Python has no imaging library, so this
program is only a standard-library copier: it writes the committed image to
/output/entry.png, byte for byte, every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
