extends Node

## Diálogo, transição entre mapas e a dica de teclas.
## O texto em si mora em scripts/story.gd.

const FADE_COLOR := Color("3a242c")
const TEXT_COLOR := Color("3a242c")
const CHAR_DELAY := 0.032
const TEXT_WIDTH := 206.0

var pending_spawn := "default"
var dialogue_open := false
var transitioning := false

var _lines: PackedStringArray = PackedStringArray()
var _index := 0
var _shown := 0
var _typing := false
var _char_clock := 0.0
var _full := ""

var _layer: CanvasLayer
var _fade: ColorRect
var _box: NinePatchRect
var _label: Label
var _arrow: TextureRect
var _prompt: TextureRect
var _hint: Control
var _prompt_anchor := Vector2.ZERO
var _prompt_wanted := false
var _hint_hidden := false

var house_seconds := 0.0
var phone_ringing := false
var phone_read := false
var gym_left := -1.0
var gym_late := false
var gym_arrived := false
var exercised := false
var heart_pieces := 0
var driving := false
var mission_ufpa := false
var dressed := false
var henrique_joined := false
var ufpa_arrived := false
var coffee_ready := false
var session_done := false
var _hearts := {}
var _spawn_used := ""
var _car: Node2D
var _after_close := ""
var _status: Label
var _phone_chip: Control

func _ready() -> void:
	_build_ui()

func blocks_player() -> bool:
	return dialogue_open or transitioning

func is_driving() -> bool:
	return driving

func start_dialogue(lines: PackedStringArray) -> void:
	if lines.is_empty() or dialogue_open or transitioning:
		return
	dialogue_open = true
	_lines = lines
	_index = 0
	_hint_hidden = true
	_hint.visible = false
	_prompt.visible = false
	_box.visible = true
	_show_current_line()

func request_scene(path: String, spawn_name: String) -> void:
	if transitioning or path.is_empty():
		return
	transitioning = true
	pending_spawn = spawn_name
	_prompt_wanted = false
	_prompt.visible = false
	var tween := create_tween()
	tween.tween_property(_fade, "color:a", 1.0, 0.22)
	tween.tween_callback(func() -> void:
		get_tree().change_scene_to_file(path)
	)

func on_map_ready(player: Node2D, spawns: Node2D) -> void:
	_spawn_used = pending_spawn
	var marker := spawns.get_node_or_null(pending_spawn) as Node2D
	if marker == null:
		marker = spawns.get_node_or_null("default") as Node2D
	if marker:
		player.global_position = marker.global_position
	pending_spawn = "default"
	var body := player as CharacterBody2D
	if body:
		body.visible = true
		body.collision_layer = 2
		body.set_physics_process(true)
		if dressed and body.has_method("apply_outfit"):
			body.apply_outfit("elegante")
	driving = false
	transitioning = true
	var tween := create_tween()
	tween.tween_property(_fade, "color:a", 0.0, 0.28)
	tween.tween_callback(func() -> void:
		transitioning = false
		var scene := get_tree().current_scene
		if scene == null:
			return
		if scene.name == "Academia":
			arrive_gym()
		elif scene.name == "Rua" and _spawn_used == "from_academia" and not mission_ufpa:
			mission_ufpa = true
		elif scene.name == "Universidade" and not ufpa_arrived:
			ufpa_arrived = true
	)

func set_prompt(anchor: Vector2, show: bool) -> void:
	_prompt_anchor = anchor
	_prompt_wanted = show

func _unhandled_input(event: InputEvent) -> void:
	if not dialogue_open:
		return
	if event.is_action_pressed(&"interact"):
		_advance()
		get_viewport().set_input_as_handled()

func _process(delta: float) -> void:
	if _typing:
		_char_clock += delta
		while _typing and _char_clock >= CHAR_DELAY:
			_char_clock -= CHAR_DELAY
			_shown += 1
			_label.text = _full.substr(0, _shown)
			if _shown >= _full.length():
				_typing = false
				_arrow.visible = true
	elif dialogue_open:
		_arrow.visible = int(Time.get_ticks_msec() / 360.0) % 2 == 0

	var scene := get_tree().current_scene
	if scene != null and scene.name == "Casa" and not phone_read and not phone_ringing and not dialogue_open:
		house_seconds += delta
		if house_seconds >= 60.0:
			phone_ringing = true
	if gym_left > 0.0 and not gym_arrived:
		gym_left = maxf(gym_left - delta, 0.0)
		if gym_left == 0.0:
			gym_late = true
			if not dialogue_open and not transitioning:
				start_dialogue(Story.lines_for("alex_alongou"))
	_refresh_status()

	var show_prompt := _prompt_wanted and not blocks_player() and not driving
	_prompt.visible = show_prompt
	if show_prompt:
		var bob := -1.0 if int(Time.get_ticks_msec() / 280.0) % 2 == 0 else 0.0
		_prompt.position = _screen_point(_prompt_anchor) + Vector2(-6, -18 + bob)

