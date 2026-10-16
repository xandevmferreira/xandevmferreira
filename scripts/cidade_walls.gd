class_name CidadeWalls
extends RefCounted

## Muros do condomínio. Sai de tools/generate_art.py.

const SIZE := Vector2i(400, 180)

const RECTS: Array[Rect2] = [
	Rect2(0, 0, 400, 8),
	Rect2(0, 8, 8, 164),
	Rect2(392, 8, 8, 164),
	Rect2(0, 172, 400, 8),
	Rect2(16, 16, 96, 28),
	Rect2(16, 44, 28, 8),
	Rect2(80, 44, 32, 8),
	Rect2(112, 16, 136, 16),
	Rect2(248, 16, 128, 28),
	Rect2(248, 44, 48, 8),
	Rect2(328, 44, 48, 8),
	Rect2(376, 16, 16, 20),
]
