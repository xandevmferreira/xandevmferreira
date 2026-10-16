extends CharacterBody2D

## Creta preto. Parado é um objeto; depois do E, a personagem dirige.

const SPEED := 110.0

var driving := false

func _ready() -> void:
	motion_mode = MOTION_MODE_FLOATING
	collision_layer = 1
	collision_mask = 1

func enter() -> void:
	if driving:
		return
	Game.queue_drive(self)

func _physics_process(_delta: float) -> void:
	if not driving or Game.blocks_player():
		velocity = Vector2.ZERO
		move_and_slide()
		return
	var axis := _axis()
	velocity = axis * SPEED
	if axis.x != 0.0:
		$Sprite.flip_h = axis.x < 0.0
	move_and_slide()
	if global_position.x < 368.0:
		return
	if Game.henrique_joined:
		Game.go_university()
	else:
		global_position.x = 360.0
		velocity = Vector2.ZERO
		Game.remind_gate()

func _unhandled_input(event: InputEvent) -> void:
	if not driving or Game.blocks_player():
		return
	if event.is_action_pressed(&"interact"):
		driving = false
		velocity = Vector2.ZERO
		Game.end_drive()
		get_viewport().set_input_as_handled()

func _axis() -> Vector2:
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
		y = 0.0
	return Vector2(x, y)
