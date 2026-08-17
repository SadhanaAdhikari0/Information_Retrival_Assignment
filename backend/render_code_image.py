"""
render_code_image.py — Renders a Python code snippet to a syntax-highlighted
PNG (VS Code "Dark+" palette), matching the style already used for the
report's code-evidence figures.

Used so the "Code Evidence" screenshots in the report can be regenerated
directly from the real, current source files whenever the code changes,
instead of going stale.
"""
import re
from PIL import Image, ImageDraw, ImageFont

FONT_REGULAR = "C:\\Windows\\Fonts\\consola.ttf"
FONT_BOLD    = "C:\\Windows\\Fonts\\consolab.ttf"

BG          = "#1e1e1e"
FG_DEFAULT  = "#d4d4d4"
FG_KEYWORD  = "#c586c0"
FG_FUNC     = "#dcdcaa"
FG_STRING   = "#ce9178"
FG_COMMENT  = "#6a9955"
FG_NUMBER   = "#b5cea8"
FG_BUILTIN  = "#4ec9b0"
FG_IMPORT   = "#c586c0"

KEYWORDS = {
    "def", "return", "if", "elif", "else", "for", "while", "in", "not", "and",
    "or", "is", "import", "from", "as", "class", "try", "except", "finally",
    "with", "global", "lambda", "yield", "raise", "pass", "break", "continue",
    "None", "True", "False", "self", "print",
}
BUILTINS = {"len", "int", "float", "str", "list", "dict", "set", "range",
            "enumerate", "sorted", "sum", "max", "min", "round", "isinstance"}

TOKEN_RE = re.compile(
    r"(?P<comment>#.*$)"
    r"|(?P<string>\"\"\".*?\"\"\"|'''.*?'''|\"[^\"\n]*\"|'[^'\n]*')"
    r"|(?P<number>\b\d+\.?\d*\b)"
    r"|(?P<word>[A-Za-z_][A-Za-z0-9_]*)",
    re.MULTILINE,
)


def _highlight_line(draw, x, y, line, font):
    cursor = x
    pos = 0
    prev_word = None
    for m in TOKEN_RE.finditer(line):
        # draw any un-matched whitespace/punctuation before this token verbatim
        if m.start() > pos:
            gap = line[pos:m.start()]
            draw.text((cursor, y), gap, font=font, fill=FG_DEFAULT)
            cursor += draw.textlength(gap, font=font)

        text = m.group(0)
        if m.lastgroup == "comment":
            color = FG_COMMENT
        elif m.lastgroup == "string":
            color = FG_STRING
        elif m.lastgroup == "number":
            color = FG_NUMBER
        elif m.lastgroup == "word":
            if text in KEYWORDS:
                color = FG_KEYWORD
            elif text in BUILTINS:
                color = FG_BUILTIN
            elif prev_word == "def" or prev_word == "class":
                color = FG_FUNC
            elif re.match(r"^[A-Z]", text):
                color = FG_BUILTIN
            else:
                color = FG_DEFAULT
            prev_word = text if text not in ("self",) else prev_word
        else:
            color = FG_DEFAULT

        draw.text((cursor, y), text, font=font, fill=color)
        cursor += draw.textlength(text, font=font)
        pos = m.end()

    if pos < len(line):
        draw.text((cursor, y), line[pos:], font=font, fill=FG_DEFAULT)


def render_code_to_png(code: str, output_path: str, font_size: int = 16,
                        pad: int = 24, max_width: int = 1180):
    lines = code.rstrip("\n").split("\n")
    font = ImageFont.truetype(FONT_REGULAR, font_size)

    line_height = int(font_size * 1.5)
    longest = max((len(l) for l in lines), default=0)
    char_w = font.getlength("m")
    width = min(max_width, int(pad * 2 + longest * char_w))
    height = pad * 2 + line_height * len(lines)

    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    y = pad
    for line in lines:
        _highlight_line(draw, pad, y, line, font)
        y += line_height

    img.save(output_path)
    print(f"  Rendered: {output_path}  ({width}x{height}, {len(lines)} lines)")


if __name__ == "__main__":
    demo = 'def hello(name: str) -> str:\n    """Docstring."""\n    return f"Hello, {name}!"  # comment\n'
    render_code_to_png(demo, "demo.png")
