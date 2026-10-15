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

func _ready() -> void:
	_build_ui()

func blocks_player() -> bool:
	return dialogue_open or transitioning

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
	var marker := spawns.get_node_or_null(pending_spawn) as Node2D
	if marker == null:
		marker = spawns.get_node_or_null("default") as Node2D
	if marker:
		player.global_position = marker.global_position
	pending_spawn = "default"
	transitioning = true
	var tween := create_tween()
	tween.tween_property(_fade, "color:a", 0.0, 0.28)
	tween.tween_callback(func() -> void:
		transitioning = false
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

	var show_prompt := _prompt_wanted and not blocks_player()
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
	_layer.move_child(_fade, -1)

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
