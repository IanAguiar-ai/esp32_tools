"""
Client esp
"""
from time import sleep

class Client:
    def __init__(self, key = None):
        self.connected = False
        self.ip = self.try_ip()

        #Function:
        self.key = key
        #self.key(ip:list) -> [int, int, int, int]
        #ip:list = [int, int, int, int]

    def try_connected(self, time_:float = 10):
        #Tenta conectar por 10 segundos
        #Se conseguir:
        #Manda uma mensagem assim: first connection
        self.connected = True
        #return ip

    def try_ip(self):
        
        #Vê se existe um txt chamado key
        #Sim:
            
            
        #Caso ele não consiga conectar ou o txt não exista...
        while True:
            #Vai no repositório git pegar a key
            sleep(60*15) #Se não conseguir ele tenta de novo em 30 segundos
            #Assim que ele conseguir pegar a key salva em um txt a key
            #Tenta conectar por 10 segundos
            #Se conseguir
            
