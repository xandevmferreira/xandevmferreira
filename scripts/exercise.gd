extends Interactable

var _count := 0

func interact() -> void:
	if Game.exercised:
		Game.start_dialogue(Story.lines_for("exercicio_fim"))
		return
	_count += 1
	if _count < 3:
		Game.start_dialogue(PackedStringArray(["Série %d de 3. Mais uma." % _count]))
		return
	Game.exercised = true
	var heart := get_parent().get_node_or_null("Heart")
	if heart:
		heart.visible = true
		heart.collision_layer = 4
	Game.start_dialogue(Story.lines_for("exercicio_fim"))
