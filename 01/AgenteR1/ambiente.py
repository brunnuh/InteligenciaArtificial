from random import Random, seed

seed(1)


class Ambiente:
    def __init__(self, size = 20):
        self.rnd = Random()
        self.ambiente = list()
        self.size = size
        self.agente_x = 1
        self.agente_y = 1
        self.parede = ["|", "+", "_"]
        self.comandos = [
            "CIMA",
            "DIREITA",
            "BAIXO",
            "ESQUERDA",
            "LIMPAR"
        ]
        self.ultimaAcao = ""
        self.regra = "continuar"
        self.estado_retroceder = []
        self.estado = list() #estado atual do mundo






    def montarAmbiente(self):
        for x in range(0, self.size + 2):
            linha = []
            for y in range(0, self.size + 2):
                if y == 0 or y == self.size + 1:
                    if y == 0 and x == 0 or y == 0 and x == self.size + 1 or y == self.size + 1 and x == 0 or y == self.size + 1 and x == self.size + 1:
                        linha.append("+")
                    else:
                        linha.append("|")
                elif y > 0 and x > 0 and y < self.size + 1 and x < self.size + 1:
                    if(self.rnd.randint(0,1) == 1):
                        linha.append("*")
                    else:
                        linha.append(".")
                else:
                    linha.append("_")
            self.ambiente.append(linha)


    def mostrarAmbiente(self):
        for index_x, x in enumerate(self.ambiente):
            for index_y, y in enumerate(x):
                if(index_y == self.agente_x and index_x == self.agente_y):
                    print("A ", end="")
                else:
                    print(y + " ", end="")
            print("")

        print(f"x: {self.agente_x}\ny: {self.agente_y}\n")
        print(2*"\n")



    def verificarLados(self): # manda os lados onde o agente esta
        return [
            self.ambiente[self.agente_y - 1][self.agente_x],
            self.ambiente[self.agente_y][self.agente_x + 1],
            self.ambiente[self.agente_y + 1][self.agente_x],
            self.ambiente[self.agente_y][self.agente_x - 1]
        ]

    def verificarAmbiente(self):# verifica se ainda tem sujeira
        for x in self.ambiente:
            if("*" in x or "." in x):
                return True
        return False


    def funcaoAgentR1Simples(self):

        #if(self.ambiente[self.agente_y][self.agente_x] == "." or self.ambiente[self.agente_y][self.agente_x] == "*"): # se o local onde o agente estiver sujo
            #self.ambiente[self.agente_y][self.agente_x] = " "

        lados = self.verificarLados()

        if "*" in lados:
            return self.comandos[lados.index("*")] #retorna o comado apos verificar em que posicao esta o primeiro *
        elif "." in lados:
            return self.comandos[lados.index(".")] #retorna o comado apos verificar em que posicao estao o primeiro .
        else:
            while(True):
                posicao = self.rnd.randint(0, 4)
                if(lados[posicao] not in self.parede):
                    return self.comandos[posicao]

    def atualizarEstado(self, lados):  # atualiza o estado, para ser mais recente
        try:
            if self.inverterDirecao(self.ultimaAcao) == self.estado[-1][1]:  # se tiver retornando, retirar a ultima posicao
                self.estado.pop(-1)
            else:
                self.estado.append([lados, self.ultimaAcao])
        except:
            self.estado.append([lados, self.ultimaAcao])


    def inverterDirecao(self, direcao):
        if direcao == "CIMA":
            return "BAIXO"
        elif direcao == "DIREITA":
            return "ESQUERDA"
        elif direcao == "BAIXO":
            return "CIMA"
        elif direcao == "ESQUERDA":
            return "DIREITA"
        return ""

    def mostrarEstado(self):
        print(self.estado)


        #for pos in self.estado:

    def validarLado(self, lados):
        try:
            if "*" in lados or "." in lados:#("*" in self.estado[-1][0] or "." in self.estado[-1][0]):
                self.regra = "continuar"
                return "continuar"
            else:
                self.regra = "retroceder"
                return "retroceder"
        except:
            self.regra = "continuar"
            return "continuar"

    def funcaoAgenteR1Modelo(self):

        lados = self.verificarLados()

        #regras = ["continuar", "regredir"]

        if(self.regra == "continuar"):
            self.atualizarEstado(lados)
        #else:
            #self.estado_retroceder = lados

        if self.validarLado(lados) == "continuar":

            if "*" in lados:
                return self.comandos[
                    lados.index("*")]  # retorna o comado apos verificar em que posicao esta o primeiro *
            elif "." in lados:
                return self.comandos[
                    lados.index(".")]  # retorna o comado apos verificar em que posicao estao o primeiro .
        else:
            #print(f"voltando para {self.estado.pop(-1)}")
            lado = self.estado.pop()
            return self.inverterDirecao(lado[1])

    def atuarNoAmbiente(self, type = 1):
        try:
            #self.ultimaAcao = ""

            #self.ambiente[self.agente_x][self.agente_y] = " "

            if type == 0:#refatorar
                self.ultimaAcao = self.funcaoAgentR1Simples()
            elif type == 1:
                self.ultimaAcao = self.funcaoAgenteR1Modelo()
            elif type == 2:
                self.ultimaAcao = self.funcaoAgenteR1Objetivo()


            if self.ambiente[self.agente_y][self.agente_x] == "." or self.ambiente[self.agente_y][
                self.agente_x] == "*":  # se o local onde o agente estiver sujo
                self.ambiente[self.agente_y][self.agente_x] = " "
            #print(self.ultimaAcao, "\n\n")
            if self.ultimaAcao == self.comandos[0]:  # se for pra cima
                self.agente_y -= 1
            elif self.ultimaAcao == self.comandos[1]:  # direita
                self.agente_x += 1
            elif self.ultimaAcao == self.comandos[2]:  # baixo
                self.agente_y += 1
            else:
                self.agente_x -= 1
        except:
            #print("erro")
            pass

    def popularPadrao(self):
        matriz = "+ _ _ _ _ _ _ +p| * * . . . * |p| * . . * * . |p| * . . . * . |p| . * . . . . |p| . . . . . . |p| . . . * . . |p+ _ _ _ _ _ _ +p"
        x = 0
        y = 0
        linha = []
        for l in matriz:
            if l == "p":
                self.ambiente.append(linha.copy())
                linha.clear()
            elif(l != " "):
                linha.append(l)
        #print(self.ambiente)

    def incrementaLado(self, index, x, y):
        if index == 0:
            y -= 1
        elif index == 1:
            x += 1
        elif index == 2:
            y += 1
        else:
            x -= 1

        return x,y

    def verificarMelhorRota(self, lados):

        melhorDist = []

        invalidos = [" ", "_", "|", ""]

        for index, lado in enumerate(lados):
            ast = 0
            ponto = 0
            x = self.agente_x
            y = self.agente_y
            if(lado not in invalidos):
                x,y = self.incrementaLado(index, x, y)

            while(lado not in invalidos and self.ambiente[y][x] not in invalidos):

                if self.ambiente[y][x] == "*":
                    ast += 1
                elif self.ambiente[y][x] == ".":
                    ponto += 1
                x, y = self.incrementaLado(index, x, y)
            melhorDist.append([ast, ponto])
        #melhorDist.clear()
        #melhorDist = [[0,3], [0,2],[0,5],[0,-1]]
        maior = max(melhorDist)



        return self.comandos[melhorDist.index(maior)]


    def funcaoAgenteR1Objetivo(self): #erro - quando esta em lugar vazio vai para lugar aleatorio e sai do mapa

        lados = self.verificarLados()

        if (self.regra == "continuar"):
            self.atualizarEstado(lados)

        if self.validarLado(lados) == "continuar":
            return self.verificarMelhorRota(lados)
        else:
            lado = self.estado.pop()
            return self.inverterDirecao(lado[1])


#criar uma memoria por onde ele passou, pra caso ele chegue em uma situacao de todos os lados vazios, ele fazer o caminho reverso onde tem sujeira


#baseado em objetivos: criar uma funcao de busca que retorna o melhor caminho
#o que seria o melhor caminho ?
#o lado onde tem mais sujeira ?
#um caminho feito somente de * ?
#