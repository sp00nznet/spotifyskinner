"""Convert a classic Winamp 2.x skin (.wsz) into a Spicetify theme.

usage: python wsz2spice.py skin.wsz [themes_dir]
Then: spicetify config current_theme <name> && spicetify apply
"""
import base64, os, re, sys, zipfile

# cbuttons.bmp sprite x-offsets (Winamp 2 spec); row y=0 normal, y=18 pressed
BUTTONS = {
    "skip-back": (0, 23), "play": (23, 23), "pause": (46, 23),
    "skip-forward": (92, 22),
}


def read_skin(path):
    """Return {lowercase basename: bytes}; skins vary in case and folder nesting."""
    with zipfile.ZipFile(path) as z:
        return {os.path.basename(n).lower(): z.read(n) for n in z.namelist() if not n.endswith("/")}


def pledit_colors(files):
    defaults = {"normal": "00ff00", "current": "ffffff", "normalbg": "000000", "selectedbg": "0000c6"}
    txt = files.get("pledit.txt", b"").decode("latin-1")
    for key, val in re.findall(r"(?im)^\s*(\w+)\s*=\s*#?([0-9a-f]{6})", txt):
        if key.lower() in defaults:
            defaults[key.lower()] = val.lower()
    font = re.search(r"(?im)^\s*font\s*=\s*(.+?)\s*$", txt)
    return defaults, font.group(1) if font else "Arial"


def uri(files, name):
    data = files.get(name)
    return f"url(data:image/bmp;base64,{base64.b64encode(data).decode()})" if data else None


def build(files):
    c, font = pledit_colors(files)
    color_ini = "[winamp]\n" + "\n".join(f"{k:<18}= {v}" for k, v in {
        "text": c["normal"], "subtext": c["normal"], "main": c["normalbg"],
        "sidebar": c["normalbg"], "player": c["normalbg"], "card": c["normalbg"],
        "shadow": "000000", "selected-row": c["current"], "button": c["current"],
        "button-active": c["current"], "button-disabled": "555555",
        "tab-active": c["selectedbg"], "notification": c["selectedbg"],
        "notification-error": "ff0000", "misc": c["selectedbg"],
    }.items()) + "\n"

    css = [f"* {{ font-family: '{font}', Arial, sans-serif !important; }}",
           "img, [style*=background] { image-rendering: pixelated; }"]
    main = uri(files, "main.bmp")
    if main:
        css.append(f".Root__now-playing-bar, [data-testid='now-playing-bar'] {{"
                   f" background: {main} center / cover no-repeat !important; image-rendering: pixelated; }}")
    cb = uri(files, "cbuttons.bmp")
    if cb:
        # ponytail: aria-label play/pause is English-only; add locales if someone asks
        for tid, sprite in [("skip-back", "skip-back"), ("skip-forward", "skip-forward"),
                            ("playpause", "play"), ("playpause'][aria-label='Pause", "pause")]:
            x, w = BUTTONS[sprite]
            sel = f"[data-testid='control-button-{tid}']"
            css.append(f"{sel} {{ background: {cb} -{x}px 0 no-repeat !important; width: {w}px !important;"
                       f" height: 18px !important; min-width: 0 !important; border-radius: 0 !important;"
                       f" transform: scale(1.5); image-rendering: pixelated; }}")
            css.append(f"{sel}:active {{ background-position: -{x}px -18px !important; }}")
            css.append(f"{sel} svg, {sel} > span {{ opacity: 0 !important; }}")
    return color_ini, "\n".join(css) + "\n"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    skin = sys.argv[1]
    themes = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.environ["APPDATA"], "spicetify", "Themes")
    name = re.sub(r"\W+", "_", os.path.splitext(os.path.basename(skin))[0])
    out = os.path.join(themes, name)
    os.makedirs(out, exist_ok=True)
    color_ini, css = build(read_skin(skin))
    open(os.path.join(out, "color.ini"), "w").write(color_ini)
    open(os.path.join(out, "user.css"), "w").write(css)
    print(f"wrote {out}\nnext: spicetify config current_theme {name} color_scheme winamp && spicetify apply")


if __name__ == "__main__":
    main()
