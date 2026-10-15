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

SKIN = (255, 214, 186, 255)
SKIN_S = (236, 178, 150, 255)
BLUSH = (236, 146, 150, 255)
MOUTH = (176, 104, 112, 255)
EYE = (58, 36, 44, 255)

HAIR = (102, 58, 52, 255)
HAIR_L = (146, 86, 70, 255)
HAIR_D = (72, 40, 40, 255)
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
    "I": (255, 252, 246, 255),
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
    stamp(grid, 5, 3, 3, 2, "R")
    dot(grid, 6, 3, "r")
    stamp(grid, 4, 6, 8, 1, "H")
    stamp(grid, 2, 5, 2, 5, "H")
    stamp(grid, 12, 5, 2, 5, "H")
    stamp(grid, 4, 7, 8, 5, "S")
    stamp(grid, 5, 8, 2, 2, "E")
    stamp(grid, 9, 8, 2, 2, "E")
    dot(grid, 5, 8, "I")
    dot(grid, 9, 8, "I")
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
    stamp(grid, 3, 2, 8, 5, "H")
    stamp(grid, 4, 2, 3, 2, "L")
    stamp(grid, 3, 4, 2, 2, "R")
    dot(grid, 4, 4, "r")
    stamp(grid, 6, 7, 6, 5, "S")
    stamp(grid, 10, 8, 2, 2, "E")
    dot(grid, 10, 8, "I")
    dot(grid, 12, 9, "s")
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
    stamp(grid, 3, 2, 10, 6, "H")
    stamp(grid, 5, 2, 4, 2, "L")
    stamp(grid, 5, 4, 5, 2, "R")
    dot(grid, 7, 4, "r")
    stamp(grid, 2, 5, 2, 4, "H")
    stamp(grid, 12, 5, 2, 4, "H")
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


