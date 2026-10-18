#!/usr/bin/env python3
"""Create private Connect IQ listing assets from audited simulator SAMPLE screenshots.

No personal health metrics or private code are published here. Outputs stay on
the public CI runner until uploaded to a GitHub RELEASE IN THE PRIVATE repo.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path.cwd()
OUT = ROOT / "build" / "store-listing-assets"
OUT.mkdir(parents=True, exist_ok=True)

FILES = [
    ("01-overview-SAMPLE.jpg", "phase05-06-overview-SAMPLE.png"),
    ("02-recovery-SAMPLE.jpg", "phase05-06-recovery-SAMPLE.png"),
    ("03-training-SAMPLE.jpg", "phase05-06-training-SAMPLE.png"),
    ("04-trends-SAMPLE.jpg", "phase05-trends-v2-SAMPLE-final.png"),
    ("05-data-sources-SAMPLE.jpg", "phase05-06-data-sources-SAMPLE.png"),
    ("06-why-SAMPLE.jpg", "phase05-06-why-SAMPLE.png"),
]
SCREENS = ROOT / "docs" / "screenshots"
for out_name, source in FILES:
    original = SCREENS / source
    if not original.is_file():
        raise RuntimeError(f"Missing simulator capture: {source}")
    with Image.open(original) as inp:
        image = inp.convert("RGB")
        image.thumbnail((720, 980), Image.Resampling.LANCZOS)
        dest = OUT / out_name
        for quality in (87, 81, 75, 69, 63, 57, 50):
            image.save(dest, "JPEG", quality=quality, optimize=True, subsampling=0)
            if dest.stat().st_size < 145000:
                break
        if dest.stat().st_size >= 150000:
            raise RuntimeError(f"Screenshot exceeds 150 KB: {out_name}")
        print(f"SCREEN {dest.name}: {image.size} {dest.stat().st_size} bytes")

# Distinctive neutral icon; this is an original generic Fusion graphic, not
# an official Garmin mark or a claim that we render real HRV on the watch.
w = h = 500
tile = Image.new("RGB", (w, h), (9, 18, 32))
pix = tile.load()
for y in range(h):
    for x in range(w):
        radial = max(0, 1-math.hypot(x-250, y-200)/400)
        pix[x, y] = (int(8+8*radial), int(18+21*radial), int(32+28*radial))
d = ImageDraw.Draw(tile)
blue=(48,180,219)
aqua=(91,227,183)
white=(233,244,250)
d.ellipse((114,72,386,344), outline=(38,84,106), width=4)
d.arc((115,74,385,344), 205, 337, fill=blue, width=18)
d.arc((115,74,385,344), 30, 163, fill=aqua, width=18)
# stylized data waves, not a fabricated numeric chart
points=[]
for x in range(149,352,3):
    y=209+14*math.sin((x-149)/22)-8*math.sin((x-149)/8.5)
    points.append((x,int(y)))
d.line(points, fill=white, width=7, joint="curve")
d.ellipse((145,205,153,213), fill=aqua)
d.ellipse((347,207,355,215), fill=blue)
fontpaths=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
def font(sz):
    for p in fontpaths:
        if Path(p).is_file(): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()
def center_line(text, y, f, fill):
    box=d.textbbox((0,0),text,font=f)
    tw=box[2]-box[0]
    d.text(((500-tw)/2,y),text,font=f,fill=fill)
center_line("FUSION",360,font(53),white)
center_line("TRAINING STATUS",424,font(19),(151,198,213))
dest=OUT / "Fusion-cover-500x500.png"
tile.save(dest, "PNG", optimize=True)
if dest.stat().st_size >= 300000: raise RuntimeError("Cover exceeds 300KB")
print(f"COVER {dest.name}: {tile.size} {dest.stat().st_size} bytes")

# Optional square 128x128 app-icon PNG as a store-ready convenience.
square=tile.resize((128,128),Image.Resampling.LANCZOS)
dest=OUT / "Fusion-icon-128x128.png"
square.save(dest, "PNG", optimize=True)
print(f"ICON {dest.name}: {square.size} {dest.stat().st_size} bytes")
