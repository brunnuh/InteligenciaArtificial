import os
from time import sleep

from puzzle import Puzzle

def init():
    puzzle = Puzzle()
    #puzzle.estadoAtual()
    print("\n\n")
    tipoDeJogo = -1 # 0 - jogador, 1 - IA

    while tipoDeJogo not in [0, 1]:
        try:
            tipoDeJogo = int(input("Escolha o quem vai jogar:\n0 - jogador\n1 - Inteligencia\n>>>>>>>"))
        except:
            print("erro, tente novamente")
            continue

    puzzle.estadoAtual()
    if tipoDeJogo == 1:
        while puzzle.venceu():
            puzzle.buscaGulosa()
            sleep(0.06)
            os.system('cls')

            puzzle.estadoAtual()
            print(f'movimentos: {puzzle.movimentos}')

    else:
        while puzzle.venceu():
            try:
                movimento = int(input("Movimentar para? "))
            except:
                continue
            if movimento in [8, 6, 2, 4]:
                puzzle.mover(movimento)
                os.system('cls')

                puzzle.estadoAtual()
    puzzle.estadoAtual()
    print(f"\nmovimentos feitos: {puzzle.movimentos}")
    if puzzle.venceu() == False:
        print("""\n_   _ _____ _   _ _____  _____ _   _\n| | | |  ___| \ | /  __ \|  ___| | | |\n| | | | |__ |  \| | /  \/| |__ | | | |\n| | | |  __|| . ` | |    |  __|| | | |\n\ \_/ / |___| |\  | \__/\| |___| |_| |\n \___/\____/\_| \_/\____/\____/ \___/\n""")
    else:
        print("""______  _____ ______ ______  _____  _   _\n| ___ \|  ___|| ___ \|  _  \|  ___|| | | |\n| |_/ /| |__  | |_/ /| | | || |__  | | | |\n|  __/ |  __| |    / | | | ||  __| | | | |\n| |    | |___ | |\ \ | |/ / | |___ | |_| |\n\_|    \____/ \_| \_||___/  \____/  \___/""")

if __name__ == '__main__':
    init()
