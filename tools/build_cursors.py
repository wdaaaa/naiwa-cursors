"""从 1024px 母版重建 .cur 光标文件。

流程与原始文件一致：按 alpha 裁边 -> 等比缩放到边长 -> 居中；
热点按 manifest.json 中的 256 基准值等比缩放；
每档额外描 1px 深色边，保证白色图形在浅色背景上依然清晰。

依赖：pip install pillow numpy scipy
用法：python tools/build_cursors.py
"""

import json
import struct
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
MASTER_DIR = ROOT / "cursor_assets" / "masters"
MANIFEST = ROOT / "manifest.json"
SIZES = (32, 48, 64, 128, 256)
RIM_RGB = (12, 12, 12)


def glyph_mask(im):
    """白色图形（含深色描边）的遮罩，用于在每档补 1px 描边。"""
    a = np.asarray(im.convert("RGBA")).astype(np.int16)
    r, g, b, alpha = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = mx - mn
    neutral = (alpha >= 200) & (sat <= 10)
    seed = neutral & ((mx >= 250) | (mx <= 60))
    labels, count = ndimage.label(seed)
    if count == 0:
        return np.zeros(alpha.shape, bool)
    sizes = ndimage.sum(seed, labels, range(1, count + 1))
    keep = [i + 1 for i in range(count) if sizes[i] >= 3000]
    mask = np.isin(labels, keep)
    return ndimage.binary_closing(mask, np.ones((3, 3)), iterations=2)


def fit_layer(layer, alpha_bbox, size, resample):
    """按 alpha 裁边、等比缩放并居中。"""
    x0, y0, x1, y1 = alpha_bbox
    crop = layer.crop((x0, y0, x1, y1))
    w, h = crop.size
    scale = size / max(w, h)
    nw, nh = round(w * scale), round(h * scale)
    resized = crop.resize((nw, nh), resample)
    canvas = Image.new(layer.mode, (size, size), 0)
    canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2))
    return canvas


def add_rim(frame, mask):
    a = np.asarray(frame).copy()
    ring = ndimage.binary_dilation(mask, ndimage.generate_binary_structure(2, 2), 1) & ~mask
    a[ring] = [*RIM_RGB, 255]
    return Image.fromarray(a, "RGBA")


def encode_frame(frame):
    """32bpp BMP + AND mask（兼容旧版软件）。"""
    size = frame.size[0]
    rgba = np.asarray(frame.convert("RGBA"))
    bgra = rgba[..., [2, 1, 0, 3]][::-1]  # bottom-up BGRA
    header = struct.pack("<IiiHHIIiiII", 40, size, size * 2, 1, 32, 0,
                         size * size * 4, 0, 0, 0, 0)
    xor = bgra.tobytes()

    transparent = rgba[..., 3] < 128
    mask_stride = ((size + 31) // 32) * 4
    mask = np.zeros((size, mask_stride), dtype=np.uint8)
    for y in range(size):
        row = transparent[size - 1 - y]
        bits = np.packbits(row, bitorder="big")
        mask[y, : len(bits)] = bits
    return header + xor + mask[::-1].tobytes()


def write_cur(frames, hotspots, out_path):
    count = len(frames)
    entries, blobs = [], []
    offset = 6 + 16 * count
    for frame, (hx, hy) in zip(frames, hotspots):
        blob = encode_frame(frame)
        size = frame.size[0]
        entries.append(struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0,
                                   hx, hy, len(blob), offset))
        blobs.append(blob)
        offset += len(blob)
    with open(out_path, "wb") as f:
        f.write(struct.pack("<HHH", 0, 2, count))
        for entry in entries:
            f.write(entry)
        for blob in blobs:
            f.write(blob)


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for state in manifest["states"]:
        path = MASTER_DIR / state["master"]
        im = Image.open(path).convert("RGBA")
        alpha = np.asarray(im)[..., 3]
        ys, xs = np.where(alpha > 0)
        bbox = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)

        mask = glyph_mask(im)
        mask_img = Image.fromarray((mask * 255).astype(np.uint8), "L")

        frames, hotspots = [], []
        for size in SIZES:
            frame = fit_layer(im, bbox, size, Image.LANCZOS)
            mask_s = np.asarray(fit_layer(mask_img, bbox, size, Image.LANCZOS)) >= 100
            frame = add_rim(frame, mask_s)
            frames.append(frame)
            hx, hy = state["hotspot_256"]
            hotspots.append((round(hx * size / 256), round(hy * size / 256)))

        out = ROOT / state["file"]
        write_cur(frames, hotspots, out)
        print(f"{state['file']:28s} hotspot256={state['hotspot_256']} -> ok")


if __name__ == "__main__":
    main()