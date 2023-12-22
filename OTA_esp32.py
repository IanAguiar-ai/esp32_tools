"""
Application to do OTA

You must pass the github raw link of the code you want to update,
it must always have a line written 'version'.

Use:

link = 'your_link_github_raw'
name = 'program.py'
if not ota_update(name):
    ota_download(link)
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

def ota(link:str, chunk_size:int = 4096):
    """
    Full OTA
    """
    name = link[link.rfind("/") + 1:]
    if not ota_update(name):
        ota_download(link)
    return True

def ota_download(link:str, chunk_size:int = 4096, name:str = None):
    """
    Download the program and save it so the board can be updated
    """
    collect()
    
    if name == None:
        name = link[link.rfind("/") + 1:]

    try:
        x = get(link)
        print(f'encoding: {x.encoding}')
    except:
        print("The previous link does not exist!")
        return None

    len_ = 100_000
    print(f"Download {name}...\n|", end="")
    can_write = True

    with open("new_"+name, 'w') as arq:
        for i in range(0, len_, chunk_size):
            if can_write:
                line = x.raw.read(chunk_size).decode(x.encoding)
                if line.replace(" ","").find('version=[') > -1:
                    n = line[line.replace(" ","").find('version=[') + len('version=['):]
                    n = n[:n.find("]")]
                    for rep in ["version", " ", "=", "[", "]", "(", ")"]:
                        n = n.replace(rep, "")
                    new_version = list(map(int, n.split(",")))
                    if not (version[0] * 1_000_000 + version[1] * 1_000 + version[2] < new_version[0] * 1_000_000 + new_version[1] * 1_000 + new_version[2]):
                        can_write = False
                arq.write(f'{line}\n')
            print("=", end="")
            collect()
    print("| (Download complete)")

    try:
        if not can_write:
            os.remove("new_"+name)
        return False
    except:
        pass
    return True

def ota_update(name:str):
    """
    Update the program that has already been downloaded
    """
    collect()

    try:
        version = find_version("new_"+name)
    except:
        print(f"This file ({name}) does not exist in memory!")
        return False

    try:
        os.remove(name)
        os.rename("new_"+name, name)
        print(f"OTA completed!")
        return True
    except UnboundLocalError:
        print("The update file does not have the corresponding version.")
        return False
