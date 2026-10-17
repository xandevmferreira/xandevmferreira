extends Sprite2D

## Folha horizontal de quadros do mesmo tamanho. Usada no gato.

@export var frame_count := 2
@export var fps := 1.5
@export var foot_inset := 1.0

var _time := 0.0

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	centered = true
	if texture == null or frame_count < 1:
		return
	var frame_h := texture.get_height()
	offset = Vector2(0, -frame_h * 0.5 + foot_inset)
	region_enabled = true
	_show_frame(0)

func _process(delta: float) -> void:
	if texture == null or frame_count <= 1:
		return
	_time += delta
	_show_frame(int(_time * fps) % frame_count)

func _show_frame(index: int) -> void:
	var frame_w := texture.get_width() / frame_count
	var frame_h := texture.get_height()
	region_rect = Rect2(index * frame_w, 0, frame_w, frame_h)
