extends Interactable

func interact() -> void:
	var car := get_parent()
	if car.has_method("enter"):
		car.enter()
