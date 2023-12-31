"""
Application to do OTA

You must pass the github link of the code you want to update,
it must always have a line written 'version'.

Use:
link = 'your_link_github'
ota(link)
"""
import requests
import os

def find_version(dir_:str):
    """
    Find the file version
    """
    text = []

    with open(dir_, 'r') as arq:
        text = arq.readlines()

    for line in text:
        if line.replace(" ","").find('version=[')> -1 or line.replace(" ","").find('version=(')> -1:
            n = line
            for rep in ["version", " ", "=", "[", "]", "(", ")"]:
                n = n.replace(rep, "")
            version = list(map(int, n.split(",")))
            print(f"Version {version[0]}.{version[1]}.{version[2]}")
            return version
    return [0, 0, 0]

def rename(dir_:str):
    old = 'old_' + dir_
    os.rename(dir_, old)
    print(f"{dir_} is now {old}")

def ota(link:str):
    """
    Pass the github link of the code you want to update.
    """
    #Requesition:
    name = link[link.rfind("/") + 1:]

    try:
        x = requests.get(link)
        print(f'encoding: {x.encoding}')
    except:
        print("The previous link does not exist!")
        return None

    #Old  version to compare:
    try:
        version = find_version(name)
    except:
        print(f"This file ({name}) does not exist in memory!")
        return None

    #Code manipulation:
    text = x.text
    text = text.split('","')

    line_ = 0
    for line in text:
        if line.find('"rawLines":[')> -1:
            start = line_ + 1

        elif line.find('"],"stylingDirectives"')> -1:
            end = line_

        elif line.replace(" ","").find('version=[')> -1 or line.replace(" ","").find('version=(')> -1:
            n = line
            for rep in ["version", " ", "=", "[", "]", "(", ")", "\\", "r"]:
                n = n.replace(rep, "")
            new_version = list(map(int, n.split(",")))
        line_ += 1

    text = text[start:end]

    #Save new code if is newer:
    try:
        if version[0] * 1_000_000 + version[1] * 1_000 + version[2] < new_version[0] * 1_000_000 + new_version[1] * 1_000 + new_version[2]:
            try:
                dir_ = name
                with open(dir_, 'w') as arq:
                    for line in text:
                        print(line)
                        arq.write(f'{line}\n')
            except:
                rename(name)

            print(f'OTA completed!')
            return True
        else:
            print(f"You are already on the latest version of {name} (version = {version[0]}.{version[1]}.{version[2]})!")
            return False
    except UnboundLocalError:
        print("The update file does not have the corresponding version.")
        return None
        

if __name__ == "__main__":
    ota("https://github.com/IanAguiar-ai/teste_ota/blob/main/aplicacao.py")
