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
		"Sua cama, no quarto da Amanda.",
		"O lençol está do jeito que você deixou.",
	],
	"piano": [
		"O piano sem cauda, encostado na sala.",
	],
	"santos": [
		"Os santos católicos, na estante.",
	],
	"sofa": [
		"O sofá da sala, de frente para a TV.",
	],
	"cozinha": [
		"A cozinha. As lajotas da parede são marrom claro.",
		"A bancada americana separa a mesa do fogão.",
	],
	"maquina": [
		"A máquina de lavar, na lavanderia.",
	],
	"planta": [
		"As plantas, num canto da sala.",
	],
	"flores": [
		"Flores recém-cortadas, ao lado da porta.",
		"São as que você sempre para para olhar.",
	],
	"gato": [
		"Um gato listrado pisca devagar, como quem guarda um segredo.",
		"Ele olha para o banco e mia baixinho.",
	],
	"celular": [
		"O celular acende.",
		"ALEX: Meu bem vc nao vem treinar?",
	],
	"creta": [
		"Você entra no Creta preto. A academia é logo ali.",
	],
	"academia_tempo": [
		"A academia é do lado da casa. O Alex nem acredita.",
	],
	"academia_atraso": [
		"Chegou. O cronômetro já tinha virado piada.",
	],
	"alex_alongou": [
		"ALEX: amor, eu já alonguei.",
	],
	"exercicio_fim": [
		"Acabou o exercício.",
		"Um pedaço do coração apareceu na academia.",
	],
	"coracao": [
		"Um quarto do coração.",
		"É o primeiro pedaço. O resto ainda está na cidade.",
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
