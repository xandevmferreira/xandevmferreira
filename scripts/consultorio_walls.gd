class_name ConsultorioWalls
extends RefCounted

## Paredes do consultório. Sai de tools/generate_art.py.

const SIZE := Vector2i(400, 240)

const RECTS: Array[Rect2] = [
	Rect2(0, 0, 176, 8),
	Rect2(216, 0, 184, 8),
	Rect2(0, 8, 8, 224),
	Rect2(392, 8, 8, 224),
	Rect2(0, 232, 400, 8),
	Rect2(8, 104, 168, 8),
	Rect2(216, 104, 176, 8),
	Rect2(32, 36, 92, 28),
	Rect2(16, 124, 108, 44),
	Rect2(228, 136, 132, 36),
	Rect2(312, 188, 36, 24),
]
