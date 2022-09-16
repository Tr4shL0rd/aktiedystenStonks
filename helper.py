import subprocess
import json
from currency_converter import CurrencyConverter

def flatten(l:list):
    '''
        flattens l:list and returns new list 
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

def loadJson():
    '''
        loads the json config file
    '''
    return json.load(open("config.json"))

def convertCurrency(amount, fromCurrency:str="DKK",targetCurrency:str="USD"):
    '''
        converts amount:int or str of fromCurrency:str to targetCurrency:str 
        >>> convertCurrency(100, "DKK", "USD")
        13.43kr.
        >>> convertCurrency(100, "USD", "DKK")
        $744.33
    '''
    return round(CurrencyConverter().convert(amount, fromCurrency, targetCurrency),1)
