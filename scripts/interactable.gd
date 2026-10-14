class_name Interactable
extends Area2D

## Área que responde à tecla de interação.
## O texto vem de Story.DIALOGUES, pela chave dialogue_id.

@export var dialogue_id := ""

func _ready() -> void:
	collision_layer = 4
	collision_mask = 0
	monitoring = false
	monitorable = true

func interact() -> void:
	var lines := Story.lines_for(dialogue_id)
	if lines.is_empty():
		return
	Game.start_dialogue(lines)

func prompt_position() -> Vector2:
	return global_position + Vector2(0, -2)
