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
	if player.global_position.distance_to(Vector2(70, 158)) > 1.5:
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

	player.global_position = Vector2(48, 150)
	player.facing = Vector2.LEFT
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

	casa.get_node("Talkers/Mae").interact()
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

	casa.get_node("Talkers/Sofa").interact()
	await process_frame
	if not await _seen("voa"):
		_fail("o Pai não recitou")
	elif _dialogue_line().contains("flechas"):
		_fail("o Pai recitou tudo de uma vez")
	await _close_talk()
	casa.get_node("Talkers/Sofa").interact()
	await process_frame
	if not await _seen("anda"):
		_fail("o Pai repetiu o primeiro ditado")
	await _close_talk()

	await create_timer(0.55).timeout
	player.global_position = Vector2(430, 148)
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
		if arrived.global_position.distance_to(Vector2(62, 86)) > 2.0:
			_fail("spawn da rua em %s" % arrived.global_position)
		await _shot(rua, "/tmp/art-preview/godot_rua.png")
		await create_timer(0.5).timeout
		arrived.global_position = Vector2(62, 78)
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
			if home.global_position.distance_to(Vector2(408, 268)) > 2.0:
				_fail("spawn de volta em %s" % home.global_position)

	await create_timer(0.4).timeout
	await _shot(current_scene, "/tmp/art-preview/godot_volta.png")

	if current_scene != null and current_scene.name == "Casa":
		_game.house_seconds = 59.2
		await create_timer(1.1).timeout
		if not _game.phone_ringing:
			_fail("o celular não tocou")
		else:
			_press_interact()
			for _frame in 4:
				await process_frame
		if not _game.dialogue_open:
			_fail("a mensagem do Alex não abriu")
		else:
			var saw_alex := false
			var guard := 0
			while _game.dialogue_open and guard < 8:
				if _dialogue_line().contains("Meu bem vc nao vem treinar?"):
					saw_alex = true
					await _shot(current_scene, "/tmp/art-preview/godot_celular.png")
				_press_interact()
				await process_frame
				guard += 1
			if not saw_alex:
				_fail("a mensagem do Alex não apareceu")
			if _game.gym_left < 100.0:
				_fail("o cronômetro não abriu: %s" % _game.gym_left)
			else:
				await _shot(current_scene, "/tmp/art-preview/godot_cronometro.png")

	await _drive_to_gym()

	if _errors.is_empty():
		print("SMOKE_OK")
		quit(0)
	else:
		for message in _errors:
			print("SMOKE_FAIL: ", message)
		quit(1)

