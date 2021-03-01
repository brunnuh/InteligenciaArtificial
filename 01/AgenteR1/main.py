import os
from time import sleep

from ambiente import Ambiente
from timeit import default_timer

def main():

    teste = Ambiente(50)
    teste.montarAmbiente()
    #teste.mostrarAmbiente()
    #print(teste.ambiente)
    #teste.popularPadrao()
    #teste.mostrarAmbiente()
    inicio = default_timer()
    while teste.verificarAmbiente():
        teste.mostrarAmbiente()
        #teste.mostrarEstado()
        teste.atuarNoAmbiente()
        #sleep(0.5)
        os.system('cls')
        #pass
    fim = default_timer()
    #teste.mostrarAmbiente()
    print(f"tempo decorrido {fim - inicio}")
if __name__ == '__main__':
    main()
