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
		"O celular acende.",
		"Alex: Meu bem vc nao vem treinar?",
	],
	"creta": [
		"A academia fica logo ali.",
	],
	"academia_tempo": [
		"Chegou a tempo.",
	],
	"academia_atraso": [
		"Chegou. O cronômetro já tinha virado piada.",
	],
	"exercicio_fim": [
		"Alex: Isso. O coração é seu.",
	],
	"coracao": [
		"Um quarto do coração.",
	],
	"alex_alongou": [
		"Alex: amor, eu já alonguei.",
	],
	"pai_amor": [
		"Pai: O amor às vezes voa e às vezes anda. Ninguém lhe escapa.",
	],
	"pai_filhos": [
		"Pai: Os filhos são como flechas. Lançamos sem saber o destino.",
	],
	"pai_vida": [
		"Pai: A vida passa. O amor fica.",
	],
	"mae": [
		"Mãe: Bom dia filhota! Deus te abençoe.",
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
	"puf": [
		"PUF. Preto e ouro.",
		"O Henrique está lá fora.",
	],
	"armario_pronta": [
		"Já estou pronta.",
	],
	"missao_ufpa": [
		"Hoje a aula é na UFPA.",
	],
	"creta_ufpa": [
		"A UFPA é seguindo a placa.",
	],
	"ufpa_cedo": [
		"O Henrique ainda não chegou.",
	],
	"ufpa_chegada": [
		"A UFPA. O rio passa atrás da Pedagogia.",
	],
	"coracao2": [
		"Outro quarto do coração.",
	],
	"henrique": [
		"Henrique: Amiga, tu nem sabe!",
		"Henrique: Vem, eu vou com você.",
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
	"clinica_chegada": [
		"O consultório está em silêncio.",
	],
	"cafe": [
		"Amanda: Um café pra mim.",
	],
	"cafe_pronto": [
		"Amanda: Já tomei o meu café.",
	],
	"paciente_espera": [
		"Amanda: Primeiro eu tomo um café.",
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
		"Eli: Eu te espero aqui.",
	],
	"eli": [
		"Eli: Um biscoito de um passeio comum na Grécia.",
		"Eli: E este pedaço do coração.",
		"Eli: O Alexandre te espera em casa.",
	],
	"gato": [
		"Miau.",
	],
	"alexandre": [
		"Amanda: Amor, to muito cansada.",
		"Amanda: Vamos dormir juntos?",
	],
	"final": [
		"Amanda, todos torcemos por ti e te amamos incondicionalmente. Estaremos sempre aqui por você. Feliz aniversário, Deus te abençoe sempre e que você nunca pare a busca pela felicidade. Te amamos!",
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
