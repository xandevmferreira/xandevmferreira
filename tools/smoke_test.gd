extends SceneTree

## Confere movimento, diálogo e a ida da casa para a rua.

var _errors: Array[String] = []
var _game

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	_game = root.get_node("Game")
	change_scene_to_file("res://scenes/casa/casa.tscn")
	for _i in 8:
		await process_frame

	for _i in 30:
		await process_frame
	var casa := current_scene
	if casa == null or casa.name != "Casa":
		_fail("cena inicial %s" % casa)
		return
	var player := casa.get_node("Props/Player") as CharacterBody2D
	if player.global_position.distance_to(Vector2(100, 156)) > 1.5:
		_fail("spawn da casa em %s" % player.global_position)

	var origin := player.global_position
	await create_timer(0.35).timeout
	await _shot(casa, "/tmp/art-preview/godot_casa.png")
	Input.action_press("move_right")
	for _i in 20:
		await physics_frame
	Input.action_release("move_right")
	if player.global_position.x < origin.x + 10.0:
		_fail("não andou para a direita: %s" % player.global_position)

	Input.action_press("move_up")
	for _i in 12:
		await physics_frame
	Input.action_release("move_up")
	if player.global_position.y > origin.y - 4.0:
		_fail("não andou para cima: %s" % player.global_position)

	player.global_position = Vector2(44, 150)
	player.facing = Vector2.UP
	for _i in 3:
		await physics_frame
	_press_interact()
	for _frame in 3:
		await process_frame
	if not _game.dialogue_open:
		_fail("a cama não respondeu à tecla")
	else:
		var guard := 0
		while _game.dialogue_open and guard < 8:
			_press_interact()
			await process_frame
			guard += 1
		if _game.dialogue_open:
			_fail("a fala da cama não terminou")

	casa.get_node("Talkers/Cozinha").interact()
	await process_frame
	_press_interact()
	for _frame in 2:
		await process_frame
	await _shot(casa, "/tmp/art-preview/godot_dialogo.png")
	if not _game.dialogue_open:
		_fail("o diálogo não abriu")
	else:
		var presses := 0
		while _game.dialogue_open and presses < 8:
			_press_interact()
			await process_frame
			presses += 1
		if _game.dialogue_open:
			_fail("o diálogo não fechou depois de %s toques" % presses)
		elif presses < 3:
			_fail("o diálogo fechou cedo demais (%s toques)" % presses)

	_check_lines()

	await create_timer(0.55).timeout
	player.global_position = Vector2(400, 132)
	player.facing = Vector2.UP
	for _i in 3:
		await physics_frame
	await _shot(casa, "/tmp/art-preview/godot_cozinha.png")
	player.global_position = Vector2(408, 274)
	await physics_frame
	Input.action_press("move_down")
	var reached := false
	var started := Time.get_ticks_msec()
	while Time.get_ticks_msec() - started < 2000:
		await process_frame
		if current_scene != null and current_scene.name == "Rua":
			reached = true
			break
	Input.action_release("move_down")
	if not reached:
		_fail("não entrou na rua. cena=%s pos=%s" % [current_scene, player.global_position])
	else:
		await create_timer(0.45).timeout
		var rua := current_scene
		var arrived := rua.get_node("Props/Player") as Node2D
		if arrived.global_position.distance_to(Vector2(120, 126)) > 2.0:
			_fail("spawn da rua em %s" % arrived.global_position)
		await _shot(rua, "/tmp/art-preview/godot_rua.png")
		await create_timer(0.5).timeout
		arrived.global_position = Vector2(120, 118)
		await physics_frame
		Input.action_press("move_up")
		var back := false
		var started_back := Time.get_ticks_msec()
		while Time.get_ticks_msec() - started_back < 2000:
			await process_frame
			if current_scene != null and current_scene.name == "Casa":
				back = true
				break
		Input.action_release("move_up")
		if not back:
			_fail("não voltou para a casa")
		else:
			for _i in 20:
				await process_frame
			var home := current_scene.get_node("Props/Player") as Node2D
			if home.global_position.distance_to(Vector2(408, 252)) > 2.0:
				_fail("spawn de volta em %s" % home.global_position)

	await create_timer(0.4).timeout
	await _shot(current_scene, "/tmp/art-preview/godot_volta.png")
	if _errors.is_empty():
		print("SMOKE_OK")
		quit(0)
	else:
		for message in _errors:
			print("SMOKE_FAIL: ", message)
		quit(1)

func _press_interact() -> void:
	var event := InputEventAction.new()
	event.action = "interact"
	event.pressed = true
	Input.parse_input_event(event)

func _check_lines() -> void:
	var font := load("res://assets/fonts/CozetteVector.ttf") as Font
	for id: String in Story.DIALOGUES:
		for line: String in Story.DIALOGUES[id]:
			var size := font.get_multiline_string_size(line, HORIZONTAL_ALIGNMENT_LEFT, 206.0, 13)
			if size.y > 30.0:
				_fail("fala longa (%s, %s px): %s" % [id, size.y, line])

func _shot(node: Node, path: String) -> void:
	if node == null or DisplayServer.get_name() == "headless":
		return
	await process_frame
	var image := root.get_viewport().get_texture().get_image()
	if image != null and image.get_width() > 0:
		image.save_png(path)

func _fail(message: String) -> void:
	_errors.append(message)
