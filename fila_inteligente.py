"""
Biblioteca que executa funções sem input de acordo com o tempo escolhido
"""

from time import sleep, time

class Fila:
    def __init__(self, print_ = False):
        self.fila:list = []
        self.print_ = print_

    def run(self) -> None:
        t0:int = time()
        while True:
            correcao = time()
            esperar = min(self.fila, key = lambda x: x[2])
            tempo_espera = max(esperar[2], 0)

            if self.print_:
                print(f"Esperando {tempo_espera:0.3f} segundos para '{esperar[0].__name__}'")

            sleep(tempo_espera)
            t:int = time()

            tm:int = time()
            for i in range(len(self.fila)):
                self.fila[i][2] -= tm - t0

            t0:int = t
            self.fila = sorted(self.fila, key = lambda x: x[3], reverse = True)
            for i in range(len(self.fila)):
                if self.fila[i][2] <= 0 + (time() - (correcao + tempo_espera)):
                    self.fila[i][0]()
                    self.fila[i][2] = self.fila[i][1] - (time() - t0)

    def adicionar(self, funcao:"funcao", tempo:float, nivel:int = 0) -> None:
        self.fila.append([funcao, tempo, tempo, nivel])

if __name__ == "__main__":
    def printar_1():
        print("1", end = "")

    def printar_2():
        print("2", end = "")

    def printar_3():
        print("3", end = "")

    def printar_4():
        print("4", end = "")
        sleep(1)

    def printar_():
        print("-", end = "")

    teste = Fila()

    n = 1
    teste.adicionar(printar_1, 1 * n, 4)
    teste.adicionar(printar_2, 2 * n, 3)
    teste.adicionar(printar_3, 3 * n, 2)
    teste.adicionar(printar_4, 4 * n, 1)
    teste.adicionar(printar_, 0.2 * n, 0)

    teste.run()
