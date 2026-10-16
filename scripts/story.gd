class_name Story
extends RefCounted

## Falas do jogo.
##
## Pessoa: "Nome: fala". Cada item é uma fala e avança com E, Z, Enter ou Espaço.
## A cama, a placa e o cartão não são gente.

const DIALOGUES := {
	"cama": [
		"A cama está arrumada.",
		"Alguém que dormiu aqui arrumou antes de sair.",
	],
	"celular": [
		"Alex: Meu bem vc nao vem treinar?",
	],
	"alex_alongou": [
		"Alex: amor, eu já alonguei.",
	],
	"pai": [
		"Pai: No Quixote, o amor às vezes voa.",
		"Pai: Às vezes anda. Ninguém o alcança, nem lhe escapa.",
	],
	"mae": [
		"Mãe: Bom dia filhota!",
		"Mãe: Deus te abençoe.",
	],
	"cachorra": [
		"Pretinha: Me leva pra passear humana!",
	],
	"alex1": [
		"Alex: Vamos lá! Ta leve!",
	],
	"alex2": [
		"Alex: Isso! Mais uma, campeã!",
	],
	"alex3": [
		"Alex: Leve demais! Quase voando!",
	],
	"alex4": [
		"Alex: Você consegue! Eu acredito!",
	],
	"henrique": [
		"Henrique: Amiga, tu nem sabe!",
		"Henrique: Entra no Creta. Eu vou junto.",
	],
	"placa": [
		"Só os melhores chegam aqui.",
	],
	"ernani": [
		"Ernani: Amiga, vc é a aluna mais elegante da universidade!",
	],
	"breno": [
		"Breno: Amanda, começa a escrever!!!!",
	],
	"presente": [
		"Feliz aniversário.",
		"Eu quis te dar um lugar pequeno para começar este dia.",
	],
	"cafe": [
		"Amanda: Café passado.",
	],
	"cafe_pronto": [
		"Amanda: O café já está pronto.",
	],
	"paciente_espera": [
		"Paciente: Sem café eu não começo.",
	],
	"paciente": [
		"Paciente: A vida está um peso.",
		"Paciente: Nada do que eu faço serve.",
		"Amanda: O desejo é o desejo do Outro.",
	],
	"paciente_fim": [
		"Paciente: Vou pensar nisso.",
	],
	"eli_espera": [
		"Eli: Atende ele. Eu te espero.",
	],
	"eli": [
		"Eli: Um biscoito de um passeio comum na Grécia.",
		"Eli: E o terceiro pedaço do coração.",
	],
	"eli_depois": [
		"Eli: O biscoito ainda está quentinho.",
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
