extends Sprite2D

## Alinha a base do desenho com a posição do objeto, para o y-sort usar os pés.

@export var foot_inset := 1.0

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	centered = true
	if texture:
		offset = Vector2(0, -texture.get_height() * 0.5 + foot_inset)
