extends Interactable

## Pessoa do mapa. Pode repetir várias falas, uma por conversa.

@export var cycle: PackedStringArray = PackedStringArray()
@export var show_if_dressed := false
@export var hide_after_join := false

var _step := 0

func _ready() -> void:
	super()
	if show_if_dressed and (not Game.dressed or Game.henrique_joined):
		visible = false
		collision_layer = 0

func interact() -> void:
	if hide_after_join:
		Game.henrique_joined = true
		visible = false
		collision_layer = 0
	var id := dialogue_id
	if not cycle.is_empty():
		id = cycle[_step % cycle.size()]
		_step += 1
	var lines := Story.lines_for(id)
	if lines.is_empty():
		return
	Game.start_dialogue(lines)
