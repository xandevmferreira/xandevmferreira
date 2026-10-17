extends Interactable

## O guarda-roupa troca a roupa quando já existe a missão da UFPA.

func interact() -> void:
	if Game.dressed:
		if not Game.henrique_joined:
			Game.start_dialogue(Story.lines_for("armario_pronta"))
		return
	if Game.mission_ufpa:
		Game.transform_outfit()
