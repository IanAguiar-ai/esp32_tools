"""
Viral OTA
"""
import os
from time import sleep
import espnow
import network

class vota:
    """
    É um OTA viral, não precisa de servidor, ele vai contagiando outros pontos com as versões mais novas

    comandos para comunicação:
    <send_[key]>
    <send_to_me> [key]|[ip]
    <versions> [key]:[ip]|[key]:[ip]|[key]:[ip]
    <del> [key]|[ip]
    <ips> [ip]|[ip]|[ip]|[ip]
    """
    def __init__(self, ips:list):
        """
        Inicia com os ips que ele conectara e com as versões de cada aplicação além dos arquivos presentes na memória
        """
        self.ips = ips
        arqs = os.listdir()
        for rem in ["boot.py", "main.py"]:
            arqs.remove(rem)
        self.arqs = arqs
        self.versions = self.find_versions()
        self.send_to_me = []
        self.sta = networt.WLAM(network.STA_IF)
        self.sta.active(True)
        informations()
        self.esp = espnow.ESPNow()
        self.esp.active(True)
        self.my_mac = self.sta.config('mac')


    def informations(self):
        print(f"MAC: {sta.config('mac')}")


    def find_versions(self, file:str = False):
        """
        Acha a versão da aplicação na sua memória
        """

        if not file:
            versions = {}
            for file in self.arqs:
                data = open(file)
                read = data.read()
                data.close()

                version_program = read[read.find("version") + len("version"):]
                del read
                version_program = version_program[version_program.find("=") + len("="):version_program.find("\n")]
                version_program = version_program.replace("[","").replace("]","")
                version_program = list(map(int, version_program.split(",")))

                version[file] = version_program
                
            return version
        else:
            data = open(file)
            read = data.read()
            data.close()

            version_program = read[read.find("version") + len("version"):]
            del read
            version_program = version_program[version_program.find("=") + len("="):version_program.find("\n")]
            version_program = version_program.replace("[","").replace("]","")
            version_program = list(map(int, version_program.split(",")))
            
            return version_program


    def viral(self):
        """
        Para cada ip diferente ele tenta conectar e manda a versão das aplicações para ele
        """
        self.send_version()
        self.send_ips()

        time_options = [3, 11]
        for i in range(time_options[int(random()*len(time_options))]*1000):
            #Ficar aberto para receber por 3 ou 11 segundos
            host, msg = self.esp.recv()
            sleep(0.01)
                
            #Se ele tiver recebido algo:
            self.receive(msg, host)

            if (not host in self.ips) and (host != self.my_mac):
                self.ips.append(host)

        if self.send_to_me != []:
            self.send()          


    def send_for_all(self, message):
        for peer in self.ips:
            self.esp.add_peer(peer)
            self.esp.send(peer, message, True)


    def send_for(self, peer, message):
        self.esp.add_peer(peer)
        self.esp.send(peer, message, True)


    def send_version(self):
        """
        Manda as versões para o outro ponto, o ponto terá o papel de conferir cada versão e pedir para que mande alguma versão
        """
        to_send = "<versions>"
        for key in self.versions:
            value = self.versions[]
            value = value[0] * 1_000_000 + value[1] * 1_000 + value[2]
            to_send += f"{key}:{value}|"
        to_send = to_send[:-1]

        send_for_all(to_send)


    def send_ips(self):
        """
        Manda os ips conhecidos para todos os pontos possíveis
        """
        to_send = "<ips>"
        for ip in self.ips:
            to_send += f"{ip}|"
        to_send = to_send[:-1]

        self.send_for_all(to_send)


    def receive(self, text:str):
        """
        Após receber uma mensagem trata ela
        """        

        if text.find("<versions>"): #Se algum ponto tiver mandado as versões que ele tem
            text.replace("<versions>", "")
            versions = {}
            for value in text.split("|"):
                value_real = value.split(":")
                versions[value_real[0]] = int(value_real[1])

            for key in versions:
                if key in self.versions:
                    my_version = self.versions[key][0] * 1_000_000 + self.versions[key][0] * 1_000 + self.versions[key][2]
                    if versions[key] > my_version and (not [key, ip] in send_to_me):
                        self.send_to_me.append([key, ip])

            print("Save list of new prograns to send to me")

        elif text.find("<send_to_me>"):
            text.replace("<send_to_me>", "")
            text, ip = text.split("|")

            #Ler tamanho do arquivo
            len_file = len(file)
            chunks = int(len_file/200) + 1)

            #Mandar de 200 a 200 caracteres o arquivo
            print("f<send_{text}> ({chunks} chunks)", end = "")
            for i in range(0, len_file, 200):
                #mandar len_file[i:i+200]
                self.send_for(ip, f"<send_{text}>file[i:i+200]")
                
            #mandar <del>{text}|{ip}
            self.senf_for(ip, f"<del>{text}|{ip}")
            print("| (send OK)")

        elif text.find("<send_"):
            arq = text[text.find("<send_") + len("<send_"):text.lfind(">")]
            text = text[text.lfind(">"):]

            file = open(f"new_{arq}.py")
            file.write(text)
            file.close()
            print(f"Save chunk of {text}")

        elif text.find("<del>"):
            text.replace("<del>", "")
            text = text.split("|")
            self.send_to_me.remove([text, ip])
            del self.versions[text] #Tira essa atualização da lista para que ele não possa mais ser atualizado até que seja dado o update
            print(f"{text} for {ip} remove requesition send")

        elif text.find("<ips>"):
            text.replace("<ips>", "")
            text = text.split("|")
            for host in text:
                if (not host in self.ips) and (host != self.my_mac):
                    self.ips.append(host)
            print(f"ips of other point receive")


    def send(self):
        """
        Mandar uma mensagem para o ip específico
        """
        for key, ip in self.send_to_me:
            text = f"<send_to_me>{key}"

            #Tentar mandar mensagem para o ip
            self.send_for(ip, text)


    def update_programs(self):
        """
        Atualiza todos os programas se possível
        """
        for arq in self.arqs:
            #Se existe f'new_{arq}' apaque o original e renomeie o novo
            if f"new_{arq}" in os.listdir():
                os.remove(name)
                os.rename(f"new_{arq}", arq)

            self.versions[arq] = find_versions(file = arq)
        self.arqs = os.listdir()

