extends Interactable

## O guarda-roupa troca a roupa quando já existe a missão da UFPA.

func interact() -> void:
	if Game.dressed:
		Game.start_dialogue(Story.lines_for("armario_pronta"))
	elif Game.mission_ufpa:
		Game.transform_outfit()
	else:
		Game.start_dialogue(Story.lines_for("armario"))
