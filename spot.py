import json
import time
import requests
import subprocess
import csv
from sys import argv
from rich import print as rprint
try: 
    DEBUG = False
    if argv[1].upper() == "DEBUG" or "d":
        DEBUG = True
except IndexError:
    DEBUG = False

def clear() -> str:
    return "\n"*32


def popUp(message: str, timeout=5):
    subprocess.Popen(["notify-send", "-a", "SPOT",
                     "-t", str(timeout*1000), message])


def main():
    with open("boughtPrices.csv", "r") as boughtPricesFile:
        reader = csv.reader(boughtPricesFile)
        next(reader)
        stockName = []
        stockPrice = []
        for row in reader:
            stockName.append(row[0])
            stockPrice.append(row[1])
        
    url = "https://aktiedysten.dk/z/chart?q=s.i1d.full(NYSE~SPOT)"

    response = requests.request("GET", url)

    data = json.loads(response.text)
    price = data["Encoded"]["Data"]
    currentPrice = round(price[-2], 1)
    beforePrice = round(price[-4], 1)
    print(
        f"Last    Price: {beforePrice}$\n"
        f"Current Price: {currentPrice}$"
    )
    if DEBUG: print(price)
    if float(stockPrice[0]) <= currentPrice:  # if boughtPrice >= currentPrice:
        rprint(f"[green]diff: {round(currentPrice-beforePrice,1)}$[/green]")
        rprint("[underline bold green]!PROFIT BOIS![/underline bold green]")
        popUp(
            f"SPOT: {currentPrice}$\ndiff: {round(currentPrice-beforePrice,1)}$\nPROFIT")
    elif currentPrice < beforePrice:
        rprint(f"[red]diff: {round(currentPrice-beforePrice,1)}$[/red]")
        rprint("[underline  bold red]FALLING![/underline bold red]")
        popUp(
            f"SPOT: {currentPrice}$\ndiff: {round(currentPrice-beforePrice,1)}$\nFalling")
    elif currentPrice > beforePrice:
        rprint(f"[green]diff: {round(currentPrice-beforePrice,1)}$[/green]")
        rprint("[underline bold green]RISING[/underline bold green]")
        popUp(
            f"SPOT: {currentPrice}$\ndiff: {round(currentPrice-beforePrice,1)}$\nRISING")
    else:
        rprint(f"[yellow]diff: {round(currentPrice-beforePrice,1)}$[/yellow]")
        rprint("[bold yellow]SAME[/bold yellow]")
        popUp(
            f"SPOT: {currentPrice}$\ndiff: {round(currentPrice-beforePrice,1)}$\nSAME")

    time.sleep(60/2)


try:
    while True:
        main()
except requests.ConnectionError:
    print("Cannot connect to wifi")
