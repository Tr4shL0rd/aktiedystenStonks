import subprocess

def flatten(l):
    '''
        flattens and returns list l
    '''
    return [item for sublist in l for item in sublist]

def popUp(message: str, timeout=5, stockName="STOCKNAME"):
    '''
        sends a KDE popup with a message, amount of time it is shown and the stockname 
    '''
    try:
        subprocess.Popen(["notify-send", "-a", stockName,
                        "-t", str(timeout*1000), message])
    except FileNotFoundError:
        pass

def clear(amount=32):
    '''
        clears the screen with \n * amount
    '''
    print("\n"*amount)
