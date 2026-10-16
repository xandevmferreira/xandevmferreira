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
		"A cama está arrumada.",
		"Alguém que dormiu aqui arrumou antes de sair.",
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
	"pai": [
		"Pai: No Quixote, o amor às vezes voa.",
		"Às vezes anda. Ninguém o alcança, nem lhe escapa.",
	],
	"mae": [
		"Bom dia filhota! Deus te abençoe.",
	],
	"cachorra": [
		"Me leva pra passear humana!",
	],
	"alex1": [
		"Vamos lá! Ta leve!",
	],
	"alex2": [
		"Isso! Mais uma, campeã!",
	],
	"alex3": [
		"Leve demais! Quase voando!",
	],
	"alex4": [
		"Você consegue! Eu acredito!",
	],
	"armario": [
		"O guarda-roupa da Amanda.",
	],
	"armario_pronta": [
		"A roupa preta já está no corpo.",
	],
	"puf": [
		"PUF.",
		"Roupa preta e joias douradas. Pronta pra UFPA.",
	],
	"missao_ufpa": [
		"Hora de ir pra casa e se arrumar.",
		"Hoje tem aula na UFPA.",
	],
	"henrique": [
		"Amiga, tu nem sabe!",
		"Entra no Creta. Eu vou junto.",
	],
	"creta_ufpa": [
		"Henrique sobe junto. A UFPA é seguindo a rua.",
	],
	"ufpa_cedo": [
		"A UFPA fica pra lá. O Henrique ainda não veio.",
	],
	"ufpa_chegada": [
		"A UFPA. O rio passa atrás da Pedagogia.",
	],
	"placa": [
		"Só os melhores chegam aqui.",
	],
	"ernani": [
		"Amiga, vc é a aluna mais elegante da universidade!",
	],
	"breno": [
		"Amanda, começa a escrever!!!!",
	],
	"coracao2": [
		"Outro quarto do coração.",
		"Já são dois. O resto ainda está na cidade.",
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