def character_sheet() -> Image.Image:
    rows = []
    for builder in (build_front, build_side, build_back):
        stand = outline(builder(0))
        stride_a = outline(builder(1))
        stride_b = outline(builder(-1))
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
    (472, 8, 8, 168, False),
    (472, 176, 8, 56, True),
    (472, 232, 8, 56, False),
    (0, 288, 392, 8, False),
    (424, 288, 56, 8, False),
    (0, 296, 8, 72, False),
    (472, 296, 8, 72, False),
    (0, 360, 480, 8, False),
    (152, 8, 8, 104, False),
    (300, 8, 8, 104, False),
    (400, 8, 8, 104, False),
    (8, 104, 32, 8, False),
    (72, 104, 80, 8, False),
    (160, 104, 36, 8, False),
    (228, 104, 72, 8, False),
    (308, 104, 28, 8, False),
    (368, 104, 32, 8, False),
    (408, 104, 16, 8, False),
    (456, 104, 16, 8, False),
    (108, 16, 44, 8, False),
    (108, 16, 8, 20, False),
    (108, 64, 8, 28, False),
    (108, 84, 44, 8, False),
    (228, 12, 72, 8, False),
    (228, 12, 8, 52, False),
    (228, 64, 20, 8, False),
    (280, 64, 20, 8, False),
    (8, 168, 168, 8, False),
    (248, 168, 224, 8, True),
    (168, 176, 8, 24, False),
    (168, 232, 8, 56, False),
    (248, 176, 8, 24, True),
    (248, 232, 8, 56, False),
    (352, 228, 8, 16, False),
    (352, 276, 8, 12, False),
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
    fill_rect(image, x + 4, y + 8, 14, 8, (255, 250, 244, 255))
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
    start = (64, 92)
    goals = {
        "spawn_direita": (80, 92),
        "spawn_cima": (64, 82),
        "cama": (32, 86),
        "banho_amanda": (132, 48),
        "centro": (200, 88),
        "banho_centro": (264, 40),
        "visita": (370, 90),
        "lavanderia": (440, 60),
        "cozinha": (400, 196),
        "jantar": (320, 262),
        "corredor": (200, 140),
        "piano": (100, 240),
        "sala": (110, 210),
        "hall": (408, 252),
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

    draw_bed_v(image, 18, 28)
    solids.append((18, 28, 28, 44))
    draw_tv_shelf(image, 46, 14, 52)
    solids.append((46, 14, 52, 12))
    draw_wardrobe(image, 86, 70, 16, 26)
    solids.append((86, 70, 16, 26))
    draw_bath_sink(image, 118, 28)
    solids.append((118, 28, 14, 10))
    draw_shower(image, 136, 28, 14, 18)
    solids.append((136, 28, 14, 18))
    draw_toilet(image, 120, 66)
    solids.append((120, 66, 10, 14))

    draw_bed(image, 166, 18)
    solids.append((166, 18, 54, 40))
    draw_bath_sink(image, 238, 22)
    solids.append((238, 22, 14, 10))
    draw_toilet(image, 276, 22)
    solids.append((276, 22, 10, 14))
    draw_shower(image, 238, 46, 12, 16)
    solids.append((238, 46, 12, 16))

    draw_bed_v(image, 316, 18)
    solids.append((316, 18, 28, 44))
    draw_wardrobe(image, 364, 16, 16, 34)
    solids.append((364, 16, 16, 34))
    draw_pc(image, 318, 68, 46, 12)
    solids.append((318, 68, 46, 12))

    draw_machine(image, 418, 16)
    solids.append((418, 16, 36, 22))

    draw_counter(image, 300, 178, 140, 12, (232, 220, 204, 255))
    solids.append((300, 178, 140, 12))
    draw_stove(image, 308, 190)
    solids.append((308, 190, 22, 16))
    draw_sink(image, 334, 190)
    solids.append((334, 190, 26, 14))
    draw_wardrobe(image, 448, 178, 14, 36)
    solids.append((448, 178, 14, 36))
    draw_counter(image, 300, 210, 132, 12, (214, 176, 140, 255))
    solids.append((300, 210, 132, 12))
    draw_plain_table(image, 262, 256, 52, 14)
    solids.append((262, 253, 52, 20))
    for stool in (314, 346, 378):
        fill_rect(image, stool, 222, 8, 4, (140, 96, 70, 255))
        solids.append((stool, 222, 8, 4))

    draw_books(image, 20, 178, 80)
    solids.append((20, 178, 80, 12))
    draw_tv_shelf(image, 24, 194, 64)
    solids.append((24, 194, 64, 12))
    draw_sofa(image, 28, 214, 68, 16)
    solids.append((28, 214, 68, 16))
    draw_piano(image, 12, 230)
    solids.append((12, 230, 18, 44))
    draw_saints(image, 40, 232, 52)
    solids.append((40, 232, 52, 14))
    draw_plain_table(image, 56, 258, 80, 14)
    solids.append((56, 255, 80, 20))
    for index, color in enumerate((LEAF_D, LEAF, LEAF_L)):
        px = 132 + index * 8
        fill_rect(image, px, 240, 6, 4, (150, 96, 70, 255))
        blob(image, px + 3, 237, 4, 4, color)
    solids.append((132, 234, 24, 10))

    wall_window(image, 36, 1, 28, 6)
    wall_window(image, 176, 1, 28, 6)
    wall_window(image, 332, 1, 22, 6)
    wall_window(image, 424, 1, 18, 6)
    wall_window(image, 473, 186, 6, 22)
    wall_window(image, 473, 248, 6, 16)
    for wx in (48, 88, 128):
        wall_window(image, wx, 289, 16, 6)

    frame_gap_x(image, 40, 104, 32)
    frame_gap_x(image, 196, 104, 32)
    frame_gap_x(image, 336, 104, 32)
    frame_gap_x(image, 424, 104, 32)
    frame_gap_y(image, 108, 36, 28)
    frame_gap_x(image, 248, 64, 32)
    frame_gap_y(image, 168, 200, 32)
    frame_gap_y(image, 248, 200, 32)
    frame_gap_y(image, 352, 244, 32)
    door_leaf(image, 42, 90, 8, 14)
    solids.append((42, 90, 8, 14))
    door_leaf(image, 198, 90, 8, 14)
    solids.append((198, 90, 8, 14))
    door_leaf(image, 338, 90, 8, 14)
    solids.append((338, 90, 8, 14))
    door_leaf(image, 426, 90, 8, 14)
    solids.append((426, 90, 8, 14))
    door_leaf(image, 116, 56, 12, 8)
    solids.append((116, 56, 12, 8))
    door_leaf(image, 270, 50, 8, 14)
    solids.append((270, 50, 8, 14))
    door_leaf(image, 154, 200, 14, 8)
    solids.append((154, 200, 14, 8))
    door_leaf(image, 256, 200, 14, 8)
    solids.append((256, 200, 14, 8))
    door_leaf(image, 360, 268, 14, 8)
    solids.append((360, 268, 14, 8))
    door_leaf(image, 392, 272, 10, 16)
    solids.append((392, 272, 10, 16))
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


def draw_rua() -> Image.Image:
    image = Image.new("RGBA", (240, 160), GRASS)
    pixels = image.load()
    for y in range(0, 58):
        t = y / 57
        if t < 0.55:
            u = t / 0.55
            color = tuple(int(SKY_TOP[i] + (SKY_MID[i] - SKY_TOP[i]) * u) for i in range(3)) + (255,)
        else:
            u = (t - 0.55) / 0.45
            color = tuple(int(SKY_MID[i] + (SKY_HOR[i] - SKY_MID[i]) * u) for i in range(3)) + (255,)
        for x in range(240):
            pixels[x, y] = color
    blob(image, 46, 18, 18, 6, CLOUD)
    blob(image, 40, 20, 10, 4, CLOUD)
    blob(image, 188, 14, 14, 5, CLOUD)
    blob(image, 196, 16, 8, 3, CLOUD)

    draw_tree(image, 4, 18)

    for y in range(96, 160):
        for x in range(240):
            noise = (x * 19 + y * 7) % 23
            if noise == 0:
                color = GRASS_L
            elif noise < 5:
                color = GRASS_D
            else:
                color = GRASS
            pixels[x, y] = color
    for y in range(154, 160):
        for x in range(240):
            pixels[x, y] = GRASS_D
    for tx, ty in ((28, 118), (40, 142), (206, 118), (214, 140), (170, 146), (20, 130)):
        pix(image, tx, ty, LEAF_D)
        pix(image, tx + 1, ty - 1, LEAF)
        pix(image, tx + 2, ty, LEAF_L)

    # caminho
    for y in range(100, 160):
        for x in range(96, 144):
            color = PATH if (x + y) % 2 == 0 else PATH_D
            if (x * 3 + y) % 11 == 0:
                color = PATH_L
            pixels[x, y] = color
    # pedrinhas
    for sx, sy in ((104, 118), (132, 126), (110, 140), (128, 148), (118, 132)):
        pix(image, sx, sy, (176, 150, 128, 255))

    # casa
    draw_roof(image, 62, 30, 116, 28)
    fill_rect(image, 74, 52, 92, 50, WALL)
    fill_rect(image, 74, 52, 92, 3, WALL_S)
    # janelas acesas de manhã, com cortina
    for wx in (84, 140):
        fill_rect(image, wx, 64, 16, 14, BEAM_D)
        fill_rect(image, wx + 2, 66, 12, 10, SKY_WIN_L)
        fill_rect(image, wx + 7, 66, 2, 10, BEAM)
        fill_rect(image, wx + 2, 70, 12, 2, BEAM)
        fill_rect(image, wx + 2, 72, 5, 4, CURTAIN)
        fill_rect(image, wx + 9, 72, 5, 4, CURTAIN)
    # porta
    fill_rect(image, 108, 70, 24, 32, BEAM_D)
    fill_rect(image, 110, 72, 20, 30, DOOR)
    fill_rect(image, 112, 74, 4, 26, DOOR_L)
    fill_rect(image, 124, 86, 2, 2, FLAME)
    # bandeirinhas
    for index, fx in enumerate(range(96, 150, 8)):
        color = RIBBON if index % 2 == 0 else SKIRT
        pix(image, fx, 56, INK)
        pix(image, fx + 1, 56, INK)
        pix(image, fx, 57, color)
        pix(image, fx + 1, 57, color)
        pix(image, fx, 58, color)
    for fx in range(96, 146):
        if fx % 2 == 0:
            pix(image, fx, 55, INK)

    blob(image, 214, 116, 16, 10, LEAF_D)
    blob(image, 208, 114, 9, 6, LEAF)
    blob(image, 220, 120, 7, 5, LEAF_L)
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


def main() -> None:
    for folder in ("sprites", "maps", "ui", "fonts"):
        (ASSETS / folder).mkdir(parents=True, exist_ok=True)

    player = character_sheet()
    plant = PLANT
    flowers = FLOWERS
    cat = new(32, 16)
    cat.alpha_composite(build_cat(False), (0, 0))
    cat.alpha_composite(build_cat(True), (16, 0))
    bench = draw_bench()
    casa = draw_casa()
    rua = draw_rua()

    player.save(ASSETS / "sprites" / "player.png")
    plant.save(ASSETS / "sprites" / "plant.png")
    flowers.save(ASSETS / "sprites" / "flowers.png")
    cat.save(ASSETS / "sprites" / "cat.png")
    bench.save(ASSETS / "sprites" / "bench.png")
    draw_shadow().save(ASSETS / "sprites" / "shadow.png")
    casa.save(ASSETS / "maps" / "casa.png")
    rua.save(ASSETS / "maps" / "rua.png")
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
    paste_feet(casa_preview, down, 64, 92)
    paste_feet(casa_preview, plant, 146, 250)
    scale(casa_preview, 2).save(preview / "casa.png")

    rua_preview = rua.copy()
    paste_feet(rua_preview, side, 120, 124)
    paste_feet(rua_preview, flowers, 76, 120)
    paste_feet(rua_preview, cat.crop((0, 0, 16, 16)), 46, 134)
    paste_feet(rua_preview, bench, 186, 136)
    scale(rua_preview, 3).save(preview / "rua.png")
    print("arte gerada em", ASSETS)


if __name__ == "__main__":
    main()
