extends Interactable

## Café, paciente e a Eli, nesta ordem.

@export_enum("cafe", "paciente", "eli") var role := "cafe"

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
				Game.start_dialogue(Story.lines_for("paciente"))
		"eli":
			if not Game.session_done:
				Game.start_dialogue(Story.lines_for("eli_espera"))
			elif Game.has_heart("eli"):
				Game.start_dialogue(Story.lines_for("eli_depois"))
			else:
				Game.collect_heart("eli")
				Game.start_dialogue(Story.lines_for("eli"))
