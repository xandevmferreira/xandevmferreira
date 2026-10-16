extends Interactable

func _ready() -> void:
	super()
	if not Game.exercised:
		visible = false
		collision_layer = 0

func interact() -> void:
	if Game.heart_pieces > 0:
		return
	Game.collect_heart()
	visible = false
	collision_layer = 0
	Game.start_dialogue(Story.lines_for("coracao"))
