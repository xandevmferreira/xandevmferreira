extends Interactable

var _count := 0

func interact() -> void:
	if Game.exercised:
		if not Game.has_heart("academia"):
			Game.grant_heart("academia", "exercicio_fim")
		return
	_count += 1
	if _count < 3:
		Game.start_dialogue(PackedStringArray(["Alex: Mais uma!"]))
		return
	Game.exercised = true
	Game.grant_heart("academia", "exercicio_fim")
