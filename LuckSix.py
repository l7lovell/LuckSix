import random

numeros_sorteados_historico = set()
numeros_bloqueados = {}


def fazer_sorteio():
    global numeros_sorteados_historico, numeros_bloqueados
    numeros_sorteio = gerar_numeros_sorteio()

    while tuple(numeros_sorteio) in numeros_sorteados_historico or any(n in numeros_bloqueados.get(n, []) for n in numeros_sorteio):
        numeros_sorteio = gerar_numeros_sorteio()

    numeros_sorteados_historico.add(tuple(numeros_sorteio))

    # Verifica se o histórico de números sorteados tem mais de 30 elementos e remove o mais antigo
    if len(numeros_sorteados_historico) > 30:
        numeros_sorteados_historico.remove(min(numeros_sorteados_historico))

    # Atualiza o histórico de sorteios para cada número
    for num in numeros_sorteio:
        numeros_bloqueados.setdefault(num, []).append(tuple(numeros_sorteio))

        # Mantém apenas as últimas 5 rodadas no histórico
        if len(numeros_bloqueados[num]) > 5:
            numeros_bloqueados[num].pop(0)

    return numeros_sorteio


def gerar_numeros_sorteio():
    numeros_sorteio = random.sample(range(1, 61), 6)
    return numeros_sorteio


def fazer_aposta():
    # Essa função pede ao jogador para digitar 6 números separados por vírgula
    # e retorna uma lista contendo os números escolhidos
    while True:
        try:
            numeros = input("Digite 6 números (separados por vírgula): ")
            numeros = numeros.replace(" ", "").split(",")
            aposta_jogador = [int(num) for num in numeros]

            if len(aposta_jogador) != 6:
                raise ValueError("Digite exatamente 6 números.")

            if not all(1 <= num <= 60 for num in aposta_jogador):
                raise ValueError("Os números devem estar entre 1 e 60.")

            return aposta_jogador

        except ValueError as e:
            print(f"Erro: {e}")


def verificar_acertos(aposta_jogador, numeros_sorteio):
    acertos = set(aposta_jogador).intersection(set(numeros_sorteio))
    return acertos


def calcular_premio_final(acertos):
    num_acertos = len(acertos)
    premio = 0
    valor_premio_maximo = 500000
    valor_premio_cinco_numeros = 400000
    valor_premio_quatro_numeros = 300000
    valor_premio_tres_numeros = 200000
    valor_premio_dois_numeros = 100000

    if num_acertos == 6:
        premio = valor_premio_maximo
    elif num_acertos == 5:
        premio = valor_premio_cinco_numeros
    elif num_acertos == 4:
        premio = valor_premio_quatro_numeros
    elif num_acertos == 3:
        premio = valor_premio_tres_numeros
    elif num_acertos == 2:
        premio = valor_premio_dois_numeros

    return premio


# Loop do jogo
while True:
    aposta_jogador = fazer_aposta()
    print("Sua aposta:", aposta_jogador)

    numeros_sorteio = fazer_sorteio()
    print("Números sorteados:", numeros_sorteio)

    acertos = verificar_acertos(aposta_jogador, numeros_sorteio)
    print("Acertos:", acertos)

    premio = calcular_premio_final(acertos)
    print("Seu prêmio é: R$", premio)

    continuar_jogando = input("Deseja continuar jogando? (S/N): ")
    if continuar_jogando.upper() != "S":
        break