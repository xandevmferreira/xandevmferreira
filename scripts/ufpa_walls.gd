class_name UfpaWalls
extends RefCounted

## Muros da UFPA. Sai de tools/generate_art.py.

const SIZE := Vector2i(400, 200)

const RECTS: Array[Rect2] = [
	Rect2(0, 0, 400, 8),
	Rect2(0, 8, 8, 184),
	Rect2(392, 8, 8, 184),
	Rect2(0, 192, 400, 8),
	Rect2(8, 8, 384, 28),
	Rect2(120, 52, 168, 8),
	Rect2(120, 60, 8, 44),
	Rect2(280, 60, 8, 44),
	Rect2(120, 104, 52, 8),
	Rect2(204, 104, 84, 8),
	Rect2(28, 120, 18, 16),
	Rect2(340, 70, 18, 16),
	Rect2(48, 150, 16, 16),
	Rect2(214, 118, 84, 16),
	Rect2(160, 64, 28, 8),
]
