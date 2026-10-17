extends Interactable

## Café da Amanda, paciente no divã e a Eli fora da sala.

const DIVAN_POS := Vector2(270, 156)

@export_enum("cafe", "paciente", "eli") var role := "cafe"

var deitado := false

func _ready() -> void:
	super()
	if role == "paciente" and Game.session_done:
		_deitar()

func interact() -> void:
	match role:
		"cafe":
			if Game.coffee_ready:
				Game.start_dialogue(Story.lines_for("cafe_pronto"))
			else:
				Game.coffee_ready = true
				Game.start_dialogue(Story.lines_for("cafe"))
		"paciente":
			if not Game.coffee_ready:
				Game.start_dialogue(Story.lines_for("paciente_espera"))
			elif Game.session_done:
				Game.start_dialogue(Story.lines_for("paciente_fim"))
			else:
				Game.session_done = true
				_deitar()
				Game.start_dialogue(Story.lines_for("paciente"))
		"eli":
			if not Game.session_done:
				Game.start_dialogue(Story.lines_for("eli_espera"))
			elif Game.has_heart("eli"):
				Game.start_dialogue(Story.lines_for("eli_depois"))
			else:
				Game.grant_heart("eli")
				Game.alexandre_pending = true
				Game.start_dialogue(Story.lines_for("eli"))

func _deitar() -> void:
	deitado = true
	var em_pe := get_node_or_null("Sprite")
	var no_diva := get_node_or_null("Deitado")
	if em_pe:
		em_pe.visible = false
	if no_diva:
		no_diva.visible = true
	global_position = DIVAN_POS