func _drive_to_gym() -> void:
	if not _errors.is_empty():
		return
	_game.request_scene("res://scenes/rua/rua.tscn", "from_casa")
	var street := false
	var started_street := Time.get_ticks_msec()
	while Time.get_ticks_msec() - started_street < 2000:
		await process_frame
		if current_scene != null and current_scene.name == "Rua":
			street = true
			break
	if not street:
		_fail("não voltou à cidade para o Creta")
		return
	await create_timer(0.45).timeout
	var rua := current_scene
	var walker := rua.get_node("Props/Player") as CharacterBody2D
	walker.global_position = Vector2(100, 96)
	walker.facing = Vector2.DOWN
	for _i in 4:
		await physics_frame
	_press_interact()
	for _frame in 4:
		await process_frame
	if not _game.dialogue_open:
		_fail("o Creta não abriu")
		return
	var guard := 0
	while _game.dialogue_open and guard < 6:
		_press_interact()
		await process_frame
		guard += 1
	if not _game.is_driving():
		_fail("não entrou no Creta")
		return
	var car := rua.get_node("Props/Creta") as CharacterBody2D
	var car_x := car.global_position.x
	Input.action_press("move_right")
	for _i in 30:
		await physics_frame
	Input.action_release("move_right")
	if car.global_position.x < car_x + 20.0:
		_fail("o Creta não andou: %s" % car.global_position)
		return
	await _shot(rua, "/tmp/art-preview/godot_creta.png")
	car.global_position = Vector2(312, 108)
	await physics_frame
	_press_interact()
	for _frame in 4:
		await process_frame
	if _game.is_driving():
		_fail("não saiu do Creta")
		return
	walker = rua.get_node("Props/Player") as CharacterBody2D
	if not walker.visible:
		_fail("a personagem não desceu do carro")
		return
	walker.global_position = Vector2(312, 78)
	walker.facing = Vector2.UP
	await physics_frame
	Input.action_press("move_up")
	var gym := false
	var started_gym := Time.get_ticks_msec()
	while Time.get_ticks_msec() - started_gym < 2500:
		await process_frame
		if current_scene != null and current_scene.name == "Academia":
			gym = true
			break
	Input.action_release("move_up")
	if not gym:
		_fail("não entrou na academia. cena=%s pos=%s" % [current_scene, walker.global_position])
		return
	await create_timer(0.55).timeout
	var close_guard := 0
	while _game.dialogue_open and close_guard < 8:
		_press_interact()
		await process_frame
		close_guard += 1
	await _shot(current_scene, "/tmp/art-preview/godot_academia.png")
	var trainee := current_scene.get_node("Props/Player") as CharacterBody2D
	for serie in 3:
		trainee.global_position = Vector2(70, 100)
		trainee.facing = Vector2.LEFT
		for _i in 4:
			await physics_frame
		_press_interact()
		for _frame in 4:
			await process_frame
		var serie_guard := 0
		while _game.dialogue_open and serie_guard < 8:
			_press_interact()
			await process_frame
			serie_guard += 1
	if not _game.exercised:
		_fail("o exercício não terminou")
		return
	if trainee.get_node_or_null("CoracaoGanho") == null or _game.heart_pieces != 1:
		_fail("o coração não ficou na cabeça: %s" % _game.heart_pieces)
		return
	await _shot(current_scene, "/tmp/art-preview/godot_coracao.png")
	trainee.global_position = Vector2(124, 130)
	trainee.facing = Vector2.DOWN
	await physics_frame
	Input.action_press("move_down")
	var left_gym := false
	var started_leave := Time.get_ticks_msec()
	while Time.get_ticks_msec() - started_leave < 2500:
		await process_frame
		if current_scene != null and current_scene.name == "Rua":
			left_gym = true
			break
	Input.action_release("move_down")
	if not left_gym:
		_fail("não saiu da academia")
		return
	await create_timer(0.55).timeout
	if not _game.mission_ufpa:
		_fail("a missão da UFPA não abriu")
		return
	await _close_talk()
	_game.request_scene("res://scenes/casa/casa.tscn", "default")
	if not await _await_scene("Casa"):
		_fail("não voltou para se arrumar")
		return
	await create_timer(0.45).timeout
	current_scene.get_node("Talkers/Armario").interact()
	await process_frame
	if not _game.dressed:
		_fail("o guarda-roupa não trocou a roupa")
		return
	await _shot(current_scene, "/tmp/art-preview/godot_puf.png")
	await _close_talk()
	_game.request_scene("res://scenes/rua/rua.tscn", "from_casa")
	if not await _await_scene("Rua"):
		_fail("não saiu para encontrar o Henrique")
		return
	await create_timer(0.45).timeout
	var friend := current_scene.get_node("Props/Henrique")
	if not friend.visible:
		_fail("o Henrique não apareceu")
		return
	var parked := current_scene.get_node("Props/Creta") as Node2D
	if parked.global_position.x < 250.0:
		_fail("o Creta não ficou onde foi deixado: %s" % parked.global_position)
		return
	var gato := current_scene.get_node_or_null("Props/GatoPreto") as Node2D
	if gato == null or gato.global_position.x > 110.0 or gato.global_position.y > 96.0:
		_fail("o gato preto não está na frente da casa")
		return
	gato.get_node("Talk").interact()
	await process_frame
	if not await _seen("Miau"):
		_fail("o gato preto não miou")
		return
	await _close_talk()
	friend.interact()
	await process_frame
	if not _game.henrique_joined or not await _seen("tu nem sabe"):
		_fail("o Henrique não falou")
		return
	await _close_talk()
	_game.request_scene("res://scenes/universidade/universidade.tscn", "default")
	if not await _await_scene("Universidade"):
		_fail("não chegou na UFPA")
		return
	await create_timer(0.55).timeout
	await _close_talk()
	await _shot(current_scene, "/tmp/art-preview/godot_ufpa.png")
	var student := current_scene.get_node("Props/Player") as CharacterBody2D
	student.global_position = Vector2(176, 102)
	student.facing = Vector2.UP
	for _i in 4:
		await physics_frame
	_press_interact()
	for _frame in 4:
		await process_frame
	if not await _seen("mais elegante"):
		_fail("o professor Ernani não falou")
		return
	await _close_talk()
	student.global_position = Vector2(320, 166)
	student.facing = Vector2.UP
	for _i in 4:
		await physics_frame
	_press_interact()
	for _frame in 4:
		await process_frame
	if not await _seen("começa a escrever"):
		_fail("o professor Breno não falou")
		return
	await _close_talk()
	var porta = current_scene.get_node("Door")
	if not String(porta.target_scene).contains("consultorio"):
		_fail("a saída da UFPA não vai ao consultório")
		return
	if _game.heart_pieces != 2 or student.get_node_or_null("CoracaoGanho") == null:
		_fail("os professores não deixaram o coração: %s" % _game.heart_pieces)
		return
	_game.request_scene("res://scenes/consultorio/consultorio.tscn", "default")
	if not await _await_scene("Consultorio"):
		_fail("não chegou no consultório")
		return
	await create_timer(0.45).timeout
	await _shot(current_scene, "/tmp/art-preview/godot_consultorio.png")
	await _close_talk()
	var paciente = current_scene.get_node("Props/Paciente")
	paciente.interact()
	await process_frame
	if not await _seen("tomo um café"):
		_fail("o café não ficou com a Amanda")
		return
	await _close_talk()
	current_scene.get_node("Cafe").interact()
	await process_frame
	if not await _seen("café pra mim"):
		_fail("o café não saiu")
		return
	await _close_talk()
	if not _game.coffee_ready:
		_fail("o café não ficou pronto")
		return
	var na_sala := current_scene.get_node("Props/Player") as CharacterBody2D
	na_sala.global_position = Vector2(196, 200)
	await physics_frame
	paciente.interact()
	await process_frame
	if not paciente.deitado:
		_fail("o paciente não deitou no divã")
		return
	if not await _seen("desejo do Outro"):
		_fail("a frase do Lacan não apareceu")
		return
	await _shot(current_scene, "/tmp/art-preview/godot_paciente.png")
	await _close_talk()
	if not _game.session_done:
		_fail("a sessão não terminou")
		return
	na_sala.global_position = Vector2(180, 70)
	await physics_frame
	current_scene.get_node("Props/Eli").interact()
	await process_frame
	if not await _seen("passeio comum"):
		_fail("a Eli não entregou o biscoito")
		return
	await _shot(current_scene, "/tmp/art-preview/godot_eli.png")
	await _close_talk()
	if _game.heart_pieces != 3:
		_fail("não recebeu o 3/4 do coração: %s" % _game.heart_pieces)
		return
	if not _game.alexandre_pending:
		_fail("a volta pra casa não abriu")
		return
	_game.request_scene("res://scenes/casa/casa.tscn", "from_clinica")
	if not await _await_scene("Casa"):
		_fail("não voltou pra casa depois do consultório")
		return
	await create_timer(0.55).timeout
	if not _game.dialogue_open:
		_fail("a mensagem pro Alexandre não apareceu")
		return
	if not await _seen("cansada"):
		_fail("a mensagem pro Alexandre não abriu")
		return
	await _shot(current_scene, "/tmp/art-preview/godot_alexandre.png")
	await _close_talk()
	if not _game.alexandre_sent:
		_fail("a mensagem pro Alexandre não foi enviada")
		return
	var espera := Time.get_ticks_msec()
	while Time.get_ticks_msec() - espera < 8000 and String(_game.finale_caption).is_empty():
		await process_frame
	if _game.heart_pieces != 4:
		_fail("o coração não fechou: %s" % _game.heart_pieces)
		return
	var tela := _game.get_node_or_null("FinalHeart/TelaFinal") as Sprite2D
	if tela == null or tela.texture == null or tela.scale.x < 2.0:
		_fail("o coração completo não cresceu")
		return
	var metade := tela.texture.get_height() * tela.scale.y * 0.5
	if tela.position.y - metade < 0.0 or tela.position.y + metade > 84.0:
		_fail("o coração completo ficou cortado")
		return
	var mensagem := "Amanda, todos torcemos por ti e te amamos incondicionalmente. Estaremos sempre aqui por você. Feliz aniversário, Deus te abençoe sempre e que você nunca pare a busca pela felicidade. Te amamos!"
	if String(_game.finale_caption) != mensagem:
		_fail("a mensagem da família não é o texto inteiro: %s" % _game.finale_caption)
		return
	var leitura := Time.get_ticks_msec()
	while Time.get_ticks_msec() - leitura < 12000 and not _dialogue_line().contains("Te amamos!"):
		await process_frame
	if not _dialogue_line().contains("Te amamos!"):
		_fail("a mensagem inteira não apareceu no balão")
		return
	await _shot(current_scene, "/tmp/art-preview/godot_final.png")

