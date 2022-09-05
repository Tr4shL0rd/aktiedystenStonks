#!/usr/bin/env python3
import os
import csv
import json
from urllib import response
import requests
from rich.table import Table
from rich.console import Console
def wifiCheck():
    try:
        return requests.get("https://www.google.com").status_code
    except requests.ConnectionError:
        print("Could not connect to wifi")
        print("Exiting...")
        exit()
def stockPrice():
    urlIndex = {
        "spot": "(NYSE~SPOT)",
        "oil":  "(BRENT~LCO)",
        "jysk": "(CPH~JYSK)",
    }
    url = "https://aktiedysten.dk/z/chart?q=s.i1d.full"

    responseSpot = requests.request("GET", f"{url}{urlIndex['spot']}")
    responseOil  = requests.request("GET",  f"{url}{urlIndex['oil']}")
    responseJysk = requests.request("GET", f"{url}{urlIndex['jysk']}")

    dataSpot = json.loads(responseSpot.text)
    dataOil  = json.loads(responseOil.text)
    dataJysk = json.loads(responseJysk.text)

    priceSpot = dataSpot["Encoded"]["Data"]
    priceOil  = dataOil["Encoded"]["Data"]
    priceJysk = dataJysk["Encoded"]["Data"]

    currentPriceSpot = round(priceSpot[-2], 1)
    currentPriceOil  = round(priceOil[-1], 1)
    currentPriceJysk = round(priceJysk[-2],1)
    return [currentPriceOil, currentPriceSpot, currentPriceJysk]
    
def main():
    wifiCheck()
    console = Console()
    table = Table(title="-|STONKS TOOLS|-")
    table.add_column("IDX")
    table.add_column("PROGRAM")
    table.add_column("DESCRIPTION")
    table.add_column("PRICE")
    
    scripts = {
        "1": ["oil.py", "Oil Stock Prices"],
        "2": ["spot.py", "Spotify Stock Prices"],
        "3": ["jysk.py", "Jysk Stock Prices"],
    }
    letterScripts = {
        "oil": "1",
        "spot": "2",
        "jysk": "3",
    }
    

    prices = {
        "oil":  f"{str(stockPrice()[0])}$",
        "spot": f"{str(stockPrice()[1])}$",
        "jysk": f"{str(stockPrice()[2])}$",
    }
    for k,v in scripts.items():
        table.add_row(k,v[0].split('.py')[0].title(), v[1],prices[v[0].split('.py')[0]])

    console.print(table)
    choice = input("Number: ").strip()

    if choice.isalpha() and choice in letterScripts:
        program = scripts[letterScripts[choice]][0]
    elif choice.isdigit() and  int(choice) > len(scripts):
        print(f"number cant be higher than {len(scripts)}")
    else:
        program = scripts[choice][0]
    print(f"starting {program}...")
    os.system(f"python {program}")
try:
    main()
except KeyboardInterrupt:
    print("Exiting....")