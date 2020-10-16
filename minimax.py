

def winner_is(tabuleiro):
	sum3 = tabuleiro[0] + tabuleiro[4] + tabuleiro[8]
	sum4 = tabuleiro[2] + tabuleiro[4] + tabuleiro[6]
	for x in range(3):
		sum1 = tabuleiro[x*3] + tabuleiro[x*3+1] + tabuleiro[x*3+2]
		sum2 = tabuleiro[x] + tabuleiro[x+3] + tabuleiro[x+6]
		if sum1 == 3 or sum2 == 3 or sum3 == 3 or sum4 == 3:
			return 1

		if sum1 == -3 or sum2 == -3 or sum3 == -3 or sum4 == -3:
			return -1
	return 0


def minimax(tabuleiro, profundidade, player, e):
	x = input("parada")
	if profundidade <= 0:
		print("Zero")
		return 0
	for x in range(9):
		if tabuleiro[x] == 0:
			tabuleiro[x] = player
			win = winner_is(tabuleiro)
			if abs(win) == 1:
				print("vencedor",player)
				return player
			z = min(minimax(tabuleiro, profundidade - 1, player * -1, e))
			return z

tabuleiro = [0]*9

print(tabuleiro)

acabou = False

def valor (x):
	if x == 0:
		return 0
	return x + valor(x-1)

print(valor(10))


while not acabou:
	print(tabuleiro)
	entrada = int(input("entre a posicao no tabuleiro, 0 sair"))
	if entrada == 0:
		acabou = True
	else:
		entrada -= 1
		tabuleiro[entrada] = 1
		if (winner_is(tabuleiro)) == 1:
			acabou = True
			print("venceu")
		else:
			print("vencedor", minimax(tabuleiro, 9, -1, -1))
		