func _seen(snippet: String) -> bool:
	var guard := 0
	while guard < 12:
		if _label_has(snippet):
			return true
		if not _game.dialogue_open:
			return false
		_press_interact()
		await process_frame
		guard += 1
	return _label_has(snippet)

func _close_talk() -> void:
	var guard := 0
	while _game.dialogue_open and guard < 12:
		_press_interact()
		await process_frame
		guard += 1

func _await_scene(scene_name: String) -> bool:
	var started := Time.get_ticks_msec()
	while Time.get_ticks_msec() - started < 2500:
		await process_frame
		if current_scene != null and current_scene.name == scene_name:
			return true
	return false

func _label_has(snippet: String) -> bool:
	return _dialogue_line().contains(snippet)

func _dialogue_line() -> String:
	for node in _game.find_children("*", "Label", true, false):
		if node.get_parent() is NinePatchRect:
			return String(node.text)
	return ""

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
			if id != "final" and size.y > 30.0:
				_fail("fala longa (%s, %s px): %s" % [id, size.y, line])
			var baixa := line.to_lower()
			if baixa.contains("quixote") or baixa.contains("como diz"):
				_fail("fala ainda anuncia o livro: %s" % line)

func _shot(node: Node, path: String) -> void:
	if node == null or DisplayServer.get_name() == "headless":
		return
	await process_frame
	var image := root.get_viewport().get_texture().get_image()
	if image != null and image.get_width() > 0:
		image.save_png(path)

func _fail(message: String) -> void:
	_errors.append(message)
