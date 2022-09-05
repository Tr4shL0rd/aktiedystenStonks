#!/usr/bin/env python3
import os
import csv
import json
import time
import requests
import subprocess
from sys import argv
from rich import print as rprint

with open("config.json", "r") as configFile:
    config = json.load(configFile)
STOCKNAME="JYSK"
UNIT="Kr."
POPUP=True
if "ANDROID_BOOTLOGO" in os.environ:
    POPUP=False

try:
    DEBUG = False
    if argv[1].upper() == "DEBUG" or "d":
        DEBUG = True
except IndexError:
    DEBUG = False


def clear() -> str:
    return "\n"*32


def popUp(message: str, timeout=5):
    if POPUP:
        subprocess.Popen(["notify-send", "-a", STOCKNAME,
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

    url = "https://aktiedysten.dk/z/chart?q=s.i1d.full(CPH~JYSK)"

    response = requests.request("GET", url)

    data = json.loads(response.text)
    price = data["Encoded"]["Data"]
    currentPrice = round(price[-2], 1)
    beforePrice = round(price[-4], 1)
    print(
        f"Last    Price: {beforePrice}{UNIT}\n"
        f"Current Price: {currentPrice}{UNIT}"
    )
    if DEBUG:
        print(price)
    if float(stockPrice[0]) <= currentPrice:  # if boughtPrice >= currentPrice:
        rprint(f"[green]diff: {round(currentPrice-beforePrice,1)}{UNIT}[/green]")
        rprint("[underline bold green]!PROFIT BOIS![/underline bold green]")
        popUp(
            f"{STOCKNAME}: {currentPrice}{UNIT}\ndiff: {round(currentPrice-beforePrice,1)}{UNIT}\nPROFIT", config["popUp_delay"])
    elif currentPrice < beforePrice:
        rprint(f"[red]diff: {round(currentPrice-beforePrice,1)}{UNIT}[/red]")
        rprint("[underline  bold red]FALLING![/underline bold red]")
        popUp(
            f"{STOCKNAME}: {currentPrice}{UNIT}\ndiff: {round(currentPrice-beforePrice,1)}{UNIT}\nFalling", config["popUp_delay"])
    elif currentPrice > beforePrice:
        rprint(f"[green]diff: {round(currentPrice-beforePrice,1)}{UNIT}[/green]")
        rprint("[underline bold green]RISING[/underline bold green]")
        popUp(
            f"{STOCKNAME}: {currentPrice}{UNIT}\ndiff: {round(currentPrice-beforePrice,1)}{UNIT}\nRISING", config["popUp_delay"])
    else:
        rprint(f"[yellow]diff: {round(currentPrice-beforePrice,1)}{UNIT}[/yellow]")
        rprint("[bold yellow]SAME[/bold yellow]")
        popUp(
            f"{STOCKNAME}: {currentPrice}{UNIT}\ndiff: {round(currentPrice-beforePrice,1)}{UNIT}\nSAME", config["popUp_delay"])

    time.sleep(config["check_delay"])


try:
    while True:
        main()
except requests.ConnectionError:
    print("Cannot connect to wifi")
