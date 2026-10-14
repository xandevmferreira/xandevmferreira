extends CharacterBody2D

## Personagem em visão de cima. Anda em quatro direções e fala com o que está à frente.

const SPEED := 48.0
const FRAME := Vector2i(16, 24)

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var interact_area: Area2D = $InteractArea

var facing := Vector2.DOWN
var _last_axis := "y"

func _ready() -> void:
	add_to_group("player")
	motion_mode = MOTION_MODE_FLOATING
	collision_layer = 2
	collision_mask = 1
	_build_frames()
	sprite.play(&"idle_down")

func _physics_process(_delta: float) -> void:
	if Game.blocks_player():
		velocity = Vector2.ZERO
		_animate(false)
		move_and_slide()
		Game.set_prompt(Vector2.ZERO, false)
		return

	var axis := _read_axis()
	if axis != Vector2.ZERO:
		facing = axis
		velocity = axis * SPEED
	else:
		velocity = Vector2.ZERO

	interact_area.position = facing * 12.0
	_animate(axis != Vector2.ZERO)
	move_and_slide()
	_update_prompt()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"move_left") or event.is_action_pressed(&"move_right"):
		_last_axis = "x"
	elif event.is_action_pressed(&"move_up") or event.is_action_pressed(&"move_down"):
		_last_axis = "y"

	if event.is_action_pressed(&"interact") and not Game.blocks_player():
		var target := _nearest_interactable()
		if target:
			target.interact()
			get_viewport().set_input_as_handled()

func _read_axis() -> Vector2:
	var x := 0.0
	var y := 0.0
	if Input.is_action_pressed(&"move_left"):
		x -= 1.0
	if Input.is_action_pressed(&"move_right"):
		x += 1.0
	if Input.is_action_pressed(&"move_up"):
		y -= 1.0
	if Input.is_action_pressed(&"move_down"):
		y += 1.0
	if x != 0.0 and y != 0.0:
		if _last_axis == "x":
			y = 0.0
		else:
			x = 0.0
	return Vector2(x, y)

func _animate(moving: bool) -> void:
	var direction := "down"
	if facing.x != 0.0:
		direction = "side"
		sprite.flip_h = facing.x < 0.0
	else:
		sprite.flip_h = false
		direction = "up" if facing.y < 0.0 else "down"
	var anim := ("%s_%s" % ["walk" if moving else "idle", direction]) as StringName
	if sprite.animation != anim:
		sprite.play(anim)

func _nearest_interactable() -> Interactable:
	var best: Interactable = null
	var best_distance := INF
	for area: Area2D in interact_area.get_overlapping_areas():
		if area is Interactable:
			var distance := global_position.distance_squared_to(area.global_position)
			if distance < best_distance:
				best = area
				best_distance = distance
	return best

func _update_prompt() -> void:
	var target := _nearest_interactable()
	if target:
		Game.set_prompt(target.prompt_position(), true)
	else:
		Game.set_prompt(Vector2.ZERO, false)

func _build_frames() -> void:
	var texture: Texture2D = load("res://assets/sprites/player.png")
	var frames := SpriteFrames.new()
	if frames.has_animation(&"default"):
		frames.remove_animation(&"default")
	var rows := {"down": 0, "side": 1, "up": 2}
	for direction: String in rows:
		var row: int = rows[direction]
		var idle := "idle_%s" % direction
		var walk := "walk_%s" % direction
		frames.add_animation(idle)
		frames.set_animation_loop(idle, true)
		frames.set_animation_speed(idle, 2.0)
		frames.add_animation(walk)
		frames.set_animation_loop(walk, true)
		frames.set_animation_speed(walk, 8.0)
		for column: int in [0, 1]:
			frames.add_frame(idle, _frame(texture, column, row))
		for column: int in [2, 3, 4, 5]:
			frames.add_frame(walk, _frame(texture, column, row))
	sprite.sprite_frames = frames
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sprite.offset = Vector2(0, -10)

func _frame(texture: Texture2D, column: int, row: int) -> AtlasTexture:
	var atlas := AtlasTexture.new()
	atlas.atlas = texture
	atlas.region = Rect2(column * FRAME.x, row * FRAME.y, FRAME.x, FRAME.y)
	return atlas
