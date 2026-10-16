extends Interactable

@export var piece_id := "academia"
@export var needs_exercise := true

func _ready() -> void:
	super()
	if Game.has_heart(piece_id) or (needs_exercise and not Game.exercised):
		visible = false
		collision_layer = 0

func interact() -> void:
	if Game.has_heart(piece_id):
		return
	Game.collect_heart(piece_id)
	visible = false
	collision_layer = 0
