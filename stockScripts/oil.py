#!/usr/bin/env python3
import csv
import json
import time
import requests
from sys import argv
from rich import print as rprint
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import helper

config = helper.loadConfig()
STOCKNAME="OIL"
UNIT="$"

try:
    DEBUG = False
    if argv[1].upper() == "DEBUG" or "d":
        DEBUG = True
except IndexError:
    pass

def main():
    with open("boughtPrices.csv", "r") as boughtPricesFile:
        reader = csv.reader(boughtPricesFile)
        next(reader)
        stockName = []
        stockPrice = []
        for row in reader:
            stockName.append(row[0])
            stockPrice.append(row[1])

    url = "https://aktiedysten.dk/z/chart?q=s.i1d.full(BRENT~LCO)"

    response = requests.get(url)

    data = json.loads(response.text)
    price = data["Encoded"]["Data"]
    currentPrice = round(price[-1], 1)
    beforePrice = round(price[-4], 1)
    print(
        f"Last    Price: {beforePrice}{UNIT}\n"
        f"Current Price: {currentPrice}{UNIT}"
    )
    if DEBUG:
        print(price)
    if float(stockPrice[1]) <= currentPrice:  # if boughtPrice >= currentPrice:
        rprint(f"[green]diff: {round(currentPrice-beforePrice,1)}{UNIT}[/green]")
        rprint("[underline bold green]!PROFIT BOIS![/underline bold green]")
        helper.popUp(
                f"{STOCKNAME}: {currentPrice}{UNIT}\ndiff: {round(currentPrice-beforePrice,1)}{UNIT}\nPROFIT", 
                config["popUp_delay"],
                STOCKNAME
            )
    if currentPrice < beforePrice:
        rprint(f"[red]diff: {round(currentPrice-beforePrice,1)}{UNIT}[/red]")
        rprint("[underline bold red]FALLING![/underline bold red]")
        helper.popUp(
                f"{STOCKNAME}: {currentPrice}{UNIT}\ndiff: {round(currentPrice-beforePrice,1)}{UNIT}\nFalling", 
                config["popUp_delay"],
                STOCKNAME
            )
    elif currentPrice > beforePrice:
        rprint(f"[green]diff: {round(currentPrice-beforePrice,1)}{UNIT}[/green]")
        rprint("[underline bold green]RISING[/underline bold green]")
        helper.popUp(
                f"{STOCKNAME}: {currentPrice}{UNIT}\ndiff: {round(currentPrice-beforePrice,1)}{UNIT}\nRISING", 
                config["popUp_delay"],
                STOCKNAME
            )
    else:
        rprint(f"[yellow]diff: {round(currentPrice-beforePrice,1)}{UNIT}[/yellow]")
        rprint("[bold yellow]SAME[/bold yellow]")
        helper.popUp(
                f"{STOCKNAME}: {currentPrice}{UNIT}\ndiff: {round(currentPrice-beforePrice,1)}{UNIT}\nSAME", 
                config["popUp_delay"],
                STOCKNAME
            )

    time.sleep(config["check_delay"])


try:
    while True:
        main()
except requests.ConnectionError:
    print("Cannot connect to wifi")
except KeyboardInterrupt:
    print("exiting...")
