"""
Class for assembling logs
"""
from time import time, localtime, sleep
import os

def time_now():
    data = localtime()
    return [data[0], data[1], data[2], data[3], data[4], data[5]]

class Log:
    """
    Creates a txt log that stores information along with the machine's local time
    """
    def __init__(self, file:str = "log"):
        """
        file: File name next to directory
        """
        if file == "log":
            t = time_now()
            file += f"_{t[2]}_{t[1]:02}_{t[0]:02}"
        if file.find(".txt") == -1:
            file += ".txt"
        self.file = file
        self.name = id(self)
        self.time_initial = time_now()
        self.create_file()

    def create_file(self):
        """
        Create txt file if file does not exist
        """
        if not self.file in os.listdir():
            with open(self.file, 'w') as arq:
                t = self.time_initial
                arq.write(f"<log creation> {t[0]:02}/{t[1]:02}/{t[2]} - {t[3]:02}:{t[4]:02}:{t[5]:02}")

        else:
            self.add(text = f"connecting to the log", description = "action")
            
        print(f"Files: {os.listdir()}")

    def add(self, text:str, description:str = "information"):
        """
        Add the requested text next to the time
        """
        if self.file in os.listdir():
            with open(self.file, 'r') as arq:
                old = arq.read()
        else:
            print("The log has been lost!")

        if self.file in os.listdir():
            with open(self.file, 'w') as arq:
                t = time_now()
                arq.write(f"{old}\n<{description}> {t[0]:02}/{t[1]:02}/{t[2]} - {t[3]:02}:{t[4]:02}:{t[5]:02} | {text}")
        else:
            print("The log has been lost!")
            
        self.compress()

    def backup(self, new_log:str = "backup_log"):
        """
        Back up the specified log
        new_log: Backup txt name
        """
        if new_log.find(".txt") == -1:
            new_log += ".txt"
        self.add(text = f"Make copy to '{new_log}'", description = "backup")
        with open(self.file, 'r') as arq:
            old = arq.read()
        if not new_log in os.listdir():
            with open(new_log, 'w') as arq:
                arq.write(old)

    def read(self):
        """
        Reads the log and returns a dictionary
        """        
        with open(self.file, 'r') as arq:
            old = arq.read()
        all_log = old.split("\n")
        
        all_log_dict = {}
        for i in range(len(all_log)):
            all_log[i] = all_log[i].replace("<","").split(">")
            if not all_log[i][0] in all_log_dict:
                all_log_dict[all_log[i][0]] = [all_log[i][1][1:]]
            else:
                all_log_dict[all_log[i][0]].append(all_log[i][1][1:])

        all_log_dict["all"] = old.split("\n")        
        return all_log_dict

    def __repr__(self):
        log = self.read()
        t = self.time_initial
        text = f"Log: {self.file}\nCreation Log: {log['log creation'][0]}\nOpen log: {t[0]:02}/{t[1]:02}/{t[2]} - {t[3]:02}:{t[4]:02}:{t[5]:02}\nLines Log: {len(log['all'])}"
        return text
    
    def remove(self):
        """
        Deleting .txt
        """
        os.remove(self.file)
        
    def size(self):
        """
        Size of .txt
        """
        return os.stat(self.file)[6]
    
    def compress(self):
        """
        Removing excess memory
        """
        if self.file in os.listdir():
            if self.size() > 1024 * 5:
                len_ = self.size()
                with open(self.file, 'r') as arq:
                    text = arq.read()
                    half = len(text) // 2
                    half = text[half + text[half:].find("\n") + len("\n"):]

                with open(self.file, 'w') as arq:
                    arq.write(half)
                print(f"Deleting old log, espace {len_}kb to {self.size()}kb")

