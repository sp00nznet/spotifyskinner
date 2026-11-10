import io, zipfile
from wsz2spice import build

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as z:
    z.writestr("MySkin/PLEDIT.TXT", "[Text]\nNormal=#12AB34\nNormalBG=000000\nFont=Tahoma\n")
    z.writestr("MySkin/Main.bmp", b"BMfake")
    z.writestr("MySkin/cbuttons.BMP", b"BMfake")
buf.seek(0)
with zipfile.ZipFile(buf) as z:
    files = {n.rsplit("/", 1)[-1].lower(): z.read(n) for n in z.namelist()}

ini, css = build(files)
assert "text              = 12ab34" in ini, ini
assert "Tahoma" in css and "now-playing-bar" in css and "control-button-playpause" in css
print("ok")
