"""
Application to do OTA

You must pass the github link of the code you want to update,
it must always have a line written 'version'.

Use:
link = 'your_link_github'
ota(link)
"""
from urequests import get
import os
from gc import collect

def find_version(dir_: str):
    with open(dir_, 'r') as arq:
        for line in arq:
            if line.replace(" ", "").find('version=[') > -1 or line.replace(" ", "").find('version=(') > -1:
                n = line
                for rep in ["version", " ", "=", "[", "]", "(", ")"]:
                    n = n.replace(rep, "")
                version = list(map(int, n.split(",")))
                print(f"Version {version[0]}.{version[1]}.{version[2]}")
                return version
    return [0, 0, 0]

def rename(dir_: str):
    old = 'old_' + dir_
    os.rename(dir_, old)
    print(f"{dir_} is now {old}")

def ota(link:str, chunk_size:int = 4096, name:str = None):
    collect()
    
    if name == None:
        name = link[link.rfind("/") + 1:]

    try:
        x = get(link)
        print(f'encoding: {x.encoding}')
    except:
        print("The previous link does not exist!")
        return None

    try:
        version = find_version(name)
    except:
        print(f"This file ({name}) does not exist in memory!")
        return None

    # Code manipulation:
    len_ = 99999
    print(f"Download {name}...\n|", end="")
    can_write = False
    exist_file = False

    with open("new_"+name, 'w') as arq:
        for i in range(0, len_, chunk_size):
            segment = x.raw.read(chunk_size).decode(x.encoding)
            for line in segment.split('","'):
                if line.replace(" ","").find('version=[') > -1:
                    n = line[line.replace(" ","").find('version=[') + len('version=['):]
                    n = n[:n.find("]")]
                    for rep in ["version", " ", "=", "[", "]", "(", ")"]:
                        n = n.replace(rep, "")
                    new_version = list(map(int, n.split(",")))
                arq.write(f'{line}\n')
                
                print("=", end="")
            collect()
    print("|")

    try:
        new_version = find_version("new_"+name)
        if version[0] * 1_000_000 + version[1] * 1_000 + version[2] < new_version[0] * 1_000_000 + new_version[1] * 1_000 + new_version[2]:
            os.remove(name)
            os.rename("new_"+name, name)
            print(f"OTA completed!")
            return True
        else:
            print(f"You are already on the latest version of {name} (version = {version[0]}.{version[1]}.{version[2]})!")
            return False
    except UnboundLocalError:
        print("The update file does not have the corresponding version.")
        return None