func _screen_point(world: Vector2) -> Vector2:
	var cam := get_viewport().get_camera_2d()
	if cam == null:
		return world
	var view := get_viewport().get_visible_rect().size
	var half := view * 0.5
	var center := cam.global_position + cam.offset
	if cam.limit_right > cam.limit_left:
		var min_x := float(cam.limit_left) + half.x
		var max_x := float(cam.limit_right) - half.x
		center.x = (min_x + max_x) * 0.5 if max_x < min_x else clampf(center.x, min_x, max_x)
	if cam.limit_bottom > cam.limit_top:
		var min_y := float(cam.limit_top) + half.y
		var max_y := float(cam.limit_bottom) - half.y
		center.y = (min_y + max_y) * 0.5 if max_y < min_y else clampf(center.y, min_y, max_y)
	return (world - center) * cam.zoom + half

func _show_current_line() -> void:
	_full = _lines[_index]
	_shown = 0
	_char_clock = 0.0
	_typing = true
	_label.text = ""
	_arrow.visible = false

func _advance() -> void:
	if _typing:
		_shown = _full.length()
		_label.text = _full
		_typing = false
		_arrow.visible = true
		return
	_index += 1
	if _index >= _lines.size():
		_close_dialogue()
	else:
		_show_current_line()

func _close_dialogue() -> void:
	dialogue_open = false
	_typing = false
	_box.visible = false
	_arrow.visible = false
	var follow := _after_close
	_after_close = ""
	if follow == "timer":
		gym_left = 180.0
	elif follow == "enter_car":
		_start_drive()

func read_phone() -> void:
	if not phone_ringing or dialogue_open or transitioning:
		return
	phone_ringing = false
	phone_read = true
	_after_close = "timer"
	start_dialogue(Story.lines_for("celular"))

func queue_drive(car: Node2D) -> void:
	if driving or dialogue_open or transitioning:
		return
	_car = car
	_start_drive()

func end_drive() -> void:
	if not driving or _car == null:
		return
	var player := get_tree().get_first_node_in_group("player") as CharacterBody2D
	if player == null:
		driving = false
		return
	player.global_position = _car.global_position + Vector2(0, -30)
	player.visible = true
	player.collision_layer = 2
	player.set_physics_process(true)
	var cam := _car.get_node_or_null("Camera2D") as Camera2D
	if cam:
		cam.reparent(player)
		cam.position = Vector2.ZERO
	driving = false

func arrive_gym() -> void:
	if gym_arrived:
		return
	gym_arrived = true
	gym_left = 0.0

func has_heart(piece_id: String) -> bool:
	return _hearts.has(piece_id)

func collect_heart(piece_id: String = "academia") -> void:
	_hearts[piece_id] = true
	heart_pieces = _hearts.size()

func transform_outfit() -> void:
	if dressed:
		return
	dressed = true
	var player := get_tree().get_first_node_in_group("player")
	if player and player.has_method("apply_outfit"):
		player.apply_outfit("elegante")
	_show_puf()

func remind_gate() -> void:
	pass

func go_university() -> void:
	if transitioning or not henrique_joined:
		return
	driving = false
	request_scene("res://scenes/universidade/universidade.tscn", "default")

func _start_drive() -> void:
	if _car == null:
		return
	var player := get_tree().get_first_node_in_group("player") as CharacterBody2D
	if player == null:
		return
	player.visible = false
	player.collision_layer = 0
	player.velocity = Vector2.ZERO
	player.set_physics_process(false)
	var cam := player.get_node_or_null("Camera2D") as Camera2D
	if cam:
		cam.reparent(_car)
		cam.position = Vector2.ZERO
	driving = true
	_car.set("driving", true)

func _refresh_status() -> void:
	if _phone_chip:
		_phone_chip.visible = phone_ringing and not blocks_player()
	if _status == null:
		return
	if gym_left > 0.0:
		var total := int(ceil(gym_left))
		_status.text = "Treino %d:%02d" % [total / 60, total % 60]
		_status.visible = true
	elif heart_pieces > 0:
		_status.text = "Coração %d/4" % heart_pieces
		_status.visible = true
	elif mission_ufpa and not dressed:
		_status.text = "UFPA: casa"
		_status.visible = true
	elif dressed and not henrique_joined:
		_status.text = "Henrique"
		_status.visible = true
	else:
		_status.visible = false

