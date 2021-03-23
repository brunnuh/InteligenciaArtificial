import os
from random import Random, seed
from copy import deepcopy

seed(1)

class Puzzle:

    def __init__(self):
        self.comandos = ["cima", "direita", "baixo", "esquerda"]
        self.puzzle = list()
        self.rdn = Random()
        self.x = 0
        self.movimentos = 0
        self.mf = 0
        self.y = 0
        self.ultimoMovimento = None
        self.movimentosFeitos = []
        #self.provisorio()
        self.montar()





    def provisorio(self):
        self.puzzle = [["+", "_", "_", "_", "+"],["|", 1, 2, 3, "|"], ["|", 4, " ", 6, "|"], ["|", 5, 8, 7, "|"], ["+", "_", "_", "_", "+"]]

    def montar(self):
        conjunto = [1, 2, 3, 4, 5, 6, 7, 8, " "]

        for x in range(0, 5):
            newLinha = list()
            for y in range(0, 5):
                if y == 0 or y == 4:
                    if y == 0 and x == 0 or y == 0 and x == 4 or y == 4 and x == 0 or y == 4 and x == 4:
                        newLinha.append("+")
                    else:
                        newLinha.append("|")
                elif y > 0 and x > 0 and y < 4 and x < 4:
                    escolhido = self.rdn.choice(conjunto) # numero aleatorio da lista
                    conjunto.remove(escolhido) # remover da lista
                    if(escolhido == " "):
                        self.x = x
                        self.y = y
                    newLinha.append(escolhido) # adicionar a nova linha
                else:
                    newLinha.append("_")
            self.puzzle.append(newLinha.copy()) # adicionar uma copia ao puzzle
        pass



    def estadoAtual(self):
        for l in self.puzzle:
            for c in l:
                print(c, end=" ")
            print("")


    def mudarPosicao(self, x_movimento, y_movimento): # muda o valor da posicao [x,y] na matriz com o vazio
        self.puzzle[self.x][self.y], self.puzzle[x_movimento][y_movimento] = self.puzzle[x_movimento][y_movimento], self.puzzle[self.x][self.y]
        self.x, self.y = x_movimento, y_movimento




    def mover(self, movimento):# 8 - cima, 6 - direita, 2 - baixo, 4 - direita
        lados = self.verificarLados(self.x, self.y)
        naoPode = ["|", "_", "+",] #lados que nao posso mover para ...

        if movimento == 2 and lados[0] not in naoPode:
            self.mudarPosicao(self.x - 1, self.y)
        elif movimento == 4 and lados[1] not in naoPode:
            self.mudarPosicao(self.x, self.y + 1)
        elif movimento == 8 and lados[2] not in naoPode:
            self.mudarPosicao(self.x + 1, self.y)
        elif movimento == 6 and lados[3] not in naoPode:
            self.mudarPosicao(self.x, self.y - 1)
        else:
            return None
        self.mf += 1
        self.movimentos += 1
        return True


    def verificarLados(self, x , y): #verifica os lados que o espaco vazio se encontra
        return [
            self.puzzle[x - 1][y],
            self.puzzle[x][y + 1],
            self.puzzle[x + 1][y],
            self.puzzle[x][y - 1],
        ]

    def venceu(self): # verificar se ja venceu
        puzzle = ""
        for i in self.puzzle:
            for c in i:
                puzzle += str(c)

        puzzle = puzzle.replace(" ", "").replace("|", "").replace("+", "").replace("_", "")
        if puzzle.replace(" ", "").replace("|", "").replace("+", "") == "12345678":
            return False
        return True


    '''
    METODOS DA IA
    '''

    # criar jogadas possiveis
    # enviar para heuristica
    # metodo h2 gera uma lista com distancia das origens
    # calcular qual tem menor custo
    #entrando em loop, salvar ultima jogada e retirar da lista de possiveis jogadas ?

    def buscaGulosa(self):
        #movimentosPossiveis = []
        heuristicas = []
        somas = []

        for i in range(2, 9, 2): # verifica todos os movimentos possiveis na jogada atual e depois calcula a heuristica
            try:
                heuristicas.append([self.heuristicaH2(self.verificarMovimento(i)), i])
            except:
                continue

        for h in heuristicas:
            somas.append([self.somarHeuristica(h[0]), h[1]])



        movimentoFazer = min(somas)[1]
        somas.remove(min(somas))

        if(self.ultimoMovimento == self.inverterMovimento(movimentoFazer)):
            movimentoFazer = min(somas)[1]
            somas.remove(min(somas))

        puzzleMovimentado = self.verificarMovimento(movimentoFazer)




        if puzzleMovimentado not in self.movimentosFeitos and self.ultimoMovimento != movimentoFazer:
            self.movimentosFeitos.append(puzzleMovimentado.copy())
            self.mover(movimento=movimentoFazer)
            self.ultimoMovimento = movimentoFazer
            '''if self.mf > 256:
                self.mf = 0
                self.movimentosFeitos.clear()'''
        else:
            while True:
                u = self.rdn.randrange(2, 10, 2)
                self.ultimoMovimento = u
                m = self.mover(movimento=u)
                if m:
                    break

    def somarHeuristica(self, listHeuristica):
        soma = 0
        for i in listHeuristica:
            soma += i

        return soma

    def inverterMovimento(self, movimento):
        if movimento == 2:
            return 8
        elif movimento == 8:
            return 2
        elif movimento == 4:
            return 6
        elif movimento == 6:
            return 4

    # muda o valor da posicao [x,y] na matriz com o vazio, mas somente como uma copia, sem afetar o original
    def mudarPosicaoDaCopia(self, x_movimento, y_movimento):
        puzzleCopy = deepcopy(self.puzzle)
        puzzleCopy[self.x][self.y], puzzleCopy[x_movimento][y_movimento] = puzzleCopy[x_movimento][y_movimento], puzzleCopy[self.x][self.y]

        return puzzleCopy

    def verificarMovimento(self, movimento):
        lados = self.verificarLados(self.x, self.y)
        naoPode = ["|", "_", "+",] #lados que nao posso mover para ...
        puzzle_movimento = None


        if movimento == 2 and lados[0] not in naoPode:
            puzzle_movimento = self.mudarPosicaoDaCopia(self.x - 1, self.y)
        elif movimento == 4 and lados[1] not in naoPode:
            puzzle_movimento = self.mudarPosicaoDaCopia(self.x, self.y + 1)
        elif movimento == 8 and lados[2] not in naoPode:
            puzzle_movimento = self.mudarPosicaoDaCopia(self.x + 1, self.y)
        elif movimento == 6 and lados[3] not in naoPode:
            puzzle_movimento = self.mudarPosicaoDaCopia(self.x, self.y - 1)


        return puzzle_movimento

    def heuristicaH2(self, puzzle): # gerar heuristica

        pontosDeOrigins = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]] # origens dos pontos

        listaHeuristica = []
        l = 0
        c = 0

        for elemento in range(1, 9):
            x, y = self.posicaoXY(elemento, puzzle)
            listaHeuristica.append(self.distancia(y, x, pontosDeOrigins[elemento - 1][0], pontosDeOrigins[elemento - 1][1]))

        return listaHeuristica

    def distancia(self, x, y, x_origin, y_origin): # retorna a distancia da sua origem
        distacia = 0
        x_cremento = 1
        y_cremento = 1
        if x > x_origin:
            x_cremento = -1
        if y > y_origin:
            y_cremento = -1

        for c in range(x, x_origin, x_cremento):
            distacia += 1

        for l in range(y, y_origin,y_cremento):
            distacia += 1

        return distacia

    def posicaoXY(self, elemento, puzzle): # pega a posicao x, y na matriz do elemento
        y = 1
        naoContaveis = ["+", "_"]
        x = []
        for x in puzzle:
            if elemento in x:
                break
            elif naoContaveis[0] not in x and naoContaveis[1] not in x:
                y += 1

        return x.index(elemento), y