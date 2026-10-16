#!/usr/bin/env python3
"""Gera a pixel art original do protótipo.

Rode de novo depois de mudar uma cor ou um sprite:

    python3 tools/generate_art.py

As cores da personagem ficam no bloco PALETTE, logo abaixo.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# --- Paleta. Altere aqui para recolorir a personagem e o mundo. ---

INK = (58, 36, 44, 255)

SKIN = (255, 246, 240, 255)
SKIN_S = (236, 214, 206, 255)
BLUSH = (236, 146, 150, 255)
MOUTH = (176, 104, 112, 255)
EYE = (58, 36, 44, 255)

HAIR = (28, 26, 32, 255)
HAIR_L = (58, 56, 66, 255)
HAIR_D = (14, 12, 18, 255)
RIBBON = (196, 82, 104, 255)
RIBBON_L = (230, 150, 160, 255)

WOOL = (255, 240, 226, 255)
WOOL_S = (236, 206, 184, 255)
WOOL_D = (204, 164, 142, 255)
SKIRT = (118, 168, 136, 255)
SKIRT_S = (82, 132, 108, 255)
SHOE = (108, 64, 58, 255)
SHOE_L = (148, 96, 80, 255)

PLASTER = (240, 220, 198, 255)
PLASTER_S = (220, 192, 168, 255)
BEAM = (122, 76, 54, 255)
BEAM_D = (90, 54, 42, 255)
BEAM_L = (156, 104, 72, 255)
FLOOR_A = (196, 146, 102, 255)
FLOOR_B = (176, 126, 86, 255)
FLOOR_L = (214, 170, 126, 255)
FLOOR_D = (150, 104, 72, 255)
BASE = (112, 72, 50, 255)
RUG = (186, 92, 104, 255)
RUG_D = (150, 64, 80, 255)
RUG_L = (214, 140, 146, 255)
SKY_WIN = (186, 214, 216, 255)
SKY_WIN_L = (230, 244, 236, 255)
CURTAIN = (214, 130, 138, 255)
CURTAIN_D = (176, 96, 108, 255)

SKY_TOP = (168, 198, 208, 255)
SKY_MID = (214, 226, 220, 255)
SKY_HOR = (255, 232, 206, 255)
CLOUD = (255, 248, 242, 255)
ROOF = (176, 84, 74, 255)
ROOF_D = (140, 60, 58, 255)
ROOF_L = (204, 116, 98, 255)
WALL = (255, 242, 226, 255)
WALL_S = (232, 210, 186, 255)
DOOR = (122, 74, 52, 255)
DOOR_D = (86, 52, 40, 255)
DOOR_L = (164, 108, 74, 255)
GRASS = (154, 186, 112, 255)
GRASS_D = (118, 154, 86, 255)
GRASS_L = (186, 210, 138, 255)
PATH = (224, 190, 156, 255)
PATH_D = (196, 160, 128, 255)
PATH_L = (240, 214, 184, 255)
LEAF = (78, 140, 86, 255)
LEAF_D = (52, 104, 68, 255)
LEAF_L = (128, 176, 112, 255)
POT = (184, 102, 78, 255)
POT_D = (140, 72, 58, 255)
POT_L = (214, 140, 112, 255)
CAT = (214, 142, 78, 255)
CAT_D = (168, 96, 52, 255)
CAT_L = (240, 184, 122, 255)
CAT_S = (92, 58, 48, 255)
GIFT = (255, 236, 214, 255)
CAKE = (255, 236, 220, 255)
FROST = (244, 176, 184, 255)
FLAME = (255, 214, 96, 255)

LEGEND = {
    "H": HAIR,
    "L": HAIR_L,
    "D": HAIR_D,
    "R": RIBBON,
    "r": RIBBON_L,
    "S": SKIN,
    "s": SKIN_S,
    "E": EYE,
    "B": BLUSH,
    "M": MOUTH,
    "W": WOOL,
    "w": WOOL_S,
    "v": WOOL_D,
    "K": SKIRT,
    "k": SKIRT_S,
    "O": SHOE,
    "o": SHOE_L,
    "T": CAT,
    "t": CAT_D,
    "Y": CAT_L,
    "P": POT,
    "p": POT_D,
    "G": LEAF,
    "g": LEAF_D,
    "J": LEAF_L,
    "F": GIFT,
    "f": FROST,
    "C": CAKE,
    "N": INK,
    "n": (22, 22, 28, 255),
    "I": (255, 252, 246, 255),
    "Q": (28, 26, 32, 255),
    "q": (58, 54, 62, 255),
    "Z": (214, 176, 78, 255),
}


def new(w: int, h: int) -> Image.Image:
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def fill_rect(im: Image.Image, x: int, y: int, w: int, h: int, color: tuple) -> None:
    if w <= 0 or h <= 0:
        return
    ImageDraw.Draw(im).rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def pix(im: Image.Image, x: int, y: int, color: tuple) -> None:
    if 0 <= x < im.size[0] and 0 <= y < im.size[1]:
        im.putpixel((x, y), color)


def paint(rows: list[str]) -> Image.Image:
    width = len(rows[0])
    for index, row in enumerate(rows):
        if len(row) != width:
            raise SystemExit(f"linha {index} tem {len(row)} colunas, esperado {width}: [{row}]")
    image = new(width, len(rows))
    pixels = image.load()
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == ".":
                continue
            if char not in LEGEND:
                raise SystemExit(f"cor desconhecida {char!r} na linha {y}")
            pixels[x, y] = LEGEND[char]
    return image


def outline(image: Image.Image, color: tuple = INK) -> Image.Image:
    """Contorno só na silhueta externa, para não tapar olhos, pernas ou o vão da cerca."""
    source = image.copy()
    src = source.load()
    width, height = image.size
    exterior = [[False] * width for _ in range(height)]
    stack: list[tuple[int, int]] = []
    for x in range(width):
        stack.append((x, 0))
        stack.append((x, height - 1))
    for y in range(height):
        stack.append((0, y))
        stack.append((width - 1, y))
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= width or y >= height or exterior[y][x]:
            continue
        if src[x, y][3] != 0:
            continue
        exterior[y][x] = True
        stack.extend(((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
    out = image.load()
    for y in range(height):
        for x in range(width):
            if src[x, y][3] != 0 or not exterior[y][x]:
                continue
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < width and 0 <= ny < height and src[nx, ny][3] != 0:
                    out[x, y] = color
                    break
    return image


def shift(image: Image.Image, dy: int) -> Image.Image:
    moved = new(*image.size)
    moved.alpha_composite(image, (0, dy))
    return moved


def shift_shoes(image: Image.Image, left_dy: int, right_dy: int) -> Image.Image:
    """Desloca os sapatos para o ciclo de caminhada. Esquerda e direita do sprite."""
    source = image.copy()
    src = source.load()
    out = image.load()
    width, height = image.size
    shoe_colors = {SHOE[:3], SHOE_L[:3]}
    found: list[tuple[int, int, tuple]] = []
    for y in range(height):
        for x in range(width):
            pixel = src[x, y]
            if pixel[3] and pixel[:3] in shoe_colors:
                found.append((x, y, pixel))
                out[x, y] = (0, 0, 0, 0)
    for x, y, pixel in found:
        dy = left_dy if x < width // 2 else right_dy
        ny = y + dy
        if 0 <= ny < height:
            out[x, ny] = pixel
    return image


def scale(image: Image.Image, factor: int) -> Image.Image:
    return image.resize((image.size[0] * factor, image.size[1] * factor), Image.NEAREST)


def paste_feet(dest: Image.Image, sprite: Image.Image, feet_x: int, feet_y: int) -> None:
    dest.alpha_composite(sprite, (feet_x - sprite.size[0] // 2, feet_y - sprite.size[1]))


# --- Personagem -----------------------------------------------------------

def blank(width: int = 16, height: int = 24) -> list[list[str]]:
    return [["."] * width for _ in range(height)]


def stamp(grid: list[list[str]], x: int, y: int, w: int, h: int, char: str) -> None:
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if 0 <= xx < len(grid[0]) and 0 <= yy < len(grid):
                grid[yy][xx] = char


def dot(grid: list[list[str]], x: int, y: int, char: str) -> None:
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        grid[y][x] = char


def grid_image(grid: list[list[str]]) -> Image.Image:
    return paint(["".join(row) for row in grid])


def build_front(step: int) -> Image.Image:
    """step 0 parado, 1 pé direito à frente, -1 pé esquerdo à frente."""
    grid = blank()
    stamp(grid, 3, 2, 10, 4, "H")
    stamp(grid, 5, 2, 4, 2, "L")
    stamp(grid, 4, 6, 8, 1, "H")
    stamp(grid, 2, 4, 2, 9, "H")
    stamp(grid, 12, 4, 2, 9, "H")
    stamp(grid, 4, 7, 8, 5, "S")
    stamp(grid, 5, 8, 2, 2, "E")
    stamp(grid, 9, 8, 2, 2, "E")
    dot(grid, 5, 8, "I")
    dot(grid, 9, 8, "I")
    stamp(grid, 4, 7, 8, 1, "n")
    dot(grid, 4, 8, "n")
    dot(grid, 7, 8, "n")
    dot(grid, 8, 8, "n")
    dot(grid, 11, 8, "n")
    dot(grid, 4, 10, "B")
    dot(grid, 11, 10, "B")
    dot(grid, 7, 11, "M")
    dot(grid, 8, 11, "M")
    stamp(grid, 3, 12, 10, 5, "W")
    stamp(grid, 3, 12, 10, 1, "v")
    stamp(grid, 3, 13, 2, 3, "w")
    stamp(grid, 11, 13, 2, 3, "w")
    dot(grid, 7, 14, "R")
    dot(grid, 8, 14, "r")
    stamp(grid, 4, 16, 8, 1, "w")
    stamp(grid, 4, 17, 8, 2, "K")
    left_dy = 0
    right_dy = 0
    if step == 1:
        left_dy, right_dy = -1, 1
    elif step == -1:
        left_dy, right_dy = 1, -1

    def leg(x: int, dy: int) -> None:
        stamp(grid, x, 19 + dy, 2, 1, "k")
        stamp(grid, x, 20 + dy, 2, 2, "O")
        dot(grid, x, 20 + dy, "o")

    leg(4, left_dy)
    leg(10, right_dy)
    return grid_image(grid)


def build_side(step: int) -> Image.Image:
    """Olhando para a direita. step 0 parado, 1 e -1 são os passos."""
    grid = blank()
    stamp(grid, 3, 2, 7, 8, "H")
    stamp(grid, 4, 2, 3, 2, "L")
    stamp(grid, 6, 7, 6, 5, "S")
    stamp(grid, 10, 8, 2, 2, "E")
    dot(grid, 10, 8, "I")
    stamp(grid, 9, 7, 4, 1, "n")
    dot(grid, 9, 8, "n")
    dot(grid, 12, 8, "n")
    dot(grid, 13, 9, "s")
    dot(grid, 9, 10, "B")
    dot(grid, 11, 10, "M")
    stamp(grid, 5, 12, 7, 5, "W")
    stamp(grid, 5, 12, 7, 1, "v")
    stamp(grid, 11, 13, 2, 3, "w")
    stamp(grid, 6, 16, 5, 1, "w")
    stamp(grid, 6, 17, 5, 2, "K")
    if step == 0:
        stamp(grid, 7, 19, 3, 1, "k")
        stamp(grid, 7, 20, 3, 2, "O")
        dot(grid, 7, 20, "o")
    elif step == 1:
        stamp(grid, 4, 19, 2, 1, "k")
        stamp(grid, 4, 20, 2, 2, "O")
        stamp(grid, 9, 18, 3, 1, "k")
        stamp(grid, 9, 19, 3, 2, "O")
        dot(grid, 9, 19, "o")
    else:
        stamp(grid, 9, 19, 2, 1, "k")
        stamp(grid, 9, 20, 2, 2, "O")
        stamp(grid, 5, 18, 3, 1, "k")
        stamp(grid, 5, 19, 3, 2, "O")
        dot(grid, 5, 19, "o")
    return grid_image(grid)


def build_back(step: int) -> Image.Image:
    grid = blank()
    stamp(grid, 3, 2, 10, 9, "H")
    stamp(grid, 5, 2, 4, 2, "L")
    stamp(grid, 2, 4, 2, 8, "H")
    stamp(grid, 12, 4, 2, 8, "H")
    stamp(grid, 3, 10, 10, 5, "W")
    stamp(grid, 3, 10, 10, 1, "v")
    stamp(grid, 3, 11, 2, 3, "w")
    stamp(grid, 11, 11, 2, 3, "w")
    stamp(grid, 4, 14, 8, 1, "w")
    stamp(grid, 4, 15, 8, 3, "K")
    left_dy = 0
    right_dy = 0
    if step == 1:
        left_dy, right_dy = -1, 1
    elif step == -1:
        left_dy, right_dy = 1, -1

    def leg(x: int, dy: int) -> None:
        stamp(grid, x, 18 + dy, 2, 1, "k")
        stamp(grid, x, 19 + dy, 2, 2, "O")
        dot(grid, x, 19 + dy, "o")

    leg(4, left_dy)
    leg(10, right_dy)
    return grid_image(grid)


def to_elegant(frame: Image.Image, view: str) -> Image.Image:
    """Troca a roupa por um vestido preto e marca joias douradas."""
    cloth = {WOOL[:3], WOOL_S[:3], WOOL_D[:3], SKIRT[:3], SKIRT_S[:3]}
    image = frame.copy()
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            if pixel[3] == 0 or pixel[:3] not in cloth:
                continue
            pixels[x, y] = (58, 54, 62, 255) if pixel[:3] in {WOOL_S[:3], WOOL_D[:3], SKIRT_S[:3]} else (24, 22, 28, 255)
    if view == "front":
        for x in (6, 7, 8, 9):
            pix(image, x, 12, (214, 176, 78, 255))
        pix(image, 7, 13, (232, 198, 110, 255))
        pix(image, 3, 9, (214, 176, 78, 255))
        pix(image, 12, 9, (214, 176, 78, 255))
    elif view == "side":
        for x in (8, 9, 10):
            pix(image, x, 12, (214, 176, 78, 255))
        pix(image, 12, 9, (214, 176, 78, 255))
    else:
        for x in (6, 7, 8, 9):
            pix(image, x, 10, (214, 176, 78, 255))
    return image


def character_sheet(elegant: bool = False) -> Image.Image:
    rows = []
    for builder, view in zip((build_front, build_side, build_back), ("front", "side", "back")):
        stand = builder(0)
        stride_a = builder(1)
        stride_b = builder(-1)
        if elegant:
            stand = to_elegant(stand, view)
            stride_a = to_elegant(stride_a, view)
            stride_b = to_elegant(stride_b, view)
        stand = outline(stand)
        stride_a = outline(stride_a)
        stride_b = outline(stride_b)
        rows.append(
            [
                stand,
                shift(stand, -1),
                stride_a,
                shift(stand, -1),
                stride_b,
                shift(stand, -1),
            ]
        )
    sheet = new(16 * 6, 24 * 3)
    for row_index, frames in enumerate(rows):
        for col_index, frame in enumerate(frames):
            sheet.alpha_composite(frame, (col_index * 16, row_index * 24))
    return sheet


# --- Objetos --------------------------------------------------------------

PLANT = outline(
    paint(
        [
            "......JGJ.......",
            ".....JGGGG......",
            "....GGGgGGG.....",
            "...GGGgJgGGG....",
            "....GGgGgGG.....",
            "......GgG.......",
            "......GgG.......",
            "......pPp.......",
            ".....PPPPPP.....",
            "....PPPPPPp.....",
            "....PPppPPP.....",
            ".....PPPPP......",
            "......ppp.......",
            "................",
        ]
    )
)

FLOWERS = outline(
    paint(
        [
            "....rR....Rr....",
            "...rRRr..rRRr...",
            "....rR....Rr....",
            ".....G....G.....",
            "....JG....GJ....",
            "......G..G......",
            ".......GG.......",
            "......pPp.......",
            ".....PPPPPP.....",
            "....PPPpPPP.....",
            ".....PPPPP......",
            "................",
        ]
    )
)

def build_cat(blink: bool) -> Image.Image:
    grid = blank(16, 16)
    stamp(grid, 2, 1, 3, 2, "t")
    stamp(grid, 8, 1, 3, 2, "t")
    dot(grid, 3, 2, "R")
    dot(grid, 9, 2, "R")
    stamp(grid, 1, 3, 11, 5, "T")
    stamp(grid, 2, 3, 9, 1, "Y")
    if blink:
        stamp(grid, 3, 5, 2, 1, "N")
        stamp(grid, 8, 5, 2, 1, "N")
    else:
        stamp(grid, 3, 5, 2, 2, "N")
        stamp(grid, 8, 5, 2, 2, "N")
        dot(grid, 3, 5, "I")
        dot(grid, 8, 5, "I")
    dot(grid, 6, 7, "R")
    stamp(grid, 1, 8, 10, 4, "T")
    stamp(grid, 3, 9, 4, 2, "Y")
    stamp(grid, 2, 10, 2, 1, "t")
    stamp(grid, 7, 9, 2, 1, "t")
    stamp(grid, 2, 12, 3, 2, "T")
    stamp(grid, 7, 12, 3, 2, "T")
    if blink:
        stamp(grid, 10, 6, 2, 4, "t")
        stamp(grid, 11, 5, 3, 2, "T")
        stamp(grid, 13, 6, 2, 2, "Y")
    else:
        stamp(grid, 10, 9, 4, 2, "T")
        stamp(grid, 13, 7, 2, 3, "t")
        dot(grid, 14, 7, "Y")
    return outline(grid_image(grid))

def draw_bench() -> Image.Image:
    image = new(36, 22)
    # assento
    fill_rect(image, 2, 8, 32, 5, BEAM)
    fill_rect(image, 2, 8, 32, 1, BEAM_L)
    fill_rect(image, 2, 12, 32, 1, BEAM_D)
    # pernas
    fill_rect(image, 4, 13, 3, 6, BEAM_D)
    fill_rect(image, 28, 13, 3, 6, BEAM_D)
    fill_rect(image, 4, 13, 1, 6, BEAM_L)
    fill_rect(image, 28, 13, 1, 6, BEAM_L)
    # presente
    fill_rect(image, 20, 2, 10, 8, GIFT)
    fill_rect(image, 24, 2, 2, 8, RIBBON)
    fill_rect(image, 20, 5, 10, 2, RIBBON)
    pix(image, 24, 0, RIBBON)
    pix(image, 25, 0, RIBBON_L)
    pix(image, 23, 1, RIBBON)
    pix(image, 26, 1, RIBBON)
    pix(image, 24, 1, RIBBON_L)
    pix(image, 25, 1, RIBBON_L)
    return outline(image)


def draw_shadow() -> Image.Image:
    image = new(12, 4)
    pixels = (
        "....NNNN....",
        "..NNNNNNNN..",
        "..NNNNNNNN..",
        "....NNNN....",
    )
    px = image.load()
    for y, row in enumerate(pixels):
        for x, char in enumerate(row):
            if char == "N":
                px[x, y] = (58, 36, 44, 110)
    return image


def draw_key_chip() -> Image.Image:
    image = new(13, 13)
    fill_rect(image, 0, 0, 13, 13, INK)
    fill_rect(image, 1, 1, 11, 11, (255, 244, 230, 255))
    # letra E, 5x7, centrada
    e = (
        ".....",
        ".NNN.",
        ".N...",
        ".NNN.",
        ".N...",
        ".NNN.",
        ".....",
    )
    px = image.load()
    for y, row in enumerate(e):
        for x, char in enumerate(row):
            if char == "N":
                px[4 + x, 3 + y] = INK
    return image


def draw_arrow() -> Image.Image:
    image = new(7, 5)
    rows = ("..N..", ".NNN.", "NNNNN", ".....", ".....")
    px = image.load()
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == "N":
                px[x, y] = INK
    return image


def draw_dialogue_frame() -> Image.Image:
    image = new(24, 24)
    fill_rect(image, 0, 0, 24, 24, INK)
    fill_rect(image, 2, 2, 20, 20, (255, 244, 228, 255))
    fill_rect(image, 2, 2, 20, 1, (255, 250, 242, 255))
    fill_rect(image, 2, 2, 1, 20, (255, 250, 242, 255))
    # cantos um pouco mais escuros, para o quadro não parecer um retângulo cru
    for x, y in ((1, 1), (22, 1), (1, 22), (22, 22), (0, 0), (23, 0), (0, 23), (23, 23)):
        pix(image, x, y, (0, 0, 0, 0))
    pix(image, 1, 1, INK)
    pix(image, 22, 1, INK)
    pix(image, 1, 22, INK)
    pix(image, 22, 22, INK)
    return image


def draw_icon() -> Image.Image:
    image = new(32, 32)
    fill_rect(image, 0, 0, 32, 32, SKY_HOR)
    # telhado
    for row in range(10):
        inset = 10 - row
        fill_rect(image, 6 + inset // 2, 4 + row, 20 - inset, 1, ROOF if row % 2 == 0 else ROOF_D)
    fill_rect(image, 8, 14, 16, 12, WALL)
    fill_rect(image, 13, 18, 6, 8, DOOR)
    pix(image, 17, 21, FLAME)
    # coração pequeno
    heart = ((14, 8), (15, 8), (17, 8), (18, 8), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9), (19, 9), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (15, 11), (16, 11), (17, 11), (16, 12))
    for x, y in heart:
        pix(image, x, y, RIBBON)
    return image.resize((128, 128), Image.NEAREST)


# --- Mapas ----------------------------------------------------------------

def wood_floor(image: Image.Image, x0: int, y0: int, x1: int, y1: int) -> None:
    pixels = image.load()
    for y in range(y0, y1):
        stripe = (y // 5) % 2
        for x in range(x0, x1):
            color = FLOOR_A if stripe == 0 else FLOOR_B
            if (x * 13 + y * 3) % 37 == 0:
                color = FLOOR_L
            if (x * 5 + y) % 53 == 0:
                color = FLOOR_D
            pixels[x, y] = color
        if y % 5 == 0:
            for x in range(x0, x1):
                if (x + y) % 3 != 0:
                    pixels[x, y] = FLOOR_D


def draw_bed(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x + 6, y + 36, 44, 3, FLOOR_D)
    fill_rect(image, x, y + 4, 4, 32, BEAM_D)
    fill_rect(image, x + 50, y + 4, 4, 32, BEAM_D)
    fill_rect(image, x, y + 4, 1, 32, BEAM_L)
    fill_rect(image, x + 2, y, 50, 12, BEAM)
    fill_rect(image, x + 2, y, 50, 2, BEAM_L)
    fill_rect(image, x + 2, y + 10, 50, 2, BEAM_D)
    fill_rect(image, x + 4, y + 12, 46, 20, (244, 228, 214, 255))
    fill_rect(image, x + 8, y + 13, 18, 8, (255, 250, 244, 255))
    fill_rect(image, x + 8, y + 20, 18, 1, (220, 196, 184, 255))
    fill_rect(image, x + 4, y + 22, 46, 12, RUG)
    fill_rect(image, x + 4, y + 22, 46, 2, RUG_L)
    fill_rect(image, x + 10, y + 26, 14, 2, RUG_D)
    fill_rect(image, x + 2, y + 32, 50, 5, BEAM)
    fill_rect(image, x + 2, y + 32, 50, 1, BEAM_L)


def draw_table(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x + 4, y + 16, 3, 16, BEAM_D)
    fill_rect(image, x + 48, y + 16, 3, 16, BEAM_D)
    fill_rect(image, x, y, 56, 18, INK)
    fill_rect(image, x + 1, y + 1, 54, 14, BEAM)
    fill_rect(image, x + 1, y + 1, 54, 2, BEAM_L)
    fill_rect(image, x + 1, y + 13, 54, 2, BEAM_D)
    # bolo
    fill_rect(image, x + 20, y + 8, 16, 2, (232, 196, 176, 255))
    fill_rect(image, x + 22, y + 4, 12, 5, CAKE)
    fill_rect(image, x + 22, y + 4, 12, 2, FROST)
    pix(image, x + 27, y + 3, FROST)
    pix(image, x + 27, y + 2, (255, 248, 230, 255))
    pix(image, x + 27, y + 1, FLAME)
    pix(image, x + 28, y + 1, (255, 244, 210, 255))
    pix(image, x + 24, y + 5, (255, 220, 214, 255))
    pix(image, x + 30, y + 6, (236, 150, 156, 255))


def draw_picture(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x, y, 28, 22, BEAM_D)
    fill_rect(image, x + 2, y + 2, 24, 18, (255, 246, 232, 255))
    # duas pessoas e um gato, bem pequenos
    fill_rect(image, x + 6, y + 6, 4, 4, HAIR)
    fill_rect(image, x + 7, y + 9, 2, 2, SKIN)
    fill_rect(image, x + 6, y + 11, 4, 5, RIBBON)
    fill_rect(image, x + 14, y + 6, 4, 4, (64, 78, 112, 255))
    fill_rect(image, x + 15, y + 9, 2, 2, SKIN)
    fill_rect(image, x + 14, y + 11, 4, 5, (96, 122, 150, 255))
    pix(image, x + 11, y + 8, RIBBON)
    pix(image, x + 12, y + 8, RIBBON)
    pix(image, x + 11, y + 9, RIBBON)
    pix(image, x + 12, y + 9, RIBBON_L)
    fill_rect(image, x + 20, y + 12, 4, 3, CAT)
    pix(image, x + 20, y + 11, CAT_D)
    pix(image, x + 23, y + 11, CAT_D)


def draw_window(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    fill_rect(image, x, y, w, h, BEAM_D)
    fill_rect(image, x + 2, y + 2, w - 4, h - 4, SKY_WIN)
    # brilho
    for i in range(6):
        pix(image, x + 4 + i, y + 4, SKY_WIN_L)
    mid_x = x + w // 2
    mid_y = y + h // 2
    fill_rect(image, mid_x - 1, y, 2, h, BEAM)
    fill_rect(image, x, mid_y - 1, w, 2, BEAM)
    # cortinas amarradas
    fill_rect(image, x - 3, y + 2, 4, h - 4, CURTAIN)
    fill_rect(image, x + w - 1, y + 2, 4, h - 4, CURTAIN)
    fill_rect(image, x - 3, y + h - 8, 4, 2, CURTAIN_D)
    fill_rect(image, x + w - 1, y + h - 8, 4, 2, CURTAIN_D)


# Paredes claras. Na cozinha, a lajota da parede é marrom claro.
WALL_C = (242, 238, 230, 255)
WALL_HI = (250, 248, 244, 255)
WALL_E = (214, 206, 194, 255)
K_TILE = (196, 158, 118, 255)
K_TILE_L = (214, 182, 148, 255)
K_GROUT = (154, 120, 88, 255)
CREAM = (234, 226, 214, 255)
CREAM_G = (214, 204, 190, 255)
BATH_F = (208, 216, 214, 255)
BATH_G = (176, 188, 186, 255)
OPEN_F = (186, 184, 176, 255)
OPEN_D = (166, 164, 156, 255)
PLANT_F = (198, 208, 186, 255)
HALL_F = (200, 192, 178, 255)
HALL_G = (176, 166, 150, 255)
PAVE = (176, 174, 168, 255)
PAVE_D = (148, 146, 140, 255)
PAVE_L = (198, 196, 190, 255)
LAUNDRY_F = (216, 218, 212, 255)

HOUSE_W = 480
HOUSE_H = 368

# Mesma lista vira colisão em scripts/casa_walls.gd.
# O último valor marca a lajota marrom claro da cozinha.
# Chão claro. O último valor marca só a lajota marrom claro da parede da cozinha.
FLOOR_W = (248, 246, 242, 255)
FLOOR_WG = (226, 224, 218, 255)
BATH_W = (238, 242, 240, 255)
BATH_WG = (210, 220, 218, 255)

HOUSE_WALLS: list[tuple[int, int, int, int, bool]] = [
    (0, 0, 480, 8, False),
    (0, 8, 8, 280, False),
    (472, 8, 8, 88, False),
    (472, 96, 8, 92, True),
    (472, 188, 8, 100, False),
    (0, 288, 392, 8, False),
    (424, 288, 56, 8, False),
    (0, 296, 8, 72, False),
    (472, 296, 8, 72, False),
    (0, 360, 480, 8, False),
    (128, 8, 8, 24, False),
    (128, 64, 8, 32, False),
    (336, 8, 8, 28, False),
    (336, 68, 8, 28, False),
    (8, 88, 148, 8, False),
    (188, 88, 72, 8, False),
    (292, 88, 44, 8, False),
    (336, 88, 136, 8, True),
    (152, 96, 8, 20, False),
    (152, 140, 8, 8, False),
    (152, 172, 8, 12, False),
    (224, 96, 8, 80, False),
    (8, 176, 104, 8, False),
    (140, 176, 12, 8, False),
    (232, 176, 24, 8, False),
    (288, 176, 48, 8, False),
    (336, 96, 8, 88, True),
    (336, 184, 8, 8, False),
    (336, 224, 8, 64, False),
    (56, 184, 8, 16, False),
    (56, 224, 8, 16, False),
    (104, 184, 8, 56, False),
    (152, 184, 8, 56, False),
    (8, 240, 64, 8, False),
    (104, 240, 56, 8, False),
    (344, 248, 48, 8, False),
    (424, 248, 48, 8, False),
]


def grid_floor(image: Image.Image, x0: int, y0: int, x1: int, y1: int, fill: tuple, grout: tuple, step: int) -> None:
    pixels = image.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            pixels[x, y] = grout if x % step == 0 or y % step == 0 else fill


def paint_light_wall(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    fill_rect(image, x, y, w, h, WALL_C)
    fill_rect(image, x, y, w, 1, WALL_HI)
    fill_rect(image, x, y + h - 1, w, 1, WALL_E)
    fill_rect(image, x + w - 1, y, 1, h, WALL_E)


def paint_tile_wall(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    pixels = image.load()
    for py in range(y, y + h):
        for px in range(x, x + w):
            if px % 5 == 0 or py % 5 == 0:
                pixels[px, py] = K_GROUT
            elif (px // 5 + py // 5) % 2 == 0:
                pixels[px, py] = K_TILE_L
            else:
                pixels[px, py] = K_TILE


def wall_window(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    fill_rect(image, x, y, w, h, BEAM_D)
    fill_rect(image, x + 1, y + 1, w - 2, h - 2, SKY_WIN_L)
    if w >= 8:
        fill_rect(image, x + w // 2, y, 1, h, BEAM)


def draw_wardrobe(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    fill_rect(image, x, y, w, h, BEAM_D)
    fill_rect(image, x + 2, y + 2, w - 4, h - 4, BEAM)
    fill_rect(image, x + 2, y + 2, w - 4, 2, BEAM_L)
    mid = x + w // 2
    fill_rect(image, mid, y + 2, 1, h - 4, BEAM_D)
    pix(image, mid - 3, y + h // 2, BEAM_L)
    pix(image, mid + 2, y + h // 2, BEAM_L)


def draw_sofa(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    fill_rect(image, x, y, w, h, (150, 96, 96, 255))
    fill_rect(image, x + 2, y + 2, w - 4, h - 5, (196, 128, 122, 255))
    fill_rect(image, x + 4, y + 3, 16, h - 8, (214, 156, 148, 255))
    fill_rect(image, x + w - 20, y + 3, 16, h - 8, (214, 156, 148, 255))


def draw_machine(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x, y, 36, 22, (214, 218, 220, 255))
    fill_rect(image, x, y, 36, 3, (176, 184, 188, 255))
    fill_rect(image, x + 6, y + 6, 14, 12, (140, 164, 170, 255))
    fill_rect(image, x + 9, y + 9, 8, 6, (224, 236, 238, 255))
    fill_rect(image, x + 24, y + 6, 8, 10, (72, 80, 86, 255))
    pix(image, x + 26, y + 8, (120, 190, 140, 255))


def draw_piano(image: Image.Image, x: int, y: int) -> None:
    # Piano vertical, sem cauda. O armário encosta na parede e o teclado olha o cômodo.
    fill_rect(image, x, y, 14, 44, (36, 30, 34, 255))
    fill_rect(image, x, y, 14, 3, (72, 60, 64, 255))
    fill_rect(image, x + 2, y + 6, 10, 14, (22, 18, 22, 255))
    fill_rect(image, x + 10, y + 22, 8, 16, (244, 240, 232, 255))
    for key in range(0, 14, 3):
        fill_rect(image, x + 11, y + 23 + key, 4, 2, (28, 24, 28, 255))
    fill_rect(image, x + 2, y + 40, 3, 4, (24, 20, 24, 255))
    fill_rect(image, x + 9, y + 40, 3, 4, (24, 20, 24, 255))
    pix(image, x + 5, y + 43, (186, 156, 72, 255))
    pix(image, x + 8, y + 43, (186, 156, 72, 255))


def draw_toilet(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x + 1, y, 8, 4, (210, 210, 206, 255))
    fill_rect(image, x, y + 3, 10, 10, (248, 248, 246, 255))
    fill_rect(image, x + 2, y + 5, 6, 6, (150, 186, 194, 255))
    fill_rect(image, x, y + 3, 10, 1, (180, 180, 176, 255))


def draw_bath_sink(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x, y, 14, 10, (236, 236, 232, 255))
    fill_rect(image, x + 3, y + 2, 8, 6, (140, 178, 186, 255))
    pix(image, x + 6, y + 1, (170, 174, 170, 255))


def door_leaf(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    fill_rect(image, x, y, w, h, DOOR)
    fill_rect(image, x, y, w, 1, DOOR_L)
    fill_rect(image, x, y + h - 1, w, 1, DOOR_D)
    if h >= w:
        pix(image, x + w // 2, y + h - 4, (232, 196, 96, 255))
    else:
        pix(image, x + w - 4, y + h // 2, (232, 196, 96, 255))


def draw_shower(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    glass = (186, 206, 210, 255)
    fill_rect(image, x, y, w, 2, glass)
    fill_rect(image, x, y, 2, h, glass)
    fill_rect(image, x + w - 2, y, 2, h, glass)
    fill_rect(image, x, y + h - 2, w, 2, glass)


def frame_gap_x(image: Image.Image, x: int, y: int, w: int, h: int = 8) -> None:
    fill_rect(image, x - 3, y, 3, h, DOOR_D)
    fill_rect(image, x + w, y, 3, h, DOOR_D)
    fill_rect(image, x, y + h - 2, w, 2, (236, 228, 216, 255))


def frame_gap_y(image: Image.Image, x: int, y: int, h: int, w: int = 8) -> None:
    fill_rect(image, x, y - 3, w, 3, DOOR_D)
    fill_rect(image, x, y + h, w, 3, DOOR_D)
    fill_rect(image, x, y, 2, h, (236, 228, 216, 255))


def draw_saints(image: Image.Image, x: int, y: int, w: int) -> None:
    fill_rect(image, x, y, w, 14, BEAM_D)
    fill_rect(image, x + 1, y + 1, w - 2, 12, BEAM)
    fill_rect(image, x + 1, y + 1, w - 2, 2, BEAM_L)
    robes = ((240, 236, 228, 255), (110, 146, 186, 255), (176, 140, 96, 255))
    for index, robe in enumerate(robes):
        fx = x + 8 + index * 16
        fill_rect(image, fx, y + 5, 6, 7, robe)
        pix(image, fx + 2, y + 3, SKIN)
        pix(image, fx + 3, y + 3, SKIN)


def draw_stove(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x, y, 22, 16, (64, 66, 70, 255))
    fill_rect(image, x + 2, y + 2, 7, 5, (36, 38, 42, 255))
    fill_rect(image, x + 12, y + 2, 7, 5, (36, 38, 42, 255))
    pix(image, x + 5, y + 4, (120, 122, 126, 255))
    pix(image, x + 15, y + 4, (120, 122, 126, 255))
    fill_rect(image, x + 11, y - 2, 8, 4, (90, 94, 98, 255))
    pix(image, x + 13, y - 4, (210, 214, 216, 255))
    pix(image, x + 15, y - 6, (210, 214, 216, 255))


def draw_sink(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x, y, 26, 14, (224, 224, 220, 255))
    fill_rect(image, x + 4, y + 3, 14, 8, (160, 186, 192, 255))
    pix(image, x + 20, y + 4, (170, 174, 170, 255))


def draw_counter(image: Image.Image, x: int, y: int, w: int, h: int, top: tuple) -> None:
    fill_rect(image, x, y, w, h, BEAM)
    fill_rect(image, x, y, w, 3, top)
    fill_rect(image, x, y + h - 2, w, 2, BEAM_D)


def draw_tv_shelf(image: Image.Image, x: int, y: int, w: int) -> None:
    fill_rect(image, x, y, w, 12, BEAM_D)
    fill_rect(image, x + 1, y + 1, w - 2, 10, BEAM)
    fill_rect(image, x + w // 2 - 8, y + 2, 16, 6, (36, 44, 52, 255))
    fill_rect(image, x + w // 2 - 6, y + 3, 12, 4, (150, 186, 190, 255))


def draw_books(image: Image.Image, x: int, y: int, w: int) -> None:
    fill_rect(image, x, y, w, 12, BEAM_D)
    spines = (RIBBON, (90, 114, 156, 255), LEAF, (176, 140, 72, 255), (150, 96, 96, 255))
    bx = x + 2
    index = 0
    while bx < x + w - 4:
        fill_rect(image, bx, y + 2, 3, 8, spines[index % len(spines)])
        bx += 4
        index += 1


def draw_pc(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    fill_rect(image, x, y, w, h, BEAM)
    fill_rect(image, x, y, w, 2, BEAM_L)
    fill_rect(image, x + w // 2 - 7, y + 2, 14, 8, (36, 44, 52, 255))
    fill_rect(image, x + w // 2 - 5, y + 3, 10, 6, SKY_WIN)


def draw_bed_v(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x, y, 28, 6, BEAM)
    fill_rect(image, x, y, 28, 2, BEAM_L)
    fill_rect(image, x + 2, y + 6, 24, 28, (244, 228, 214, 255))
    fill_rect(image, x + 4, y + 8, 10, 7, (255, 250, 244, 255))
    fill_rect(image, x + 15, y + 8, 8, 7, (232, 214, 214, 255))
    fill_rect(image, x + 2, y + 16, 24, 2, (220, 196, 184, 255))
    fill_rect(image, x + 2, y + 18, 24, 14, RUG)
    fill_rect(image, x + 2, y + 18, 24, 2, RUG_L)
    fill_rect(image, x, y + 38, 28, 6, BEAM_D)


def draw_plain_table(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    fill_rect(image, x, y, w, h, BEAM)
    fill_rect(image, x, y, w, 2, BEAM_L)
    fill_rect(image, x, y + h - 2, w, 2, BEAM_D)
    chair = (156, 108, 84, 255)
    fill_rect(image, x + 6, y - 3, 8, 3, chair)
    fill_rect(image, x + w - 14, y - 3, 8, 3, chair)
    fill_rect(image, x + 6, y + h, 8, 3, chair)
    fill_rect(image, x + w - 14, y + h, 8, 3, chair)


def feet_blocked(px: int, py: int, rects: list[tuple[int, int, int, int]]) -> bool:
    left = px - 4
    top = py - 5
    right = px + 4
    bottom = py
    if left < 0 or top < 0 or right > HOUSE_W or bottom > HOUSE_H:
        return True
    for x, y, w, h in rects:
        if right > x and left < x + w and bottom > y and top < y + h:
            return True
    return False


def assert_paths(rects: list[tuple[int, int, int, int]]) -> None:
    start = (70, 158)
    goals = {
        "spawn_direita": (86, 158),
        "spawn_cima": (70, 148),
        "cama": (48, 150),
        "casal": (60, 70),
        "banho_casal": (168, 48),
        "aberta": (270, 50),
        "lavanderia": (400, 50),
        "visita": (280, 140),
        "cozinha": (430, 148),
        "jantar": (420, 230),
        "corredor": (190, 140),
        "piano": (110, 258),
        "sala": (300, 250),
        "plantas": (80, 210),
        "banho_quarto": (148, 208),
        "hall": (408, 268),
        "porta": (408, 278),
    }
    for name, point in {"amanda": start, **goals}.items():
        if feet_blocked(point[0], point[1], rects):
            raise SystemExit(f"ponto preso ({name}): {point}")
    seen = {start}
    queue = [start]
    while queue:
        x, y = queue.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            nxt = (nx, ny)
            if nxt in seen or feet_blocked(nx, ny, rects):
                continue
            seen.add(nxt)
            queue.append(nxt)
    missing = [name for name, point in goals.items() if point not in seen]
    if missing:
        raise SystemExit("sem caminho até: " + ", ".join(missing))


def write_casa_walls(rects: list[tuple[int, int, int, int]]) -> None:
    lines = [
        "class_name CasaWalls",
        "extends RefCounted",
        "",
        "## Paredes e móveis sólidos da casa.",
        "## Sai de tools/generate_art.py, da mesma lista que desenha o mapa.",
        "",
        "const SIZE := Vector2i(480, 368)",
        "",
        "const RECTS: Array[Rect2] = [",
    ]
    for x, y, w, h in rects:
        lines.append(f"\tRect2({x}, {y}, {w}, {h}),")
    lines.append("]")
    lines.append("")
    (ROOT / "scripts" / "casa_walls.gd").write_text("\n".join(lines), encoding="utf-8")


def draw_casa() -> Image.Image:
    image = Image.new("RGBA", (HOUSE_W, HOUSE_H), WALL_C)
    grid_floor(image, 8, 8, 472, 288, FLOOR_W, FLOOR_WG, 16)
    pixels = image.load()
    for y in range(296, 360):
        for x in range(8, 472):
            if x % 8 == 0 or y % 8 == 0:
                pixels[x, y] = PAVE_D
            elif (x // 8 + y // 8) % 2 == 0:
                pixels[x, y] = PAVE_L
            else:
                pixels[x, y] = PAVE

    solids: list[tuple[int, int, int, int]] = [(x, y, w, h) for x, y, w, h, _tile in HOUSE_WALLS]
    for x, y, w, h, tile in HOUSE_WALLS:
        if tile:
            paint_tile_wall(image, x, y, w, h)
        else:
            paint_light_wall(image, x, y, w, h)

    draw_bed(image, 16, 18)
    solids.append((16, 18, 54, 40))
    draw_bath_sink(image, 148, 18)
    solids.append((148, 18, 14, 10))
    draw_toilet(image, 172, 62)
    solids.append((172, 62, 10, 14))

    draw_bed_v(image, 16, 122)
    solids.append((16, 122, 28, 44))
    draw_tv_shelf(image, 52, 104, 70)
    solids.append((52, 104, 70, 12))
    draw_wardrobe(image, 96, 118, 18, 40)
    solids.append((96, 118, 18, 40))
    fill_rect(image, 20, 168, 22, 6, (214, 186, 176, 255))

    draw_bed_v(image, 240, 108)
    solids.append((240, 108, 28, 44))
    draw_wardrobe(image, 304, 108, 16, 32)
    solids.append((304, 108, 16, 32))
    draw_pc(image, 246, 156, 44, 12)
    solids.append((246, 156, 44, 12))

    draw_machine(image, 390, 18)
    solids.append((390, 18, 36, 22))

    draw_counter(image, 360, 108, 96, 12, (232, 220, 204, 255))
    solids.append((360, 108, 96, 12))
    draw_stove(image, 360, 124)
    solids.append((360, 124, 22, 16))
    draw_sink(image, 388, 124)
    solids.append((388, 124, 26, 14))
    draw_wardrobe(image, 448, 112, 14, 32)
    solids.append((448, 112, 14, 32))
    draw_counter(image, 380, 156, 72, 12, (214, 176, 140, 255))
    solids.append((380, 156, 72, 12))
    for stool in (392, 424):
        fill_rect(image, stool, 168, 8, 4, (140, 96, 70, 255))
        solids.append((stool, 168, 8, 4))
    draw_plain_table(image, 352, 220, 52, 14)
    solids.append((352, 217, 52, 20))

    for y in range(184, 240):
        for x in range(112, 152):
            pixels[x, y] = (232, 236, 234, 255) if (x // 8 + y // 8) % 2 == 0 else (244, 246, 244, 255)
    fill_rect(image, 140, 186, 8, 10, (186, 206, 210, 255))
    fill_rect(image, 142, 188, 4, 6, (230, 240, 242, 255))
    draw_bath_sink(image, 116, 192)
    solids.append((116, 192, 14, 10))
    draw_toilet(image, 132, 192)
    solids.append((132, 192, 10, 14))
    draw_shower(image, 118, 214, 22, 18)
    solids.append((118, 214, 22, 18))
    for index, color in enumerate((LEAF_D, LEAF, LEAF_L)):
        px = 70 + index * 10
        fill_rect(image, px, 200, 6, 4, (150, 96, 70, 255))
        blob(image, px + 3, 196, 4, 4, color)
    solids.append((70, 192, 28, 12))

    fill_rect(image, 168, 242, 120, 36, (214, 176, 176, 255))
    fill_rect(image, 172, 246, 112, 28, (196, 140, 146, 255))
    draw_books(image, 176, 208, 90)
    solids.append((176, 208, 90, 12))
    draw_tv_shelf(image, 184, 226, 64)
    solids.append((184, 226, 64, 12))
    draw_sofa(image, 180, 246, 64, 16)
    solids.append((180, 246, 64, 16))
    draw_plain_table(image, 176, 266, 96, 14)
    solids.append((176, 263, 96, 20))
    draw_piano(image, 12, 250)
    solids.append((12, 250, 18, 36))
    draw_saints(image, 40, 252, 48)
    solids.append((40, 252, 48, 14))

    wall_window(image, 40, 1, 28, 6)
    wall_window(image, 250, 1, 18, 6)
    wall_window(image, 390, 1, 22, 6)
    wall_window(image, 473, 120, 6, 20)
    wall_window(image, 473, 210, 6, 16)
    for wx in (200, 248, 296):
        wall_window(image, wx, 289, 16, 6)

    frame_gap_y(image, 128, 32, 32)
    frame_gap_x(image, 156, 88, 32)
    frame_gap_y(image, 336, 36, 32)
    frame_gap_x(image, 260, 88, 32)
    frame_gap_y(image, 152, 116, 24)
    frame_gap_y(image, 152, 148, 24)
    frame_gap_x(image, 256, 176, 32)
    frame_gap_y(image, 336, 192, 32)
    frame_gap_x(image, 112, 176, 28)
    frame_gap_x(image, 72, 240, 32)
    frame_gap_x(image, 392, 248, 32)
    door_leaf(image, 136, 32, 12, 8)
    solids.append((136, 32, 12, 8))
    door_leaf(image, 156, 78, 8, 10)
    solids.append((156, 78, 8, 10))
    door_leaf(image, 344, 36, 12, 8)
    solids.append((344, 36, 12, 8))
    door_leaf(image, 160, 116, 12, 8)
    solids.append((160, 116, 12, 8))
    door_leaf(image, 160, 148, 12, 8)
    solids.append((160, 148, 12, 8))
    door_leaf(image, 256, 166, 8, 10)
    solids.append((256, 166, 8, 10))
    door_leaf(image, 344, 192, 12, 8)
    solids.append((344, 192, 12, 8))
    door_leaf(image, 392, 258, 10, 14)
    solids.append((392, 258, 10, 14))
    fill_rect(image, 390, 288, 2, 8, DOOR_D)
    fill_rect(image, 424, 288, 2, 8, DOOR_D)
    fill_rect(image, 396, 292, 24, 2, (236, 228, 216, 255))

    assert_paths(solids)
    write_casa_walls(solids)
    return image


def blob(image: Image.Image, cx: int, cy: int, rx: int, ry: int, color: tuple) -> None:
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            nx = (x - cx) / max(rx, 1)
            ny = (y - cy) / max(ry, 1)
            if nx * nx + ny * ny <= 1 and 0 <= x < image.size[0] and 0 <= y < image.size[1]:
                image.putpixel((x, y), color)


def draw_roof(image: Image.Image, x: int, y: int, w: int, h: int) -> None:
    pixels = image.load()
    for row in range(h):
        inset = int((h - row) * 0.45)
        left = x + inset
        right = x + w - inset
        for px in range(left, right):
            if 0 <= px < image.size[0]:
                tile = (px // 4 + row // 3) % 2
                pixels[px, y + row] = ROOF_D if tile else ROOF
                if row == 0 or px == left or px == right - 1:
                    pixels[px, y + row] = ROOF_D
                elif (px + row) % 7 == 0:
                    pixels[px, y + row] = ROOF_L


def draw_tree(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x + 10, y + 28, 6, 28, BEAM_D)
    fill_rect(image, x + 10, y + 28, 2, 28, BEAM)
    blob(image, x + 13, y + 16, 16, 12, LEAF_D)
    blob(image, x + 8, y + 18, 10, 8, LEAF)
    blob(image, x + 18, y + 20, 9, 7, LEAF)
    blob(image, x + 12, y + 12, 7, 5, LEAF_L)


CITY_W = 400
CITY_H = 180
ASPHALT = (78, 80, 86, 255)
ASPHALT_D = (62, 64, 70, 255)
WALK = (198, 196, 190, 255)
WALK_D = (168, 166, 160, 255)
FACADE = (236, 232, 224, 255)
GYM_C = (176, 186, 196, 255)

CITY_WALLS: list[tuple[int, int, int, int]] = [
    (0, 0, 400, 8),
    (0, 8, 8, 164),
    (392, 8, 8, 164),
    (0, 172, 400, 8),
    (16, 16, 96, 28),
    (16, 44, 28, 8),
    (80, 44, 32, 8),
    (112, 16, 136, 16),
    (248, 16, 128, 28),
    (248, 44, 48, 8),
    (328, 44, 48, 8),
    (376, 16, 16, 20),
]


def write_cidade_walls() -> None:
    lines = [
        "class_name CidadeWalls",
        "extends RefCounted",
        "",
        "## Muros do condomínio. Sai de tools/generate_art.py.",
        "",
        "const SIZE := Vector2i(400, 180)",
        "",
        "const RECTS: Array[Rect2] = [",
    ]
    for x, y, w, h in CITY_WALLS:
        lines.append(f"\tRect2({x}, {y}, {w}, {h}),")
    lines.append("]")
    lines.append("")
    (ROOT / "scripts" / "cidade_walls.gd").write_text("\n".join(lines), encoding="utf-8")


def draw_creta() -> Image.Image:
    image = new(44, 20)
    fill_rect(image, 4, 2, 36, 16, (22, 22, 26, 255))
    fill_rect(image, 2, 4, 4, 12, (22, 22, 26, 255))
    fill_rect(image, 38, 4, 4, 12, (22, 22, 26, 255))
    fill_rect(image, 14, 4, 16, 12, (32, 34, 40, 255))
    fill_rect(image, 22, 5, 6, 10, (150, 176, 186, 255))
    fill_rect(image, 15, 5, 5, 10, (120, 146, 158, 255))
    fill_rect(image, 34, 6, 4, 3, (255, 244, 210, 255))
    fill_rect(image, 6, 6, 4, 3, (220, 60, 54, 255))
    fill_rect(image, 8, 0, 6, 4, (16, 16, 18, 255))
    fill_rect(image, 30, 0, 6, 4, (16, 16, 18, 255))
    fill_rect(image, 8, 16, 6, 4, (16, 16, 18, 255))
    fill_rect(image, 30, 16, 6, 4, (16, 16, 18, 255))
    return image


def draw_heart() -> Image.Image:
    image = new(16, 16)
    fill_rect(image, 3, 3, 4, 3, (214, 72, 96, 255))
    fill_rect(image, 2, 5, 6, 3, (214, 72, 96, 255))
    fill_rect(image, 4, 8, 4, 2, (214, 72, 96, 255))
    fill_rect(image, 8, 3, 5, 8, (236, 228, 226, 255))
    fill_rect(image, 5, 10, 6, 3, (236, 228, 226, 255))
    pix(image, 7, 4, (255, 214, 220, 255))
    return outline(image)


def draw_academia() -> Image.Image:
    image = Image.new("RGBA", (240, 160), (214, 216, 220, 255))
    pixels = image.load()
    for y in range(8, 152):
        for x in range(8, 232):
            pixels[x, y] = (186, 190, 196, 255) if (x // 16 + y // 16) % 2 == 0 else (198, 202, 206, 255)
    paint_light_wall(image, 0, 0, 240, 8)
    paint_light_wall(image, 0, 8, 8, 144)
    paint_light_wall(image, 232, 8, 8, 144)
    paint_light_wall(image, 0, 152, 108, 8)
    paint_light_wall(image, 140, 152, 100, 8)
    fill_rect(image, 16, 16, 90, 8, (150, 168, 178, 255))
    fill_rect(image, 18, 18, 86, 4, (214, 228, 232, 255))
    fill_rect(image, 28, 36, 28, 40, (64, 68, 74, 255))
    fill_rect(image, 36, 44, 16, 16, (36, 38, 42, 255))
    fill_rect(image, 40, 48, 8, 8, (120, 124, 130, 255))
    fill_rect(image, 24, 78, 8, 10, (48, 50, 56, 255))
    fill_rect(image, 52, 78, 8, 10, (48, 50, 56, 255))
    fill_rect(image, 150, 40, 36, 10, (90, 96, 104, 255))
    fill_rect(image, 156, 28, 6, 22, (70, 74, 80, 255))
    fill_rect(image, 174, 28, 6, 22, (70, 74, 80, 255))
    fill_rect(image, 108, 154, 2, 6, DOOR_D)
    fill_rect(image, 138, 154, 2, 6, DOOR_D)
    return image


def _asphalt_grit(x: int, y: int) -> bool:
    """Pontos soltos, sem listra. Listra na rua parecia plantação."""
    n = (x * 374761393 + y * 668265263) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return (n & 255) < 22


def draw_rua() -> Image.Image:
    image = Image.new("RGBA", (CITY_W, CITY_H), WALK)
    pixels = image.load()
    for y in range(60, 96):
        for x in range(8, 392):
            pixels[x, y] = WALK_D if x % 12 == 0 or y % 12 == 0 else WALK
    for y in range(148, 172):
        for x in range(8, 392):
            pixels[x, y] = WALK_D if x % 12 == 0 or y % 12 == 0 else WALK
    for y in range(96, 148):
        for x in range(8, 392):
            pixels[x, y] = ASPHALT_D if _asphalt_grit(x, y) else ASPHALT
    for x in range(24, 380, 18):
        fill_rect(image, x, 118, 8, 2, (214, 206, 120, 255))
    for x, y, w, h in CITY_WALLS:
        if h <= 8 or w <= 8:
            paint_light_wall(image, x, y, w, h)
        elif x >= 248:
            fill_rect(image, x, y, w, h, GYM_C)
            fill_rect(image, x, y, w, 3, (150, 162, 174, 255))
        elif x >= 112 and w > 40:
            fill_rect(image, x, y, w, h, (92, 96, 104, 255))
            fill_rect(image, x + 48, y + 2, 28, 12, (70, 74, 82, 255))
        else:
            fill_rect(image, x, y, w, h, FACADE)
            fill_rect(image, x, y, w, 4, (176, 92, 84, 255))
    wall_window(image, 28, 24, 18, 12)
    wall_window(image, 58, 24, 18, 12)
    wall_window(image, 268, 24, 22, 12)
    wall_window(image, 300, 24, 22, 12)
    fill_rect(image, 42, 44, 2, 8, DOOR_D)
    fill_rect(image, 78, 44, 2, 8, DOOR)
    fill_rect(image, 294, 44, 2, 8, DOOR_D)
    fill_rect(image, 326, 44, 2, 8, DOOR_D)
    fill_rect(image, 360, 28, 8, 18, (64, 68, 74, 255))
    fill_rect(image, 363, 22, 2, 8, (64, 68, 74, 255))
    pix(image, 364, 20, (255, 236, 170, 255))
    write_cidade_walls()
    return image


def contact(frames: list[Image.Image], scale_factor: int) -> Image.Image:
    pad = 2
    width = sum(frame.size[0] + pad for frame in frames) * scale_factor
    height = max(frame.size[1] for frame in frames) * scale_factor
    sheet = Image.new("RGBA", (width, height), (210, 196, 176, 255))
    x = 0
    for frame in frames:
        big = scale(frame, scale_factor)
        sheet.alpha_composite(big, (x, 0))
        x += big.size[0] + pad * scale_factor
    return sheet


MORENO = (186, 124, 86, 255)
MORENO_S = (156, 98, 66, 255)
BROWN = (102, 64, 42, 255)
WHITE_HAIR = (236, 232, 224, 255)
ELDER = (228, 190, 162, 255)
ELDER_S = (196, 156, 132, 255)
GOLD = (214, 176, 78, 255)


def draw_standing(
    skin: tuple,
    skin_s: tuple,
    hair: tuple,
    shirt: tuple,
    pants: tuple,
    glasses: bool = False,
    chubby: bool = False,
    beard: bool = False,
    jewelry: bool = False,
) -> Image.Image:
    image = new(16, 24)
    fill_rect(image, 3, 2, 10, 4, hair)
    fill_rect(image, 2, 4, 2, 7, hair)
    fill_rect(image, 12, 4, 2, 7, hair)
    fill_rect(image, 4, 6, 8, 6, skin)
    pix(image, 5, 8, (255, 252, 246, 255))
    pix(image, 6, 8, EYE)
    pix(image, 9, 8, EYE)
    pix(image, 10, 8, (255, 252, 246, 255))
    if glasses:
        fill_rect(image, 4, 7, 8, 1, (22, 22, 28, 255))
        pix(image, 4, 8, (22, 22, 28, 255))
        pix(image, 7, 8, (22, 22, 28, 255))
        pix(image, 8, 8, (22, 22, 28, 255))
        pix(image, 11, 8, (22, 22, 28, 255))
    if beard:
        fill_rect(image, 5, 10, 6, 2, hair)
    else:
        pix(image, 7, 11, MOUTH)
        pix(image, 8, 11, MOUTH)
    pix(image, 4, 10, skin_s)
    pix(image, 11, 10, skin_s)
    body_w = 12 if chubby else 10
    body_x = 2 if chubby else 3
    fill_rect(image, body_x, 12, body_w, 6, shirt)
    fill_rect(image, body_x, 12, body_w, 1, skin_s if chubby else shirt)
    fill_rect(image, 4, 17, 8, 3, pants)
    fill_rect(image, 4, 20, 3, 2, SHOE)
    fill_rect(image, 9, 20, 3, 2, SHOE)
    if jewelry:
        pix(image, 3, 9, GOLD)
        pix(image, 12, 9, GOLD)
        pix(image, 6, 13, GOLD)
        pix(image, 7, 14, GOLD)
        pix(image, 8, 14, GOLD)
        pix(image, 9, 13, GOLD)
    return outline(image)


def draw_father() -> Image.Image:
    image = new(20, 16)
    fill_rect(image, 6, 0, 8, 3, (168, 164, 158, 255))
    fill_rect(image, 5, 2, 10, 5, ELDER)
    pix(image, 7, 4, EYE)
    pix(image, 12, 4, EYE)
    pix(image, 9, 6, MOUTH)
    fill_rect(image, 2, 7, 16, 7, (64, 92, 140, 255))
    fill_rect(image, 4, 8, 12, 5, (86, 114, 158, 255))
    fill_rect(image, 1, 12, 4, 3, (48, 62, 96, 255))
    fill_rect(image, 15, 12, 4, 3, (48, 62, 96, 255))
    fill_rect(image, 3, 14, 5, 2, (46, 52, 70, 255))
    fill_rect(image, 12, 14, 5, 2, (46, 52, 70, 255))
    return outline(image)


def draw_dog() -> Image.Image:
    image = new(24, 12)
    fill_rect(image, 4, 4, 16, 6, (24, 22, 26, 255))
    fill_rect(image, 2, 5, 4, 4, (24, 22, 26, 255))
    fill_rect(image, 16, 3, 6, 5, (24, 22, 26, 255))
    fill_rect(image, 18, 5, 4, 2, (150, 146, 142, 255))
    pix(image, 20, 4, (250, 246, 240, 255))
    pix(image, 21, 4, EYE)
    pix(image, 22, 6, (120, 80, 80, 255))
    fill_rect(image, 6, 9, 3, 2, (24, 22, 26, 255))
    fill_rect(image, 14, 9, 3, 2, (24, 22, 26, 255))
    fill_rect(image, 1, 6, 2, 3, (24, 22, 26, 255))
    return outline(image)


def draw_tree_campus(image: Image.Image, x: int, y: int) -> None:
    fill_rect(image, x + 6, y + 14, 4, 12, (92, 64, 48, 255))
    blob(image, x + 8, y + 10, 10, 8, LEAF_D)
    blob(image, x + 5, y + 8, 6, 5, LEAF)
    blob(image, x + 11, y + 7, 5, 4, LEAF_L)


GLYPHS = {
    "A": ["010", "101", "111", "101", "101"],
    "C": ["011", "100", "100", "100", "011"],
    "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"],
    "G": ["011", "100", "101", "101", "011"],
    "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "L": ["100", "100", "100", "100", "111"],
    "M": ["101", "111", "101", "101", "101"],
    "O": ["010", "101", "101", "101", "010"],
    "P": ["110", "101", "110", "100", "100"],
    "Q": ["010", "101", "101", "011", "001"],
    "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"],
    "U": ["101", "101", "101", "101", "010"],
    " ": ["000", "000", "000", "000", "000"],
}


def paint_text(image: Image.Image, x: int, y: int, text: str, color: tuple) -> None:
    cursor = x
    for char in text:
        glyph = GLYPHS.get(char, GLYPHS[" "])
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == "1":
                    pix(image, cursor + col, y + row, color)
        cursor += 4


UNI_W = 400
UNI_H = 200
UNI_WALLS: list[tuple[int, int, int, int]] = [
    (0, 0, 400, 8),
    (0, 8, 8, 184),
    (392, 8, 8, 184),
    (0, 192, 400, 8),
    (8, 8, 384, 28),
    (120, 52, 168, 8),
    (120, 60, 8, 44),
    (280, 60, 8, 44),
    (120, 104, 52, 8),
    (204, 104, 84, 8),
    (28, 120, 18, 16),
    (340, 70, 18, 16),
    (48, 150, 16, 16),
    (214, 118, 84, 16),
    (160, 64, 28, 8),
]


def write_ufpa_walls() -> None:
    lines = [
        "class_name UfpaWalls",
        "extends RefCounted",
        "",
        "## Muros da UFPA. Sai de tools/generate_art.py.",
        "",
        "const SIZE := Vector2i(400, 200)",
        "",
        "const RECTS: Array[Rect2] = [",
    ]
    for x, y, w, h in UNI_WALLS:
        lines.append(f"\tRect2({x}, {y}, {w}, {h}),")
    lines.append("]")
    lines.append("")
    (ROOT / "scripts" / "ufpa_walls.gd").write_text("\n".join(lines), encoding="utf-8")


def draw_universidade() -> Image.Image:
    image = Image.new("RGBA", (UNI_W, UNI_H), (214, 208, 196, 255))
    pixels = image.load()
    for y in range(36, 192):
        for x in range(8, 392):
            pixels[x, y] = (198, 192, 180, 255) if (x // 16 + y // 16) % 2 == 0 else (214, 208, 196, 255)
    for y in range(8, 36):
        for x in range(8, 392):
            wave = (x // 6 + y) % 5 == 0
            pixels[x, y] = (96, 156, 180, 255) if wave else (64, 124, 156, 255)
    for x, y, w, h in (
        (120, 52, 168, 8),
        (120, 60, 8, 44),
        (280, 60, 8, 44),
        (120, 104, 52, 8),
        (204, 104, 84, 8),
    ):
        fill_rect(image, x, y, w, h, (232, 214, 186, 255))
        fill_rect(image, x, y, w, 2, (176, 92, 84, 255))
    fill_rect(image, 128, 60, 152, 44, (240, 230, 210, 255))
    fill_rect(image, 160, 64, 28, 8, (48, 58, 70, 255))
    fill_rect(image, 162, 66, 24, 4, (180, 206, 196, 255))
    wall_window(image, 206, 70, 20, 12)
    wall_window(image, 234, 70, 20, 12)
    paint_text(image, 136, 54, "PEDAGOGIA", (92, 48, 40, 255))
    fill_rect(image, 214, 118, 84, 16, (122, 86, 58, 255))
    fill_rect(image, 214, 118, 84, 2, (92, 62, 40, 255))
    paint_text(image, 218, 120, "SO OS MELHORES", (255, 244, 220, 255))
    paint_text(image, 226, 126, "CHEGAM AQUI", (255, 244, 220, 255))
    fill_rect(image, 168, 108, 4, 14, DOOR_D)
    fill_rect(image, 200, 108, 4, 14, DOOR)
    draw_tree_campus(image, 20, 108)
    draw_tree_campus(image, 332, 58)
    draw_tree_campus(image, 40, 138)
    draw_tree_campus(image, 300, 140)
    write_ufpa_walls()
    return image


CLINIC_W = 320
CLINIC_H = 180
CLINIC_WALLS: list[tuple[int, int, int, int]] = [
    (0, 0, 320, 8),
    (0, 8, 8, 164),
    (312, 8, 8, 164),
    (0, 172, 136, 8),
    (184, 172, 136, 8),
    (44, 54, 96, 34),
    (214, 22, 90, 46),
    (18, 22, 22, 24),
    (156, 68, 28, 26),
]


def write_consultorio_walls() -> None:
    lines = [
        "class_name ConsultorioWalls",
        "extends RefCounted",
        "",
        "## Paredes do consultório. Sai de tools/generate_art.py.",
        "",
        "const SIZE := Vector2i(320, 180)",
        "",
        "const RECTS: Array[Rect2] = [",
    ]
    for x, y, w, h in CLINIC_WALLS:
        lines.append(f"\tRect2({x}, {y}, {w}, {h}),")
    lines.append("]")
    lines.append("")
    (ROOT / "scripts" / "consultorio_walls.gd").write_text("\n".join(lines), encoding="utf-8")


def draw_consultorio() -> Image.Image:
    image = Image.new("RGBA", (CLINIC_W, CLINIC_H), (36, 34, 40, 255))
    pixels = image.load()
    stone = (236, 230, 222, 255)
    stone_b = (224, 216, 206, 255)
    grout = (196, 186, 174, 255)
    for y in range(36, 172):
        for x in range(8, 312):
            if x % 18 == 0 or y % 18 == 0:
                pixels[x, y] = grout
            else:
                pixels[x, y] = stone if ((x // 18) + (y // 18)) % 2 == 0 else stone_b
    fill_rect(image, 8, 34, 304, 2, GOLD)
    fill_rect(image, 8, 170, 304, 2, (58, 52, 48, 255))
    fill_rect(image, 78, 10, 132, 22, (214, 176, 78, 255))
    fill_rect(image, 80, 12, 128, 18, (186, 206, 214, 255))
    fill_rect(image, 92, 16, 14, 14, (62, 64, 78, 255))
    fill_rect(image, 112, 18, 22, 12, (48, 50, 62, 255))
    fill_rect(image, 150, 14, 18, 16, (72, 74, 88, 255))
    fill_rect(image, 176, 18, 20, 12, (52, 54, 68, 255))
    fill_rect(image, 40, 70, 104, 36, (52, 48, 46, 255))
    fill_rect(image, 42, 72, 100, 32, (214, 176, 78, 255))
    fill_rect(image, 44, 74, 96, 28, (48, 46, 52, 255))
    fill_rect(image, 44, 58, 96, 28, (28, 26, 30, 255))
    fill_rect(image, 46, 56, 92, 8, (22, 20, 24, 255))
    fill_rect(image, 48, 60, 88, 16, (244, 236, 226, 255))
    fill_rect(image, 48, 74, 88, 6, (232, 220, 206, 255))
    fill_rect(image, 44, 54, 18, 24, (250, 244, 236, 255))
    fill_rect(image, 46, 56, 14, 4, GOLD)
    fill_rect(image, 48, 80, 88, 2, GOLD)
    fill_rect(image, 156, 72, 28, 16, (24, 22, 26, 255))
    fill_rect(image, 158, 68, 24, 8, (32, 30, 34, 255))
    fill_rect(image, 160, 70, 20, 4, (244, 236, 226, 255))
    fill_rect(image, 158, 86, 3, 6, GOLD)
    fill_rect(image, 179, 86, 3, 6, GOLD)
    fill_rect(image, 214, 22, 90, 46, (22, 20, 24, 255))
    fill_rect(image, 214, 64, 90, 4, GOLD)
    fill_rect(image, 222, 28, 18, 22, (48, 46, 50, 255))
    fill_rect(image, 226, 32, 10, 8, (180, 176, 170, 255))
    pix(image, 230, 30, GOLD)
    fill_rect(image, 248, 36, 8, 6, (250, 246, 240, 255))
    fill_rect(image, 260, 36, 8, 6, (250, 246, 240, 255))
    fill_rect(image, 272, 34, 22, 16, (236, 228, 216, 255))
    fill_rect(image, 276, 30, 14, 6, (250, 250, 246, 255))
    fill_rect(image, 18, 36, 22, 12, (46, 72, 58, 255))
    fill_rect(image, 14, 30, 12, 10, (36, 64, 50, 255))
    fill_rect(image, 28, 28, 14, 12, (58, 90, 68, 255))
    fill_rect(image, 22, 44, 14, 10, (20, 18, 22, 255))
    fill_rect(image, 24, 46, 10, 6, (32, 30, 34, 255))
    fill_rect(image, 186, 104, 22, 10, (24, 22, 26, 255))
    fill_rect(image, 190, 100, 14, 8, (250, 244, 232, 255))
    pix(image, 194, 102, (196, 132, 72, 255))
    pix(image, 196, 103, (214, 156, 96, 255))
    pix(image, 198, 102, (176, 112, 64, 255))
    fill_rect(image, 140, 152, 40, 20, (28, 24, 22, 255))
    fill_rect(image, 144, 152, 6, 20, GOLD)
    fill_rect(image, 168, 160, 3, 3, GOLD)
    write_consultorio_walls()
    return image


def draw_heart_more() -> Image.Image:
    image = new(16, 16)
    fill_rect(image, 3, 3, 4, 3, (214, 72, 96, 255))
    fill_rect(image, 2, 5, 6, 3, (214, 72, 96, 255))
    fill_rect(image, 9, 3, 4, 3, (214, 72, 96, 255))
    fill_rect(image, 8, 5, 6, 3, (214, 72, 96, 255))
    fill_rect(image, 4, 8, 8, 2, (236, 228, 226, 255))
    fill_rect(image, 5, 10, 6, 3, (236, 228, 226, 255))
    return outline(image)


def main() -> None:
    for folder in ("sprites", "maps", "ui", "fonts"):
        (ASSETS / folder).mkdir(parents=True, exist_ok=True)

    player = character_sheet()
    elegante = character_sheet(True)
    plant = PLANT
    flowers = FLOWERS
    cat = new(32, 16)
    cat.alpha_composite(build_cat(False), (0, 0))
    cat.alpha_composite(build_cat(True), (16, 0))
    bench = draw_bench()
    casa = draw_casa()
    rua = draw_rua()
    academia = draw_academia()
    creta = draw_creta()
    heart = draw_heart()
    heart_more = draw_heart_more()
    alex = draw_standing(MORENO, MORENO_S, HAIR, (168, 64, 72, 255), (48, 52, 64, 255))
    henrique = draw_standing(MORENO, MORENO_S, HAIR, (64, 104, 156, 255), (48, 52, 64, 255))
    mae = draw_standing(SKIN, SKIN_S, BROWN, (214, 168, 150, 255), (120, 96, 84, 255), glasses=True)
    pai = draw_father()
    cachorra = draw_dog()
    ernani = draw_standing(ELDER, ELDER_S, WHITE_HAIR, (52, 62, 92, 255), (60, 56, 52, 255), beard=True)
    breno = draw_standing(ELDER, ELDER_S, WHITE_HAIR, (120, 84, 58, 255), (48, 52, 60, 255))
    eli = draw_standing(SKIN, SKIN_S, WHITE_HAIR, (22, 20, 24, 255), (16, 14, 18, 255), jewelry=True)
    paciente = draw_standing(SKIN, SKIN_S, (72, 60, 54, 255), (86, 96, 108, 255), (48, 50, 58, 255))

    player.save(ASSETS / "sprites" / "player.png")
    elegante.save(ASSETS / "sprites" / "player_elegante.png")
    alex.save(ASSETS / "sprites" / "alex.png")
    henrique.save(ASSETS / "sprites" / "henrique.png")
    mae.save(ASSETS / "sprites" / "mae.png")
    pai.save(ASSETS / "sprites" / "pai.png")
    cachorra.save(ASSETS / "sprites" / "cachorra.png")
    ernani.save(ASSETS / "sprites" / "ernani.png")
    breno.save(ASSETS / "sprites" / "breno.png")
    eli.save(ASSETS / "sprites" / "eli.png")
    paciente.save(ASSETS / "sprites" / "paciente.png")
    plant.save(ASSETS / "sprites" / "plant.png")
    flowers.save(ASSETS / "sprites" / "flowers.png")
    cat.save(ASSETS / "sprites" / "cat.png")
    bench.save(ASSETS / "sprites" / "bench.png")
    draw_shadow().save(ASSETS / "sprites" / "shadow.png")
    casa.save(ASSETS / "maps" / "casa.png")
    rua.save(ASSETS / "maps" / "rua.png")
    academia.save(ASSETS / "maps" / "academia.png")
    draw_universidade().save(ASSETS / "maps" / "ufpa.png")
    consultorio = draw_consultorio()
    consultorio.save(ASSETS / "maps" / "consultorio.png")
    creta.save(ASSETS / "sprites" / "creta.png")
    heart.save(ASSETS / "sprites" / "heart.png")
    heart_more.save(ASSETS / "sprites" / "heart2.png")
    draw_dialogue_frame().save(ASSETS / "ui" / "dialogue_frame.png")
    draw_key_chip().save(ASSETS / "ui" / "key_e.png")
    draw_arrow().save(ASSETS / "ui" / "arrow.png")
    draw_icon().save(ROOT / "icon.png")

    preview = Path("/tmp/art-preview")
    preview.mkdir(exist_ok=True)
    # folha da personagem: baixo, lado, costas
    scale(player, 4).save(preview / "player.png")
    scale(plant, 6).save(preview / "plant.png")
    scale(flowers, 6).save(preview / "flowers.png")
    scale(cat, 6).save(preview / "cat.png")
    scale(bench, 4).save(preview / "bench.png")

    down = player.crop((0, 0, 16, 24))
    side = player.crop((0, 24, 16, 48))
    casa_preview = casa.copy()
    paste_feet(casa_preview, down, 70, 158)
    paste_feet(casa_preview, plant, 100, 270)
    scale(casa_preview, 2).save(preview / "casa.png")

    rua_preview = rua.copy()
    paste_feet(rua_preview, side, 62, 86)
    paste_feet(rua_preview, creta, 190, 108)
    scale(rua_preview, 2).save(preview / "rua.png")
    scale(academia, 2).save(preview / "academia.png")
    paste_feet(consultorio, eli, 204, 120)
    paste_feet(consultorio, paciente, 78, 136)
    scale(consultorio, 2).save(preview / "consultorio.png")
    print("arte gerada em", ASSETS)


if __name__ == "__main__":
    main()
