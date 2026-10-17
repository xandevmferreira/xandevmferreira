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
		"Agora vá pra academia.",
	],
	"creta": [
		"A academia é a porta ao lado.",
		"Agora vá pra lá.",
	],
	"academia_tempo": [
		"A academia é do lado da casa.",
	],
	"academia_atraso": [
		"Chegou. O cronômetro já tinha virado piada.",
	],
	"exercicio_fim": [
		"Acabou o exercício.",
		"Agora volte pra casa.",
	],
	"coracao": [
		"Um quarto do coração.",
	],
	"alex_alongou": [
		"Alex: amor, eu já alonguei.",
	],
	"pai": [
		"Pai: O amor às vezes voa.",
		"Pai: Às vezes anda. Ninguém lhe escapa.",
		"Pai: Os filhos são como flechas.",
		"Pai: Lançamos sem saber o destino.",
		"Pai: A vida passa. O amor fica.",
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
	"puf": [
		"PUF. Roupa preta e joias douradas.",
		"Agora vá pra rua.",
	],
	"armario_pronta": [
		"Pronta pra UFPA.",
		"O Henrique espera na rua.",
	],
	"missao_ufpa": [
		"Agora vá pra casa se arrumar.",
		"Hoje tem aula na UFPA.",
	],
	"creta_ufpa": [
		"Siga a placa da UFPA.",
	],
	"ufpa_cedo": [
		"A UFPA fica pra lá. O Henrique ainda não veio.",
	],
	"ufpa_chegada": [
		"Fale com Ernani e o Breno.",
		"Depois siga a placa CLINICA.",
	],
	"coracao2": [
		"Outro quarto do coração.",
	],
	"henrique": [
		"Henrique: Amiga, tu nem sabe!",
		"Henrique: Entre no Creta. Placa UFPA.",
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
		"A sala particular é pra dentro.",
		"A Eli fica fora, no sofá.",
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
		"Agora fale com a Eli, lá fora.",
	],
	"paciente_fim": [
		"Paciente: Vou pensar nisso.",
	],
	"eli_espera": [
		"Eli: Atende na sala particular.",
		"Eli: Eu espero aqui fora.",
	],
	"eli": [
		"Eli: Um biscoito de um passeio comum na Grécia.",
		"Eli: E o terceiro pedaço do coração.",
		"Agora volte pra casa.",
		"Mande mensagem pro Alexandre.",
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
