class_name Door
extends Area2D

## Troca de mapa ao entrar na área. O jogador surge no marcador target_spawn.

@export_file("*.tscn") var target_scene := ""
@export var target_spawn := "default"
@export var arm_delay := 0.4

var _armed := false

func _ready() -> void:
	collision_layer = 0
	collision_mask = 2
	monitorable = false
	monitoring = false
	body_entered.connect(_on_body_entered)
	_arm()

func _arm() -> void:
	await get_tree().create_timer(arm_delay).timeout
	if not is_inside_tree():
		return
	monitoring = true
	await get_tree().physics_frame
	if not is_inside_tree():
		return
	if get_overlapping_bodies().is_empty():
		_armed = true
	else:
		body_exited.connect(_on_cleared, CONNECT_ONE_SHOT)

func _on_cleared(_body: Node) -> void:
	_armed = true

func _on_body_entered(body: Node) -> void:
	if not _armed or Game.blocks_player():
		return
	if not body.is_in_group("player"):
		return
	_armed = false
	Game.request_scene(target_scene, target_spawn)
