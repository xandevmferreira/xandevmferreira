extends Node2D

## Monta as paredes do mapa e coloca a personagem no ponto de entrada.
## As áreas de fala e os objetos ficam na cena, para poder mover no editor.

@export var map_id := "casa"

const CASA_WALLS: Array[Rect2] = [
	Rect2(0, 0, 240, 86),
	Rect2(0, 86, 8, 64),
	Rect2(232, 86, 8, 64),
	Rect2(0, 150, 100, 10),
	Rect2(140, 150, 100, 10),
]

const RUA_WALLS: Array[Rect2] = [
	Rect2(68, 28, 104, 66),
	Rect2(68, 94, 40, 10),
	Rect2(132, 94, 40, 10),
	Rect2(0, 96, 6, 64),
	Rect2(234, 96, 6, 64),
	Rect2(0, 152, 240, 8),
	Rect2(208, 108, 26, 22),
]

func _ready() -> void:
	_build_walls()
	Game.on_map_ready($Props/Player, $Spawns)

func _build_walls() -> void:
	var rects: Array[Rect2] = CASA_WALLS if map_id == "casa" else RUA_WALLS
	var body := $Walls as StaticBody2D
	for rect: Rect2 in rects:
		var shape := RectangleShape2D.new()
		shape.size = rect.size
		var collider := CollisionShape2D.new()
		collider.shape = shape
		collider.position = rect.position + rect.size * 0.5
		body.add_child(collider)
