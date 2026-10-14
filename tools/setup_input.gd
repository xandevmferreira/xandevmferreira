extends SceneTree

## Grava as ações de teclado no formato desta versão do Godot.

func _init() -> void:
	_bind("move_up", [KEY_W, KEY_UP])
	_bind("move_down", [KEY_S, KEY_DOWN])
	_bind("move_left", [KEY_A, KEY_LEFT])
	_bind("move_right", [KEY_D, KEY_RIGHT])
	_bind("interact", [KEY_E, KEY_Z, KEY_ENTER, KEY_KP_ENTER, KEY_SPACE])
	var err := ProjectSettings.save()
	if err != OK:
		push_error("Não foi possível salvar project.godot (%s)" % err)
		quit(1)
		return
	quit()

func _bind(action: String, keys: Array) -> void:
	var events: Array[InputEvent] = []
	for key: Key in keys:
		var event := InputEventKey.new()
		event.physical_keycode = key
		events.append(event)
	ProjectSettings.set_setting("input/%s" % action, {
		"deadzone": 0.5,
		"events": events,
	})
