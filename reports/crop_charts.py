"""Remove only unused white screenshot margins for report figures."""

from pathlib import Path
from PIL import Image, ImageChops


assets = Path(__file__).with_name("chart_assets")
for index in range(1, 10):
    source = assets / f"chart_{index:02}.png"
    target = assets / f"figure_{index:02}.png"
    image = Image.open(source).convert("RGB")
    diff = ImageChops.difference(image, Image.new("RGB", image.size, "white"))
    bbox = diff.getbbox()
    if bbox is None:
        raise RuntimeError(f"No chart content in {source}")
    pad = 24
    left, top, right, bottom = bbox
    box = (max(0, left - pad), max(0, top - pad), min(image.width, right + pad), min(image.height, bottom + pad))
    image.crop(box).save(target)
    print(f"{target.name}: {image.size} -> {Image.open(target).size}")
