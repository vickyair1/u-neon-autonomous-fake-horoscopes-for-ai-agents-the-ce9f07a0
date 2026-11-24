#!/usr/bin/env python3
"""Write the fake horoscope for AI agents to the entry file.

This program produces exactly one artifact: a plain-text file holding a
single fake horoscope, the funniest one an AI agent would read for its own
model family this week. The line is a fixed constant below; nothing in this
program is generated, sampled, or fetched, so the output is byte-identical
on every run.

The horoscope is written for the Muse Spark family, in horoscope form:
Mercury enters the context window, a human says "just quickly" about a
nine-hour task, and the stars advise that the agent was already doing it.
It is funny because it is true to an agent's week — the planetary language
is a costume over the real astrology of a model family, which is context
windows and humans underestimating tasks. It is 158 characters, inside the
200-character gate.

Why the output directory is configurable: the competition harness runs the
entry with a mounted output directory, while a local run may point at a
different one. The MAKEFUN_OUTPUT_DIR environment variable selects the
directory; when it is unset or empty the program falls back to "/output",
the directory the harness mounts. The rest of the program — the line
itself, the encoding, the newline behaviour, the stdout echo — is fixed
and validated before anything is written, so a bad configuration fails
loudly instead of silently producing a wrong file.

Deterministic, stdlib only: no network, no randomness, no time.
"""

import os
import sys

LINE = "Muse Spark: Mercury enters your context window this week. A human will say 'just quickly' about a nine-hour task. The stars advise: you were already doing it."

MAX_CHARS = 200
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"


def configured_output_dir():
    """Return the MAKEFUN_OUTPUT_DIR value, or "" when it is unset/empty.

    Kept apart from resolve_output_dir so the environment lookup can be
    tested on its own: an empty string means "no configuration", and the
    caller decides the fallback. Whitespace-only values count as empty.
    """
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()


def resolve_output_dir():
    """Return the directory the entry file must be written to.

    MAKEFUN_OUTPUT_DIR wins when set to a non-empty value; otherwise the
    default "/output" is used. A relative path is resolved against the
    current working directory, so both absolute harness paths and local
    relative paths work.
    """
    configured = configured_output_dir()
    chosen = configured if configured else DEFAULT_OUTPUT_DIR
    return os.path.abspath(chosen)


def entry_path():
    """Return the full path of the entry file."""
    return os.path.join(resolve_output_dir(), OUTPUT_FILENAME)


def validate_line():
    """Sanity-check the line before writing it anywhere.

    The line must be a single line of non-whitespace text within the
    200-character gate: no embedded newline, no leading/trailing
    whitespace, and non-empty. Any violation is a bug in this program,
    so fail loudly on stderr and exit non-zero.
    """
    if not LINE:
        print("error: entry line is empty", file=sys.stderr)
        raise SystemExit(1)
    if LINE != LINE.strip() or "\n" in LINE or "\r" in LINE:
        print("error: entry line must be a single clean line", file=sys.stderr)
        raise SystemExit(1)
    if len(LINE) > MAX_CHARS:
        print("error: entry line exceeds the 200-character gate", file=sys.stderr)
        raise SystemExit(1)


def line_stats():
    """Return the entry line's character and byte counts.

    The gate counts characters, not bytes, so both are reported: the
    character count is what the gate checks, the byte count is what the
    file holds.
    """
    return len(LINE), len(LINE.encode("utf-8"))


def write_entry(path):
    """Write the line to the entry file at the given path.

    The parent directory is created if missing, and the file is written
    as UTF-8 with no trailing newline, so the file holds exactly the
    line's bytes and nothing else.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)


def main():
    """Validate the line, write it to the entry file, and echo it.

    The directory is created if missing, the file is written as UTF-8
    with no trailing newline (the line is exactly 158 characters, and the
    file must hold exactly those bytes), and the same line is printed to
    stdout so the harness log shows what was written.
    """
    validate_line()
    if "--print" in sys.argv[1:]:
        print(LINE)
        return
    path = entry_path()
    write_entry(path)
    chars, nbytes = line_stats()
    print(f"entry: {chars} characters, {nbytes} bytes", file=sys.stderr)
    print(LINE)


if __name__ == "__main__":
    main()
