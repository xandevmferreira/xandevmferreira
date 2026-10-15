extends Node2D

## Monta as paredes do mapa e coloca a personagem no ponto de entrada.
## As áreas de fala e os objetos ficam na cena, para poder mover no editor.

@export var map_id := "casa"

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
	if map_id == "casa":
		_follow_player()
	Game.on_map_ready($Props/Player, $Spawns)

func _follow_player() -> void:
	var cam := $Camera2D as Camera2D
	cam.limit_left = 0
	cam.limit_top = 0
	cam.limit_right = CasaWalls.SIZE.x
	cam.limit_bottom = CasaWalls.SIZE.y
	cam.position_smoothing_enabled = false
	cam.offset = Vector2(0, -8)
	cam.reparent($Props/Player)
	cam.position = Vector2.ZERO
	cam.make_current()

func _build_walls() -> void:
	var rects: Array[Rect2] = CasaWalls.RECTS if map_id == "casa" else RUA_WALLS
	var body := $Walls as StaticBody2D
	for rect: Rect2 in rects:
		var shape := RectangleShape2D.new()
		shape.size = rect.size
		var collider := CollisionShape2D.new()
		collider.shape = shape
		collider.position = rect.position + rect.size * 0.5
		body.add_child(collider)
