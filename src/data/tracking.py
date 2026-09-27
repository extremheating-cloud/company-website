from pathlib import Path

TAGS = Path(__file__).resolve().parents[2] / "tags"

HEAD = (TAGS / "head.html").read_text(encoding="utf-8")
BODY_START = (TAGS / "body.html").read_text(encoding="utf-8")
