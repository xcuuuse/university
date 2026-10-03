import argparse
import os
import struct

from PIL import Image, ImageDraw
from Crypto.Cipher import AES, DES
from Crypto.Util import Counter

AES_KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
DES_KEY = bytes.fromhex("0001020304050607")
AES_IV = bytes.fromhex("0f0e0d0c0b0a09080706050403020100")
DES_IV = bytes.fromhex("0706050403020100")

ALGORITHMS = {
    "AES": {"module": AES, "key": AES_KEY, "iv": AES_IV, "block": 16},
    "DES": {"module": DES, "key": DES_KEY, "iv": DES_IV, "block": 8},
}
MODES = ["ECB", "CBC", "CTR"]


def to_bmp24(src_path, dst_path, max_width=None):
    img = Image.open(src_path).convert("RGB")
    if max_width and img.width > max_width:
        h = round(img.height * max_width / img.width)
        img = img.resize((max_width, h), Image.LANCZOS)
    img.save(dst_path, format="BMP")
    return dst_path


def split_bmp(path):
    with open(path, "rb") as f:
        raw = f.read()
    if raw[:2] != b"BM":
        raise ValueError(f"{path}: это не BMP-файл")
    offset = struct.unpack_from("<I", raw, 10)[0]
    return raw[:offset], raw[offset:]


def make_cipher(algorithm, mode):
    spec = ALGORITHMS[algorithm]
    module, key, iv = spec["module"], spec["key"], spec["iv"]
    if mode == "ECB":
        return module.new(key, module.MODE_ECB)
    if mode == "CBC":
        return module.new(key, module.MODE_CBC, iv=iv)
    if mode == "CTR":
        counter = Counter.new(spec["block"] * 8, initial_value=0)
        return module.new(key, module.MODE_CTR, counter=counter)
    raise ValueError(f"Неизвестный режим: {mode}")


def encrypt_pixels(data, algorithm, mode):
    block = ALGORITHMS[algorithm]["block"]
    if mode == "CTR":
        # Поточный режим — длина сохраняется автоматически.
        return make_cipher(algorithm, mode).encrypt(data)
    whole = len(data) - len(data) % block
    head = make_cipher(algorithm, mode).encrypt(data[:whole])
    return head + data[whole:]  # незашифрованный хвост < размера блока


def build_grid(paths_with_titles, out_path, columns=4, thumb_width=320):
    thumbs = []
    for title, path in paths_with_titles:
        img = Image.open(path).convert("RGB")
        h = round(img.height * thumb_width / img.width)
        thumbs.append((title, img.resize((thumb_width, h), Image.NEAREST)))
    cell_h = max(t.height for _, t in thumbs)
    pad, caption = 12, 22
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (columns * (thumb_width + pad) + pad,
         rows * (cell_h + caption + pad) + pad),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    for i, (title, thumb) in enumerate(thumbs):
        x = pad + (i % columns) * (thumb_width + pad)
        y = pad + (i // columns) * (cell_h + caption + pad)
        draw.text((x, y + 5), title, fill="black")
        sheet.paste(thumb, (x, y + caption))
    sheet.save(out_path)
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Шифрование изображения блочными шифрами в разных режимах"
    )
    parser.add_argument("image", help="исходное изображение (png, jpg, bmp ...)")
    parser.add_argument("-o", "--outdir", default="out", help="папка результатов")
    parser.add_argument("--width", type=int, default=512,
                        help="уменьшить ширину до N пикселей (0 — не менять)")
    parser.add_argument("--no-grid", action="store_true",
                        help="не собирать сводную таблицу grid.png")
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    original = os.path.join(args.outdir, "00_original.bmp")
    to_bmp24(args.image, original, args.width or None)
    header, pixels = split_bmp(original)
    print(f"Исходное изображение: {original}")
    print(f"Заголовок BMP: {len(header)} байт, пиксельные данные: {len(pixels)} байт\n")
    results = [("Original", original)]
    for algorithm in ALGORITHMS:
        for mode in MODES:
            name = f"{algorithm}_{mode}"
            path = os.path.join(args.outdir, f"{name}.bmp")
            with open(path, "wb") as f:
                f.write(header + encrypt_pixels(pixels, algorithm, mode))
            results.append((f"{algorithm} / {mode}", path))
            print(f"  {name:10s} -> {path}")
    if not args.no_grid:
        grid = build_grid(results, os.path.join(args.outdir, "grid.png"))
        print(f"\nСводная таблица для отчёта: {grid}")


if __name__ == "__main__":
    main()