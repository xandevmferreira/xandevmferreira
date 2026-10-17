extends Node2D

## Monta as paredes do mapa e coloca a personagem no ponto de entrada.
## As áreas de fala e os objetos ficam na cena, para poder mover no editor.

@export var map_id := "casa"

const ACADEMIA_WALLS: Array[Rect2] = [
	Rect2(0, 0, 240, 8),
	Rect2(0, 8, 8, 144),
	Rect2(232, 8, 8, 144),
	Rect2(0, 152, 108, 8),
	Rect2(140, 152, 100, 8),
	Rect2(28, 36, 28, 52),
	Rect2(150, 28, 36, 22),
]

func _ready() -> void:
	_build_walls()
	if map_id == "casa":
		_follow_player(CasaWalls.SIZE)
	elif map_id == "rua":
		_follow_player(CidadeWalls.SIZE)
	elif map_id == "ufpa":
		_follow_player(UfpaWalls.SIZE)
	elif map_id == "clinica":
		_follow_player(ConsultorioWalls.SIZE)
	Game.on_map_ready($Props/Player, $Spawns)

func _follow_player(map_size: Vector2i) -> void:
	var cam := $Camera2D as Camera2D
	cam.limit_left = 0
	cam.limit_top = 0
	cam.limit_right = map_size.x
	cam.limit_bottom = map_size.y
	cam.position_smoothing_enabled = false
	cam.offset = Vector2(0, -8)
	cam.reparent($Props/Player)
	cam.position = Vector2.ZERO
	cam.make_current()

func _build_walls() -> void:
	var rects: Array[Rect2] = CasaWalls.RECTS
	if map_id == "rua":
		rects = CidadeWalls.RECTS
	elif map_id == "academia":
		rects = ACADEMIA_WALLS
	elif map_id == "ufpa":
		rects = UfpaWalls.RECTS
	elif map_id == "clinica":
		rects = ConsultorioWalls.RECTS
	var body := $Walls as StaticBody2D
	for rect: Rect2 in rects:
		var shape := RectangleShape2D.new()
		shape.size = rect.size
		var collider := CollisionShape2D.new()
		collider.shape = shape
		collider.position = rect.position + rect.size * 0.5
		body.add_child(collider)
