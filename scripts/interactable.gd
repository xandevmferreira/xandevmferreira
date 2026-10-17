class_name Interactable
extends Area2D

## Área que responde à tecla de interação.
## O texto vem de Story.DIALOGUES, pela chave dialogue_id.

@export var dialogue_id := ""
@export var one_by_one := false
@export var sayings: PackedStringArray = PackedStringArray()

var _step := 0

func _ready() -> void:
	collision_layer = 4
	collision_mask = 0
	monitoring = false
	monitorable = true

func interact() -> void:
	if not sayings.is_empty():
		var saying := sayings[_step % sayings.size()]
		_step += 1
		Game.start_dialogue(Story.lines_for(saying))
		return
	var lines := Story.lines_for(dialogue_id)
	if lines.is_empty():
		return
	if one_by_one:
		var line := lines[_step % lines.size()]
		_step += 1
		Game.start_dialogue(PackedStringArray([line]))
		return
	Game.start_dialogue(lines)

func prompt_position() -> Vector2:
	return global_position + Vector2(0, -2)
