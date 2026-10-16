class_name ConsultorioWalls
extends RefCounted

## Paredes do consultório. Sai de tools/generate_art.py.

const SIZE := Vector2i(320, 180)

const RECTS: Array[Rect2] = [
	Rect2(0, 0, 320, 8),
	Rect2(0, 8, 8, 164),
	Rect2(312, 8, 8, 164),
	Rect2(0, 172, 136, 8),
	Rect2(184, 172, 136, 8),
	Rect2(44, 54, 96, 34),
	Rect2(214, 22, 90, 46),
	Rect2(18, 22, 22, 24),
	Rect2(156, 68, 28, 26),
]
