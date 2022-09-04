import json
import time
import requests
import subprocess
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
    subprocess.Popen(["notify-send", "-a", "OIL",
                     "-t", str(timeout*1000), message])


def main():
    url = "https://aktiedysten.dk/z/chart?q=s.i1d.full(BRENT~LCO)"

    response = requests.request("GET", url)

    data = json.loads(response.text)
    price = data["Encoded"]["Data"]
    currentPrice = round(price[-1], 1)
    beforePrice = round(price[-4], 1)
    print(
        f"Last    Price: {beforePrice}$\n"
        f"Current Price: {currentPrice}$"
    )
    if DEBUG: print(price)
    if 94.4 <= currentPrice:  # if boughtPrice >= currentPrice:
        rprint(f"[green]diff: {round(currentPrice-beforePrice,1)}$[/green]")
        rprint("[underline bold green]!PROFIT BOIS![/underline bold green]")
        popUp(
            f"OIL: {currentPrice}$\ndiff: {round(currentPrice-beforePrice,1)}$\nPROFIT")
    if currentPrice < beforePrice:
        rprint(f"[red]diff: {round(currentPrice-beforePrice,1)}$[/red]")
        rprint("[underline bold red]FALLING![/underline bold red]")
        popUp(
            f"OIL: {currentPrice}$\ndiff: {round(currentPrice-beforePrice,1)}$\nFalling")
    elif currentPrice > beforePrice:
        rprint(f"[green]diff: {round(currentPrice-beforePrice,1)}$[/green]")
        rprint("[underline bold green]RISING[/underline bold green]")
        popUp(
            f"OIL: {currentPrice}$\ndiff: {round(currentPrice-beforePrice,1)}$\nRISING")
    else:
        rprint(f"[yellow]diff: {round(currentPrice-beforePrice,1)}$[/yellow]")
        rprint("[bold yellow]SAME[/bold yellow]")
        popUp(
            f"OIL: {currentPrice}$\ndiff: {round(currentPrice-beforePrice,1)}$\nSAME")

    time.sleep(60/2)


try:
    while True:
        main()
except requests.ConnectionError:
    print("Cannot connect to wifi")
