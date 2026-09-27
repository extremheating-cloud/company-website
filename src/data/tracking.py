from pathlib import Path

# Google says "paste in <head>": tags/head.html. "Right after <body>": tags/body.html.
TAGS = Path(__file__).resolve().parents[2] / "tags"

HEAD = (TAGS / "head.html").read_text(encoding="utf-8")
BODY_START = (TAGS / "body.html").read_text(encoding="utf-8")