func _build_ui() -> void:
	_layer = CanvasLayer.new()
	_layer.layer = 20
	add_child(_layer)

	var font := load("res://assets/fonts/CozetteVector.ttf") as FontFile
	font.antialiasing = TextServer.FONT_ANTIALIASING_NONE
	font.hinting = TextServer.HINTING_NONE
	font.subpixel_positioning = TextServer.SUBPIXEL_POSITIONING_DISABLED

	_fade = ColorRect.new()
	_fade.color = Color(FADE_COLOR, 1.0)
	_fade.position = Vector2.ZERO
	_fade.size = Vector2(240, 160)
	_fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_layer.add_child(_fade)

	_hint = _make_hint(font)
	_layer.add_child(_hint)

	_box = NinePatchRect.new()
	_box.texture = load("res://assets/ui/dialogue_frame.png")
	_box.patch_margin_left = 6
	_box.patch_margin_top = 6
	_box.patch_margin_right = 6
	_box.patch_margin_bottom = 6
	_box.position = Vector2(6, 108)
	_box.size = Vector2(228, 48)
	_box.visible = false
	_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_layer.add_child(_box)

	_label = Label.new()
	_label.position = Vector2(10, 6)
	_label.size = Vector2(TEXT_WIDTH, 36)
	_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	_label.add_theme_font_override(&"font", font)
	_label.add_theme_font_size_override(&"font_size", 13)
	_label.add_theme_color_override(&"font_color", TEXT_COLOR)
	_label.add_theme_constant_override(&"line_spacing", -1)
	_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_box.add_child(_label)

	_arrow = TextureRect.new()
	_arrow.texture = load("res://assets/ui/arrow.png")
	_arrow.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_arrow.position = Vector2(208, 34)
	_arrow.size = Vector2(7, 5)
	_arrow.visible = false
	_arrow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_box.add_child(_arrow)

	_prompt = TextureRect.new()
	_prompt.texture = load("res://assets/ui/key_e.png")
	_prompt.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_prompt.size = Vector2(13, 13)
	_prompt.visible = false
	_prompt.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_layer.add_child(_prompt)

	_phone_chip = _make_chip(font, "E  celular", Vector2(4, 18), Vector2(78, 14))
	_phone_chip.visible = false
	_layer.add_child(_phone_chip)

	_status = Label.new()
	_status.position = Vector2(150, 18)
	_status.size = Vector2(86, 14)
	_status.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_status.add_theme_font_override(&"font", font)
	_status.add_theme_font_size_override(&"font_size", 13)
	_status.add_theme_color_override(&"font_color", Color("fff6ea"))
	_status.add_theme_color_override(&"font_outline_color", FADE_COLOR)
	_status.add_theme_constant_override(&"outline_size", 3)
	_status.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_status.visible = false
	_layer.add_child(_status)

	_layer.move_child(_fade, -1)

func _show_puf() -> void:
	var flash := ColorRect.new()
	flash.color = Color(1, 1, 1, 0.0)
	flash.position = Vector2.ZERO
	flash.size = Vector2(240, 160)
	flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_layer.add_child(flash)
	var font := load("res://assets/fonts/CozetteVector.ttf") as Font
	var label := Label.new()
	label.text = "PUF"
	label.position = Vector2(80, 58)
	label.size = Vector2(80, 28)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_font_override(&"font", font)
	label.add_theme_font_size_override(&"font_size", 28)
	label.add_theme_color_override(&"font_color", Color("3a242c"))
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_layer.add_child(label)
	_layer.move_child(_fade, -1)
	var tween := create_tween()
	tween.tween_property(flash, "color:a", 0.9, 0.08)
	tween.tween_property(flash, "color:a", 0.0, 0.28)
	tween.parallel().tween_property(label, "modulate:a", 0.0, 0.4)
	tween.tween_callback(func() -> void:
		if is_instance_valid(flash):
			flash.queue_free()
		if is_instance_valid(label):
			label.queue_free()
	)

func _make_chip(font: Font, text: String, pos: Vector2, chip_size: Vector2) -> Control:
	var chip := ColorRect.new()
	chip.position = pos
	chip.size = chip_size
	chip.color = Color(FADE_COLOR, 0.72)
	chip.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var label := Label.new()
	label.text = text
	label.position = Vector2(4, 0)
	label.size = chip_size - Vector2(6, 0)
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_override(&"font", font)
	label.add_theme_font_size_override(&"font_size", 13)
	label.add_theme_color_override(&"font_color", Color("fff6ea"))
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	chip.add_child(label)
	return chip

func _make_hint(font: Font) -> Control:
	var chip := ColorRect.new()
	chip.position = Vector2(4, 3)
	chip.size = Vector2(170, 14)
	chip.color = Color(FADE_COLOR, 0.72)
	chip.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var label := Label.new()
	label.text = "Setas/WASD andam  ·  E fala"
	label.position = Vector2(4, 0)
	label.size = Vector2(162, 14)
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_override(&"font", font)
	label.add_theme_font_size_override(&"font_size", 13)
	label.add_theme_color_override(&"font_color", Color("fff6ea"))
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	chip.add_child(label)
	return chip
