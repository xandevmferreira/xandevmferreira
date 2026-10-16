extends Interactable

## O guarda-roupa troca a roupa quando já existe a missão da UFPA.

func interact() -> void:
	if Game.mission_ufpa and not Game.dressed:
		Game.transform_outfit()
