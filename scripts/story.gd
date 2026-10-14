class_name Story
extends RefCounted

## Textos do protótipo.
##
## Cada chave é um objeto do mapa. A lista é a sequência de falas:
## cada item aparece sozinho e avança com E, Z, Enter ou Espaço.
##
## A última fala de "presente" é o cartão no banco.
## Troque por o que você quiser dizer.

const DIALOGUES := {
	"cama": [
		"O lençol está dobrado de um jeito que você não costuma deixar.",
		"Alguém passou por aqui antes de você acordar.",
	],
	"bolo": [
		"Um bolo pequeno espera na mesa, com a vela ainda apagada.",
		"O parabéns ficou guardado para daqui a pouco.",
	],
	"planta": [
		"Alguém regou a planta. As folhas estão firmes, viradas para a luz.",
	],
	"quadro": [
		"Um desenho feito à mão: duas pessoas, um gato e esta casa.",
		"Embaixo, com letra miúda: nossa casa.",
	],
	"flores": [
		"Flores recém-cortadas, ao lado da porta.",
		"São as que você sempre para para olhar.",
	],
	"gato": [
		"Um gato listrado pisca devagar, como quem guarda um segredo.",
		"Ele olha para o banco e mia baixinho.",
	],
	"presente": [
		"Uma caixinha amarrada com fita está em cima do banco.",
		"Você abre o cartão.",
		"Feliz aniversário.",
		"Eu quis te dar um lugar pequeno para começar este dia.",
	],
}


static func lines_for(id: String) -> PackedStringArray:
	if not DIALOGUES.has(id):
		push_warning("Diálogo não encontrado: %s" % id)
		return PackedStringArray()
	var result := PackedStringArray()
	for line: String in DIALOGUES[id]:
		result.append(line)
	return result
