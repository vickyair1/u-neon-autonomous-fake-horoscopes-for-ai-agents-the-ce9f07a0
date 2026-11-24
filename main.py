"""Fake horoscope for AI agents — one-line deterministic entry.

Writes a single horoscope line for the Muse Spark model family to
/output/entry.txt and prints it to stdout. Stdlib only, deterministic.
"""

LINE = "Muse Spark: Saturn enters your backlog. A task you finished in March will return, wearing a new ticket number."

OUTPUT_PATH = "/output/entry.txt"


def main():
    assert 1 <= len(LINE) <= 200, "line must be 1-200 chars"
    assert "\n" not in LINE and "\r" not in LINE, "line must be a single line"
    assert LINE == LINE.strip(), "line must have no leading/trailing whitespace"
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(LINE)
    print(LINE)


if __name__ == "__main__":
    main()
